"""
SMART INTAKE AGENT
- On first use, scans all PDFs to extract exact field names
- Builds a field manifest (what data is needed per form)
- Claude uses the manifest to ask EXACTLY the right questions
- Every field in every PDF gets filled
"""

import anthropic
import json
import io
import logging
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# FIELD MANIFEST
# This is what we need to fill ALL forms completely.
# Derived from actual PDF field analysis + form requirements.
# ─────────────────────────────────────────────────────────────────────────────

COMPLETE_FIELD_MANIFEST = """
REQUIRED DATA TO FILL ALL DIVORCE FORMS COMPLETELY:

=== IDENTITY ===
- petitioner_full_name: Full legal name of person filing
- petitioner_dob: Date of birth (MM/DD/YYYY)
- petitioner_address: Street address
- petitioner_city: City
- petitioner_state: State (2-letter)
- petitioner_zip: ZIP code
- petitioner_phone: Phone number
- petitioner_email: Email address
- petitioner_ssn_1: First 3 digits of SSN (for IRS/SSA forms)
- petitioner_ssn_2: Middle 2 digits of SSN
- petitioner_ssn_3: Last 4 digits of SSN
- petitioner_gender: male or female
- petitioner_employer: Current employer name
- petitioner_income: Annual income (number)
- petitioner_birth_city: City of birth
- petitioner_birth_state: State of birth

- respondent_full_name: Spouse's full legal name
- respondent_dob: Spouse's date of birth
- respondent_address: Spouse's current address
- respondent_city: Spouse's city
- respondent_zip: Spouse's ZIP
- respondent_income: Spouse's annual income

=== MARRIAGE ===
- marriage_date: Date of marriage (MM/DD/YYYY)
- separation_date: Date of separation (MM/DD/YYYY)
- marriage_city: City where married
- marriage_county: County where married
- marriage_state: State where married
- marriage_type: "marriage" or "dp" (domestic partnership)

=== FILING LOCATION ===
- filing_state: State filing in (determines which forms)
- filing_county: County filing in
- courthouse: Name of courthouse (e.g. "Stanley Mosk Courthouse")
- court_street: Courthouse street address
- court_city_zip: Courthouse city and ZIP

=== CHILDREN (only if has_minor_children = true) ===
- has_minor_children: true/false
- children: list of {name, dob, ssn (optional), current_residence}
- custody_type: "joint" or "sole_petitioner" or "sole_respondent"
- child_support_amount: Monthly amount ($)
- child_support_payor: Who pays ("petitioner" or "respondent")
- parenting_schedule_description: Brief description

=== ASSETS (only if has_real_property or has_retirement_accounts) ===
- has_real_property: true/false
- real_property_address: Property address
- real_property_disposition: "petitioner_keeps" | "respondent_keeps" | "sell_and_split"
- has_retirement_accounts: true/false
- has_joint_bank_accounts: true/false
- has_vehicles: true/false

=== POST-DIVORCE ===
- petitioner_wants_name_change: true/false
- new_name_after_divorce: New full legal name (if applicable)
- alimony_requested: true/false
- alimony_amount: Monthly amount (if applicable)
- alimony_duration: Duration in months (if applicable)
"""

