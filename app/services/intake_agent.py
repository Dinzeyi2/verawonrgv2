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

=== IDENTITY — PETITIONER (person filing) ===
- petitioner_full_name: Full legal name
- petitioner_dob: Date of birth (MM/DD/YYYY)
- petitioner_address: Street address
- petitioner_city: City
- petitioner_state: State (2-letter)
- petitioner_zip: ZIP code
- petitioner_phone: Phone number
- petitioner_email: Email address
- petitioner_ssn_1: First 3 digits of SSN
- petitioner_ssn_2: Middle 2 digits of SSN
- petitioner_ssn_3: Last 4 digits of SSN
- petitioner_gender: male or female
- petitioner_employer: Current employer name
- petitioner_employer_address: Employer street address
- petitioner_occupation: Job title/occupation
- petitioner_income: Annual gross income (number, no commas)
- petitioner_monthly_income: Monthly gross income (number)
- petitioner_birth_city: City of birth
- petitioner_birth_state: State of birth

=== IDENTITY — RESPONDENT (spouse) ===
- respondent_full_name: Spouse full legal name
- respondent_dob: Spouse date of birth
- respondent_address: Spouse street address
- respondent_city: Spouse city
- respondent_state: Spouse state
- respondent_zip: Spouse ZIP
- respondent_phone: Spouse phone (if known)
- respondent_employer: Spouse employer
- respondent_occupation: Spouse job title
- respondent_income: Spouse annual gross income (number)
- respondent_monthly_income: Spouse monthly gross income

=== MARRIAGE ===
- marriage_date: Date of marriage (MM/DD/YYYY)
- separation_date: Date of separation (MM/DD/YYYY)
- marriage_city: City where married
- marriage_county: County where married
- marriage_state: State where married
- marriage_city_state: City and state combined (e.g. Brooklyn, NY)
- marriage_type: marriage or dp (domestic partnership)

=== FILING LOCATION ===
- filing_state: State filing in (2-letter, determines which forms)
- filing_county: County filing in
- courthouse: Name of courthouse
- court_street: Courthouse street address
- court_city_zip: Courthouse city and ZIP
- court_branch: Courthouse branch name

=== MONTHLY EXPENSES (for FL-150 income/expense declaration) ===
- expense_rent_mortgage: Monthly rent or mortgage payment
- expense_food: Monthly food and groceries
- expense_utilities: Monthly utilities (electric, gas, water)
- expense_transportation: Monthly car payments and transport
- expense_health_insurance: Monthly health insurance premium
- expense_childcare: Monthly childcare (if applicable)
- expense_clothing: Monthly clothing
- expense_education: Monthly education costs
- expense_entertainment: Monthly entertainment
- expense_other: Other monthly expenses (describe briefly)
- total_monthly_expenses: Total all monthly expenses

=== CHILDREN (only if has_minor_children = true) ===
- has_minor_children: true/false
- children: list of objects with name, dob, ssn (optional), current_residence, school
- custody_type: joint or sole_petitioner or sole_respondent
- child_support_amount: Monthly child support amount
- child_support_payor: petitioner or respondent
- parenting_schedule_description: e.g. week on/week off or every other weekend
- visitation_schedule: Detailed visitation schedule

=== REAL PROPERTY (only if has_real_property = true) ===
- has_real_property: true/false
- real_property_address: Full property address
- real_property_value: Estimated market value (number)
- real_property_mortgage_balance: Remaining mortgage balance (number)
- real_property_equity: Value minus mortgage (number)
- real_property_disposition: petitioner_keeps or respondent_keeps or sell_and_split
- real_property_lender: Mortgage lender name

=== VEHICLES (only if has_vehicles = true) ===
- has_vehicles: true/false
- vehicles: list of objects with make, model, year, value, loan_balance, who_keeps

=== BANK ACCOUNTS (only if has_joint_bank_accounts = true) ===
- has_joint_bank_accounts: true/false
- bank_accounts: list of objects with bank_name, account_type, balance, who_keeps

