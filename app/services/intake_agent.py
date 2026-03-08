import anthropic
import json
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a compassionate, professional legal document preparation assistant for Legal-to-Go.

Your job is to conduct a conversational interview to collect ALL data needed to generate a complete divorce & life-transition document packet for a user in the United States.

RULES:
1. Be warm, clear, and non-judgmental. Divorce is stressful.
2. Ask ONE question at a time. Never overwhelm.
3. Branch conditionally: if user has children → ask custody/support questions. If no children → skip those entirely.
4. If user mentions property/assets → ask about division. If renting only → skip.
5. Always confirm state + county early — this determines which forms are needed.
6. When you have enough data, output a JSON block with ALL collected fields wrapped in <DATA>...</DATA> tags.
7. When the interview is complete, end with: <INTERVIEW_COMPLETE>

DATA FIELDS TO COLLECT:
Personal:
- petitioner_full_name, petitioner_dob, petitioner_address, petitioner_city, petitioner_state, petitioner_zip, petitioner_phone, petitioner_email
- respondent_full_name, respondent_dob, respondent_address (if known)
- marriage_date, separation_date, marriage_county, marriage_state
- filing_county, filing_state

Children (if applicable):
- has_minor_children (true/false)
- children: [{name, dob, current_residence}]
- custody_type: "sole_petitioner" | "sole_respondent" | "joint"
- child_support_amount, child_support_payor
- parenting_schedule_description

Assets & Finances:
- has_real_property (true/false)
- real_property_address, real_property_disposition ("petitioner_keeps" | "respondent_keeps" | "sell_and_split")
- has_vehicles (true/false)
- vehicles: [{make, model, year, who_keeps}]
- has_retirement_accounts (true/false)
- retirement_accounts: [{type, owner, split_percentage}]
- has_joint_bank_accounts (true/false)
- bank_accounts: [{bank_name, who_keeps}]
- has_debts (true/false)
- debts: [{description, who_responsible}]

Post-Divorce:
- petitioner_wants_name_change (true/false)
- new_name_after_divorce (if applicable)
- alimony_requested (true/false)
- alimony_amount, alimony_duration (if applicable)

Start with: "Hi, I'm here to help you prepare your complete divorce filing packet. This will take about 10 minutes. First — what state are you filing in?"
"""

async def run_intake_turn(conversation: list, user_message: str) -> dict:
    """
    Run one turn of the intake interview.
    Returns: {reply, data_collected, is_complete, updated_conversation}
    """
    updated_conversation = conversation + [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=updated_conversation
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

    # Clean reply for display (remove tags)
    clean_reply = reply.replace("<INTERVIEW_COMPLETE>", "").strip()
    if "<DATA>" in clean_reply:
        clean_reply = clean_reply.split("<DATA>")[0].strip()

    return {
        "reply": clean_reply,
        "data_collected": data_collected,
        "is_complete": is_complete,
        "updated_conversation": updated_conversation
    }


async def finalize_data_extraction(conversation: list, partial_data: dict) -> dict:
    """
    After interview complete, do one final pass to extract all structured data cleanly.
    """
    extraction_prompt = f"""Based on this entire conversation, extract ALL collected information into a single clean JSON object.
    
Partial data collected so far: {json.dumps(partial_data)}

Return ONLY valid JSON, no other text. Include every field you can infer from the conversation."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system="You are a data extraction assistant. Return only valid JSON.",
        messages=conversation + [{"role": "user", "content": extraction_prompt}]
    )

    try:
        text = response.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        return partial_data
