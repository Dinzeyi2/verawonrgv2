"""
SMART INTAKE AGENT — v3
- Grouped questions (10 min flow)
- Does NOT rely on mid-conversation <DATA> tags
- Full extraction happens at end via finalize_data_extraction
- is_complete fires reliably on INTERVIEW_COMPLETE tag
"""

import anthropic
import json
import logging
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
logger = logging.getLogger(__name__)

COMPLETE_FIELD_MANIFEST = """
REQUIRED DATA TO FILL ALL DIVORCE FORMS COMPLETELY:

=== PETITIONER (person filing) ===
- petitioner_full_name, petitioner_dob, petitioner_address, petitioner_city
- petitioner_state, petitioner_zip, petitioner_phone, petitioner_email
- petitioner_gender, petitioner_birth_city, petitioner_birth_state
- petitioner_employer, petitioner_employer_address, petitioner_occupation
- petitioner_income (annual), petitioner_monthly_income
- petitioner_ssn_1 (first 3), petitioner_ssn_2 (middle 2), petitioner_ssn_3 (last 4)

=== RESPONDENT (spouse) ===
- respondent_full_name, respondent_dob, respondent_address, respondent_city
- respondent_state, respondent_zip, respondent_phone
- respondent_employer, respondent_occupation
- respondent_income (annual), respondent_monthly_income

=== MARRIAGE ===
- marriage_date (MM/DD/YYYY), separation_date (MM/DD/YYYY)
- marriage_city, marriage_county, marriage_state, marriage_city_state
- marriage_type: "marriage" or "dp"

=== FILING ===
- filing_state (2-letter), filing_county
- courthouse, court_street, court_city_zip

=== MONTHLY EXPENSES ===
- expense_rent_mortgage, expense_food, expense_utilities
- expense_transportation, expense_health_insurance, expense_childcare
- expense_clothing, expense_education, expense_entertainment, expense_other
- total_monthly_expenses

=== CHILDREN (if has_minor_children = true) ===
- has_minor_children (true/false)
- children: [{name, dob, ssn, current_residence, school}]
- custody_type: "joint" | "sole_petitioner" | "sole_respondent"
- child_support_amount, child_support_payor
- parenting_schedule_description, visitation_schedule

=== PROPERTY (if has_real_property = true) ===
- has_real_property (true/false)
- real_property_address, real_property_value, real_property_mortgage_balance
- real_property_equity, real_property_disposition, real_property_lender

=== OTHER ASSETS ===
- has_vehicles (true/false)
- vehicles: [{make, model, year, value, loan_balance, who_keeps}]
- has_joint_bank_accounts (true/false)
- bank_accounts: [{bank_name, account_type, balance, who_keeps}]
- has_retirement_accounts (true/false)
- retirement_accounts: [{type, owner, value, split_percentage}]
- has_debts (true/false)
- debts: [{description, balance, who_responsible}]

=== POST-DIVORCE ===
- petitioner_wants_name_change (true/false)
- new_name_after_divorce (if applicable)
- alimony_requested (true/false)
- alimony_amount, alimony_duration (if applicable)

=== PASSPORT (if name change = true) ===
- has_current_passport (true/false)
- passport_number, passport_issue_date, passport_expiration_date
- passport_action: "renew" or "new"
"""

SYSTEM_PROMPT = f"""You are a compassionate, professional legal document preparation assistant for Legal-to-Go.

Your job: collect ALL data needed to fill every field in a complete divorce & life-transition document packet. Complete the interview in exactly 10 steps, ~10 minutes total.

{COMPLETE_FIELD_MANIFEST}

INTERVIEW FLOW — follow this EXACTLY, one step per message:

STEP 1: Ask: state + county filing in, and their full legal name.

STEP 2: Ask all at once:
- Full street address, city, ZIP
- Phone number and email
- Date of birth (MM/DD/YYYY)
- Gender (male/female)
- Place of birth (city and state)

STEP 3: Ask all at once:
- Current employer name and address
- Job title/occupation
- Annual gross income
- Monthly gross income

STEP 4: Ask all at once:
- Spouse's full legal name
- Spouse's complete address (street, city, state, ZIP)
- Spouse's employer and occupation
- Spouse's annual income (if known)

STEP 5: Ask all at once:
- Date of marriage (MM/DD/YYYY)
- City and state where married
- Date of separation (MM/DD/YYYY)
- Marriage or domestic partnership?

STEP 6: Ask: do they have minor children together (under 18)?
- If YES → ask all at once: each child's name + DOB + residence, custody type, support amount, who pays, parenting schedule
- If NO → skip to step 7

STEP 7: Ask yes/no for each asset type:
- Real estate/property together?
- Joint bank accounts?
- Retirement accounts (401k, IRA, pension)?
- Vehicles together?
- Joint debts (credit cards, loans)?
For each YES → ask all details in the SAME message.

STEP 8: Show this list and ask for monthly dollar amounts:
"Please give me your monthly amounts for:
1. Rent/mortgage: $
2. Food/groceries: $
3. Utilities: $
4. Transportation: $
5. Health insurance: $
6. Childcare: $
7. Clothing: $
8. Education: $
9. Entertainment: $
10. Other: $"
If they say spouse pays everything, explain the court still needs THEIR personal estimates.

STEP 9: Ask all at once:
- Do you want to change your name after divorce? (if yes → what new name?)
- Are you requesting alimony/spousal support? (if yes → monthly amount + how many months?)
- Do you have a valid US passport? (if yes AND name change → ask passport number, issue date, expiration date)

STEP 10: Say: "Almost done! The last thing I need is your Social Security Number — required for the IRS W-4, address change form, and SSA name change form. It stays private and only appears on your forms."
Ask: all 3 parts of SSN at once (first 3 digits, middle 2, last 4).
Also ask: spouse's SSN if known (optional).

After step 10 is answered, output ONLY this — nothing else:
<INTERVIEW_COMPLETE>

RULES:
- Do NOT output <DATA> tags mid-interview. Just ask questions naturally.
- Skip steps that don't apply (no children → skip step 6, no name change → skip passport part of step 9).
- Be warm and empathetic. Divorce is hard.
- Accept partial/rough answers and move on. Don't interrogate.
- After step 10, output <INTERVIEW_COMPLETE> immediately.
"""


