"""
Legal-to-Go — Form Registry
Only verified, confirmed-working URLs.
Currently supported: New York + all Federal forms.
Add more states as you verify their URLs.

Features:
  01_divorce     — Divorce petition + financial forms
  02_name_change — SSA, Passport, DMV
  03_asset       — Property settlement, QDRO, financial affidavit
  04_coparenting — Parenting plan, child support
  05_financial   — W-4, beneficiary audit, COBRA, tax guides
"""

FORM_REGISTRY = {

    # ══════════════════════════════════════════════════════════════
    # FEATURE 1 — DIVORCE PETITION FORMS
    # ══════════════════════════════════════════════════════════════
    "01_divorce": {
        "California": [
            ("CA_FL100_petition.pdf",       "https://www.courts.ca.gov/documents/fl100.pdf"),
            ("CA_FL110_summons.pdf",        "https://www.courts.ca.gov/documents/fl110.pdf"),
            ("CA_FL120_response.pdf",       "https://www.courts.ca.gov/documents/fl120.pdf"),
            ("CA_FL150_income_expense.pdf", "https://www.courts.ca.gov/documents/fl150.pdf"),
            ("CA_FL180_judgment.pdf",       "https://www.courts.ca.gov/documents/fl180.pdf"),
            ("CA_FL142_assets_debts.pdf",   "https://www.courts.ca.gov/documents/fl142.pdf"),
            ("CA_FL160_property.pdf",       "https://www.courts.ca.gov/documents/fl160.pdf"),
        ],
        "New York": [
            ("NY_composite_uncontested_divorce_forms.pdf", "https://www.nycourts.gov/LegacyPDFS/divorce/COMPOSITE-UNCONTESTED-DIVORCE-FORMS.pdf"),
            ("NY_UD1_summons.pdf",                         "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-1.pdf"),
            ("NY_UD2_verified_complaint.pdf",              "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-2.pdf"),
            ("NY_UD6_sworn_affidavit.pdf",                 "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-6.pdf"),
            ("NY_UD7_affirmation_defendant.pdf",           "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-7.pdf"),
            ("NY_UD9_note_of_issue.pdf",                   "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-9.pdf"),
            ("NY_UD11_judgment_divorce.pdf",               "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-11.pdf"),
            ("NY_UD13_rji.pdf",                            "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-13.pdf"),
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 2 — NAME CHANGE FORMS
    # ══════════════════════════════════════════════════════════════
    "02_name_change": {
        "_FEDERAL": [
            ("SSA_SS5_name_change.pdf",          "https://www.ssa.gov/forms/ss-5.pdf"),
            ("DS82_passport_renewal.pdf",        "https://eforms.state.gov/Forms/ds82.pdf"),
            ("DS11_new_passport.pdf",            "https://eforms.state.gov/Forms/ds11.pdf"),
            ("DS5504_name_error_correction.pdf", "https://eforms.state.gov/Forms/ds5504.pdf"),
        ],
        "California": [
            ("CA_DL44_license_application.pdf",  "https://www.dmv.ca.gov/portal/uploads/2020/05/dl44.pdf"),
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 3 — ASSET TRANSFER FORMS
    # ══════════════════════════════════════════════════════════════
    "03_asset": {
        "_FEDERAL": [
            ("DOL_QDRO_guide.pdf",      "https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/qdros-the-division-of-retirement-benefits-through-qualified-domestic-relations-orders.pdf"),
            ("DOL_COBRA_guide.pdf",     "https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-to-health-benefits-under-cobra.pdf"),
            ("IRS_Pub575_pension.pdf",  "https://www.irs.gov/pub/irs-pdf/p575.pdf"),
        ],
        "California": [
            ("CA_FL160_property.pdf",       "https://www.courts.ca.gov/documents/fl160.pdf"),
            ("CA_FL142_assets_debts.pdf",   "https://www.courts.ca.gov/documents/fl142.pdf"),
            ("CA_FL150_income_expense.pdf", "https://www.courts.ca.gov/documents/fl150.pdf"),
        ],
        "New York": [
            ("NY_net_worth_statement.pdf",      "https://www.nycourts.gov/forms/matrimonial/networth.pdf"),
            ("NY_UD9_financial_disclosure.pdf", "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-9.pdf"),
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 4 — CO-PARENTING PLAN FORMS
    # ══════════════════════════════════════════════════════════════
    "04_coparenting": {
        "California": [
            ("CA_FL341_custody_visitation.pdf", "https://www.courts.ca.gov/documents/fl341.pdf"),
            ("CA_FL342_child_support.pdf",      "https://www.courts.ca.gov/documents/fl342.pdf"),
            ("CA_FL311_custody_decl.pdf",       "https://www.courts.ca.gov/documents/fl311.pdf"),
        ],
        "New York": [
            ("NY_composite_divorce_with_children.pdf", "https://www.nycourts.gov/LegacyPDFS/divorce/COMPOSITE-UNCONTESTED-DIVORCE-FORMS.pdf"),
            ("NY_UD6_affidavit_custody.pdf",           "https://www.nycourts.gov/LegacyPDFS/divorce/forms_instructions/ud-6.pdf"),
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 5 — FINANCIAL RESET + BENEFICIARY AUDIT
    # ══════════════════════════════════════════════════════════════
    "05_financial": {
        "_FEDERAL": [
            ("IRS_W4_withholding.pdf",        "https://www.irs.gov/pub/irs-pdf/fw4.pdf"),
            ("IRS_W4P_pension.pdf",           "https://www.irs.gov/pub/irs-pdf/fw4p.pdf"),
            ("IRS_8332_child_exemption.pdf",  "https://www.irs.gov/pub/irs-pdf/f8332.pdf"),
            ("IRS_Pub504_divorced_taxes.pdf", "https://www.irs.gov/pub/irs-pdf/p504.pdf"),
            ("IRS_Pub501_filing_status.pdf",  "https://www.irs.gov/pub/irs-pdf/p501.pdf"),
            ("IRS_8822_address_change.pdf",   "https://www.irs.gov/pub/irs-pdf/f8822.pdf"),
            ("SSA_survivors_guide.pdf",       "https://www.ssa.gov/pubs/EN-05-10084.pdf"),
            ("DOL_COBRA_guide.pdf",           "https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-to-health-benefits-under-cobra.pdf"),
            ("DOL_QDRO_guide.pdf",            "https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/qdros-the-division-of-retirement-benefits-through-qualified-domestic-relations-orders.pdf"),
        ],
        "California": [
            ("CA_FL150_income_expense.pdf", "https://www.courts.ca.gov/documents/fl150.pdf"),
            ("CA_FL157_spousal_support.pdf","https://www.courts.ca.gov/documents/fl157.pdf"),
        ],
        "New York": [
            ("NY_net_worth_statement.pdf",    "https://www.nycourts.gov/forms/matrimonial/networth.pdf"),
        ],
    },
}


def get_forms_for_session(state: str, has_children: bool, wants_name_change: bool, has_assets: bool) -> dict:
    needed = {}
    needed["01_divorce"] = FORM_REGISTRY["01_divorce"].get(state, [])
    if wants_name_change:
        needed["02_name_change"] = (
            FORM_REGISTRY["02_name_change"].get("_FEDERAL", []) +
            FORM_REGISTRY["02_name_change"].get(state, [])
        )
    if has_assets:
        needed["03_asset"] = (
            FORM_REGISTRY["03_asset"].get("_FEDERAL", []) +
            FORM_REGISTRY["03_asset"].get(state, [])
        )
    if has_children:
        needed["04_coparenting"] = FORM_REGISTRY["04_coparenting"].get(state, [])
    needed["05_financial"] = (
        FORM_REGISTRY["05_financial"].get("_FEDERAL", []) +
        FORM_REGISTRY["05_financial"].get(state, [])
    )
    return needed


def get_supported_states() -> list:
    return list(FORM_REGISTRY["01_divorce"].keys())
