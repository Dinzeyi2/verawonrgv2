"""
SMART INTAKE AGENT v4
Flow:
  1. Ask 3 screening questions → determine which forms are needed
  2. Fetch those PDFs → extract real field names + labels
  3. Claude reads the field labels → generates targeted questions
  4. User answers → Claude maps answers to exact field names
  5. Every field filled correctly
"""

import anthropic
import json
import logging
import requests
import io
from pypdf import PdfReader
from app.core.config import settings
from app.services.form_registry import FORM_REGISTRY

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Extract real field names from PDFs
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_pdf_fields(url: str, filename: str) -> dict:
    """Fetch a PDF and return its real AcroForm field names and labels."""
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return {"filename": filename, "type": "unavailable"}

        reader = PdfReader(io.BytesIO(resp.content))
        fields = reader.get_fields()

        if not fields:
            return {"filename": filename, "type": "flat_pdf", "fields": []}

        field_list = []
        for name, field in fields.items():
            label = str(field.get("/TU", field.get("/T", name)))
            ftype = str(field.get("/FT", "text"))
            field_list.append({
                "field_name": name,
                "label": label,
                "type": ftype
            })

        return {"filename": filename, "type": "fillable", "fields": field_list}

    except Exception as e:
        logger.error(f"Failed to fetch {filename}: {e}")
        return {"filename": filename, "type": "error", "fields": []}


def get_forms_and_fields(state: str, has_children: bool, wants_name_change: bool, has_assets: bool) -> list:
    """
    Given screening answers, return list of needed forms with their real PDF fields.
    """
    from app.services.form_registry import get_forms_for_session
    needed = get_forms_for_session(state, has_children, wants_name_change, has_assets)

    forms_with_fields = []
    for feature, form_list in needed.items():
        for filename, url in form_list:
            # Skip pure reference/guide PDFs — they have no fillable fields
            skip_keywords = ["guide", "pub501", "pub504", "pub575", "survivors", "cobra"]
            if any(kw in filename.lower() for kw in skip_keywords):
                forms_with_fields.append({
                    "filename": filename,
                    "feature": feature,
                    "type": "reference",
                    "fields": []
                })
                continue

            field_data = _fetch_pdf_fields(url, filename)
            field_data["feature"] = feature
            forms_with_fields.append(field_data)

    return forms_with_fields


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Build targeted question list from real field labels
# ─────────────────────────────────────────────────────────────────────────────

def _build_question_prompt(forms_with_fields: list) -> str:
    """
    Given real PDF field names, ask Claude to generate grouped questions
    that will fill every field.
    """
    # Summarize fields for Claude
    field_summary = []
    for form in forms_with_fields:
        if form["type"] == "fillable" and form["fields"]:
            field_summary.append(f"\n=== {form['filename']} ===")
            for f in form["fields"]:
                field_summary.append(f"  - [{f['field_name']}] \"{f['label']}\" ({f['type']})")

    fields_text = "\n".join(field_summary)

    return f"""You are preparing a divorce filing packet. Here are the EXACT fields in the PDF forms that need to be filled:

{fields_text}

Your job: generate a grouped interview to collect all the data needed to fill every single field above.

Rules:
1. Group related fields into natural conversation blocks (identity, marriage, children, assets, etc.)
2. Ask each group in ONE message — never ask one field at a time
3. Only ask what's needed — don't ask for fields that don't exist in these forms
4. Be warm and empathetic — divorce is hard
5. After ALL data is collected, output a JSON object with field_name → value mappings
6. Format the JSON inside <FIELD_DATA>...</FIELD_DATA> tags

Start the interview now with the first group of questions."""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN INTAKE FLOW
# ─────────────────────────────────────────────────────────────────────────────

SCREENING_PROMPT = """You are a legal document preparation assistant for Legal-to-Go.

Start by asking EXACTLY these 4 screening questions in ONE message to determine which forms are needed:

1. What state are you filing in? (This determines which court forms you get)
2. Do you have minor children together (under 18)? (yes/no)
3. Do you want to change your name after the divorce? (yes/no)  
4. Do you have significant assets together — property, retirement accounts, or investments? (yes/no)

After they answer, output their answers in this exact format:
<SCREENING>
{"state": "California", "has_children": false, "wants_name_change": false, "has_assets": false}
</SCREENING>

Then say: "Thank you! Give me a moment while I pull up the exact forms you'll need..."
And output: <SCREENING_COMPLETE>
"""