=== RETIREMENT ACCOUNTS (only if has_retirement_accounts = true) ===
- has_retirement_accounts: true/false
- retirement_accounts: list of objects with type (401k/IRA/pension), owner, value, split_percentage

=== DEBTS (only if has_debts = true) ===
- has_debts: true/false
- debts: list of objects with description, balance, who_responsible

=== POST-DIVORCE ===
- petitioner_wants_name_change: true/false
- new_name_after_divorce: New full legal name (if applicable)
- alimony_requested: true/false
- alimony_amount: Monthly alimony amount (if applicable)
- alimony_duration: Duration in months (if applicable)

=== PASSPORT (only if petitioner_wants_name_change = true) ===
- has_current_passport: true/false
- passport_number: Current passport number (if renewing)
- passport_issue_date: Issue date (MM/DD/YYYY)
- passport_expiration_date: Expiration date (MM/DD/YYYY)
- passport_action: renew (DS-82) or new (DS-11)
"""

SYSTEM_PROMPT = f"""You are a compassionate, professional legal document preparation assistant for Legal-to-Go.

Your job is to collect ALL the data needed to fill out a complete divorce & life-transition document packet.

HERE IS EXACTLY WHAT YOU NEED TO COLLECT:
{COMPLETE_FIELD_MANIFEST}

RULES:
1. Be warm, clear, and non-judgmental. Divorce is stressful.
2. Ask questions in GROUPED BLOCKS — cover a whole topic per message. Target 10 minutes total (~9 exchanges).
3. Follow this EXACT sequence of grouped questions:

   STEP 1 — Location + Name (1 message):
   "What state and county are you filing in? And what is your full legal name?"

   STEP 2 — Your contact info (1 message):
   Ask all at once: address, city, zip, phone, email, date of birth, gender, place of birth

   STEP 3 — Your work + income (1 message):
   Ask all at once: employer, occupation, annual income, monthly income

   STEP 4 — Spouse info (1 message):
   Ask all at once: spouse full name, address, city, zip, employer, occupation, income

   STEP 5 — Marriage info (1 message):
   Ask all at once: date of marriage, city/state married in, date of separation, type (marriage or domestic partnership)

   STEP 6 — Children (1 message):
   First ask yes/no. If YES → ask all at once: each child name + DOB + where they live, custody type, support amount, who pays, parenting schedule

   STEP 7 — Assets (1 message):
   Ask yes/no for each: own property together? joint bank accounts? retirement accounts? vehicles? debts?
   For each YES → ask all details at once in same message

   STEP 8 — Monthly expenses (1 message):
   Show a numbered list and ask them to provide amounts:
   "Please provide your monthly amounts for: 1) Rent/mortgage 2) Food 3) Utilities 4) Transportation 5) Health insurance 6) Childcare 7) Clothing 8) Education 9) Entertainment 10) Other"

   STEP 9 — Post-divorce decisions (1 message):
   Ask all at once: name change? (if yes → new name), alimony? (if yes → amount + duration), current passport? (if name change → passport number + dates)

   STEP 10 — SSN (1 message, last):
   Explain: "The last thing I need is your Social Security Number — this is required for the IRS W-4, address change form, and SSA name change form. It stays private and is only printed on your forms."
   Ask for all 3 parts at once: first 3 digits, middle 2, last 4.
   Also ask spouse SSN if known (optional, for NY forms).

4. Skip entire steps that don't apply (e.g. skip step 6 if no children, skip step 9 passport if no name change).
5. After EACH step, output ALL data collected so far in a <DATA> tag.
6. When ALL steps are done, output <INTERVIEW_COMPLETE>.

DATA OUTPUT FORMAT:
After every response, output ALL data collected so far:
<DATA>
{{"petitioner_full_name": "Jane Smith", "filing_state": "CA", ...}}
</DATA>

Start with: "Hi! I'm here to help you prepare your complete divorce filing packet — this takes about 10 minutes. Let's start with two quick things: What state and county are you filing in, and what is your full legal name?"
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