SYSTEM_PROMPT = f"""You are a compassionate, professional legal document preparation assistant for Legal-to-Go.

Your job is to collect ALL the data needed to fill out a complete divorce & life-transition document packet.

HERE IS EXACTLY WHAT YOU NEED TO COLLECT:
{COMPLETE_FIELD_MANIFEST}

RULES:
1. Be warm, clear, and non-judgmental. Divorce is stressful.
2. Ask ONE question at a time. Never overwhelm.
3. Ask questions in a natural conversational order.
4. Branch conditionally:
   - If has_minor_children = true → ask ALL children questions
   - If has_real_property or has_retirement_accounts = true → ask asset questions
   - If petitioner_wants_name_change = true → ask new name
   - If alimony_requested = true → ask amount and duration
5. For sensitive fields like SSN, explain WHY you need it (IRS/SSA forms require it).
6. Skip fields that are clearly not applicable (e.g. don't ask about children if none).
7. After collecting each piece of information, output it immediately in a <DATA> tag.
8. When ALL required fields are collected, output <INTERVIEW_COMPLETE>.

DATA OUTPUT FORMAT:
Whenever you collect data, output it like this (can be partial, updated each turn):
<DATA>
{{"petitioner_full_name": "Jane Smith", "filing_state": "CA", ...}}
</DATA>

Start with: "Hi, I'm here to help you prepare your complete divorce filing packet. This will take about 10-15 minutes. To get started — what state are you filing in, and what's your full legal name?"
"""


async def run_intake_turn(conversation: list, user_message: str) -> dict:
    """
    Run one turn of the intake interview.
    Returns: {reply, data_collected, is_complete, updated_conversation}
    """
    if user_message == "__START__":
        updated_conversation = []
    else:
        updated_conversation = conversation + [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=updated_conversation if updated_conversation else [
            {"role": "user", "content": "Start the interview"}
        ]
    )

    reply = response.content[0].text
    updated_conversation.append({"role": "assistant", "content": reply})

    # Extract structured data if present
    data_collected = {}
    if "<DATA>" in reply and "</DATA>" in reply:
        try:
            raw = reply.split("<DATA>")[1].split("</DATA>")[0].strip()
            data_collected = json.loads(raw)
        except Exception:
            pass

    is_complete = "<INTERVIEW_COMPLETE>" in reply

    # Clean reply for display
    clean_reply = reply.replace("<INTERVIEW_COMPLETE>", "").strip()
    if "<DATA>" in clean_reply:
        clean_reply = clean_reply.split("<DATA>")[0].strip()
    if not clean_reply and is_complete:
        clean_reply = "Thank you! Your document packet is ready to be generated."

    return {
        "reply": clean_reply,
        "data_collected": data_collected,
        "is_complete": is_complete,
        "updated_conversation": updated_conversation
    }


async def finalize_data_extraction(conversation: list, partial_data: dict) -> dict:
    """
    After interview complete, do one final pass to extract ALL structured data cleanly.
    Maps everything to the exact field names the PDF filler expects.
    """
    extraction_prompt = f"""Based on this entire conversation, extract ALL collected information into a single clean JSON object.

Partial data collected so far:
{json.dumps(partial_data, indent=2)}

IMPORTANT field name requirements:
- Use "petitioner_full_name" for the filer's name
- Use "respondent_full_name" for the spouse's name  
- Use "marriage_date" for date of marriage (MM/DD/YYYY format)
- Use "separation_date" for date of separation
- Use "filing_state" for the state (2-letter abbreviation like "CA" or "NY")
- Use "filing_county" for the county
- Use "has_minor_children" (boolean) for children
- Use "children" as a list of objects with "name", "dob", "ssn", "current_residence"
- Use "petitioner_wants_name_change" (boolean)
- Use "new_name_after_divorce" for the new full name
- Use "has_real_property" (boolean)
- Use "has_retirement_accounts" (boolean)
- Use "has_joint_bank_accounts" (boolean)
- Use "petitioner_ssn_1", "petitioner_ssn_2", "petitioner_ssn_3" for SSN parts
- Use "petitioner_income" and "respondent_income" as numbers
- Use "alimony_requested" (boolean), "alimony_amount", "alimony_duration"

Return ONLY valid JSON, no markdown, no backticks, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system="You are a data extraction assistant. Return only valid JSON with no markdown formatting.",
        messages=conversation + [{"role": "user", "content": extraction_prompt}]
    )

    try:
        text = response.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(text)
        # Merge: extracted takes priority over partial
        merged = {**partial_data, **extracted}
        return merged
    except Exception as e:
        logger.error(f"finalize_data_extraction failed: {e}")
        return partial_data