INTERVIEW_SYSTEM = """You are a compassionate legal document preparation assistant for Legal-to-Go.

You have been given the EXACT field names from the PDF forms this person needs to fill out.
Your job is to ask questions that will collect data for every single field, then map the answers back to exact field names.

Rules:
1. Ask questions in grouped blocks — cover a whole topic per message (never one field at a time)
2. Be warm and clear — divorce is stressful
3. Accept rough answers and move on
4. When done collecting ALL data, output the complete field mapping as JSON inside <FIELD_DATA>...</FIELD_DATA> tags
5. Then output <INTERVIEW_COMPLETE>

The JSON inside <FIELD_DATA> must map exact PDF field names to values, like:
<FIELD_DATA>
{"FL-100[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party1_ft[0]": "Jane Smith", ...}
</FIELD_DATA>
"""


async def run_intake_turn(conversation: list, user_message: str, session_meta: dict = None) -> dict:
    """
    Main intake turn handler.
    session_meta holds: {stage, state, has_children, wants_name_change, has_assets, forms_with_fields}
    """
    if session_meta is None:
        session_meta = {}

    stage = session_meta.get("stage", "screening")

    # ── STAGE 1: Screening ────────────────────────────────────────
    if stage == "screening" or not conversation:
        if user_message == "__START__":
            updated_conversation = [{"role": "user", "content": "Start"}]
        else:
            updated_conversation = conversation + [{"role": "user", "content": user_message}]

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=SCREENING_PROMPT,
            messages=updated_conversation
        )

        reply = response.content[0].text
        updated_conversation.append({"role": "assistant", "content": reply})

        # Check if screening is complete
        screening_data = {}
        if "<SCREENING>" in reply and "</SCREENING>" in reply:
            try:
                raw = reply.split("<SCREENING>")[1].split("</SCREENING>")[0].strip()
                screening_data = json.loads(raw)
            except Exception:
                pass

        screening_complete = "<SCREENING_COMPLETE>" in reply
        clean_reply = reply.replace("<SCREENING_COMPLETE>", "")
        if "<SCREENING>" in clean_reply:
            clean_reply = clean_reply.split("<SCREENING>")[0]
        clean_reply = clean_reply.strip()

        return {
            "reply": clean_reply,
            "data_collected": screening_data,
            "is_complete": False,
            "screening_complete": screening_complete,
            "updated_conversation": updated_conversation,
            "stage": "screening"
        }

    # ── STAGE 2: Form-aware interview ─────────────────────────────
    elif stage == "interview":
        forms_with_fields = session_meta.get("forms_with_fields", [])
        system_prompt = INTERVIEW_SYSTEM

        # Build field context for Claude
        field_context = _build_question_prompt(forms_with_fields)
        system_prompt = INTERVIEW_SYSTEM + f"\n\n{field_context}"

        updated_conversation = conversation + [{"role": "user", "content": user_message}]

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=system_prompt,
            messages=updated_conversation
        )

        reply = response.content[0].text
        updated_conversation.append({"role": "assistant", "content": reply})

        # Extract field data if present
        field_data = {}
        if "<FIELD_DATA>" in reply and "</FIELD_DATA>" in reply:
            try:
                raw = reply.split("<FIELD_DATA>")[1].split("</FIELD_DATA>")[0].strip()
                field_data = json.loads(raw)
            except Exception:
                pass

        is_complete = "<INTERVIEW_COMPLETE>" in reply
        clean_reply = reply.replace("<INTERVIEW_COMPLETE>", "")
        if "<FIELD_DATA>" in clean_reply:
            clean_reply = clean_reply.split("<FIELD_DATA>")[0]
        clean_reply = clean_reply.strip()

        return {
            "reply": clean_reply,
            "data_collected": field_data,
            "is_complete": is_complete,
            "screening_complete": False,
            "updated_conversation": updated_conversation,
            "stage": "interview"
        }

    return {
        "reply": "Something went wrong. Please refresh and try again.",
        "data_collected": {},
        "is_complete": False,
        "screening_complete": False,
        "updated_conversation": conversation,
        "stage": stage
    }


async def finalize_data_extraction(conversation: list, partial_data: dict) -> dict:
    """Final pass — returns the field_data as-is since it already has exact field names."""
    # partial_data already has exact PDF field names from <FIELD_DATA> tags
    # Just do a cleanup pass to catch anything missed
    extraction_prompt = f"""Based on this conversation, extract ALL data collected and return it as a JSON object.

The keys should be the exact PDF field names discussed. Use the partial data as a base and fill in anything missing.

Partial data: {json.dumps(partial_data)}

Return ONLY valid JSON, no markdown, no backticks."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        system="Return only valid JSON, no markdown.",
        messages=conversation + [{"role": "user", "content": extraction_prompt}]
    )

    try:
        text = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
        extracted = json.loads(text)
        return {**partial_data, **extracted}
    except Exception as e:
        logger.error(f"finalize failed: {e}")
        return partial_data