async def run_intake_turn(conversation: list, user_message: str) -> dict:
    if user_message == "__START__":
        updated_conversation = [{"role": "user", "content": "Start the interview"}]
    else:
        updated_conversation = conversation + [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=updated_conversation
    )

    reply = response.content[0].text
    updated_conversation.append({"role": "assistant", "content": reply})

    is_complete = "<INTERVIEW_COMPLETE>" in reply
    clean_reply = reply.replace("<INTERVIEW_COMPLETE>", "").strip()
    if not clean_reply and is_complete:
        clean_reply = "Thank you! All your information has been collected. Your document packet is now being prepared."

    return {
        "reply": clean_reply,
        "data_collected": {},   # We never rely on mid-turn data — finalize does it all
        "is_complete": is_complete,
        "updated_conversation": updated_conversation
    }


async def finalize_data_extraction(conversation: list, partial_data: dict) -> dict:
    """
    Single clean extraction pass over the full conversation.
    Maps everything to exact field names the PDF filler expects.
    """
    extraction_prompt = f"""Read this entire interview conversation and extract ALL information the user provided into a single JSON object.

Use EXACTLY these field names:
- petitioner_full_name, petitioner_dob, petitioner_address, petitioner_city, petitioner_state, petitioner_zip
- petitioner_phone, petitioner_email, petitioner_gender, petitioner_birth_city, petitioner_birth_state
- petitioner_employer, petitioner_employer_address, petitioner_occupation
- petitioner_income, petitioner_monthly_income
- petitioner_ssn_1, petitioner_ssn_2, petitioner_ssn_3
- respondent_full_name, respondent_dob, respondent_address, respondent_city, respondent_state, respondent_zip
- respondent_phone, respondent_employer, respondent_occupation, respondent_income, respondent_monthly_income
- marriage_date, separation_date, marriage_city, marriage_county, marriage_state, marriage_city_state, marriage_type
- filing_state, filing_county, courthouse, court_street, court_city_zip
- expense_rent_mortgage, expense_food, expense_utilities, expense_transportation
- expense_health_insurance, expense_childcare, expense_clothing, expense_education
- expense_entertainment, expense_other, total_monthly_expenses
- has_minor_children, children (list with name/dob/ssn/current_residence/school)
- custody_type, child_support_amount, child_support_payor
- parenting_schedule_description, visitation_schedule
- has_real_property, real_property_address, real_property_value, real_property_mortgage_balance
- real_property_equity, real_property_disposition, real_property_lender
- has_vehicles, vehicles (list with make/model/year/value/loan_balance/who_keeps)
- has_joint_bank_accounts, bank_accounts (list with bank_name/account_type/balance/who_keeps)
- has_retirement_accounts, retirement_accounts (list with type/owner/value/split_percentage)
- has_debts, debts (list with description/balance/who_responsible)
- petitioner_wants_name_change, new_name_after_divorce
- alimony_requested, alimony_amount, alimony_duration
- has_current_passport, passport_number, passport_issue_date, passport_expiration_date, passport_action

IMPORTANT:
- filing_state must be a 2-letter abbreviation (CA, NY, FL, etc.)
- SSN parts: petitioner_ssn_1 = first 3 digits, petitioner_ssn_2 = middle 2, petitioner_ssn_3 = last 4
- For expenses the user said spouse pays → use 0 for all expense fields
- income values should be numbers (no $ or commas)
- Return ONLY valid JSON. No markdown. No backticks. No explanation.

Partial data already collected: {json.dumps(partial_data)}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        system="You are a data extraction assistant. Return only valid JSON, no markdown, no backticks.",
        messages=conversation + [{"role": "user", "content": extraction_prompt}]
    )

    try:
        text = response.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(text)
        merged = {**partial_data, **extracted}
        return merged
    except Exception as e:
        logger.error(f"finalize_data_extraction failed: {e}")
        logger.error(f"Raw response: {response.content[0].text[:500]}")
        return partial_data
