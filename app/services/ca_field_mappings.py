"""
CA FILLABLE FORM FIELD MAPPINGS
Maps user interview data to exact AcroForm PDF field names.
"""

# ---------------------------------------------------------------------------
# CA FL-100 Petition for Dissolution
# ---------------------------------------------------------------------------
CA_FL100 = {
    "FL-100[0].Page1[0].CaptionP1_sf[0].FormTitle[0].DissolutionOf_cb[0]": True,
    "FL-100[0].Page1[0].CaptionP1_sf[0].FormTitle[0].Marriage_cb[0]": lambda d: d.get("marriage_type", "marriage") == "marriage",
    "FL-100[0].Page1[0].CaptionP1_sf[0].FormTitle[0].DomesticPartnership_cb[0]": lambda d: d.get("marriage_type") == "dp",
    "FL-100[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].CrtCounty_ft[0]": "county",
    "FL-100[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].Branch_ft[0]": "court_branch",
    "FL-100[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].Street_ft[0]": "court_street",
    "FL-100[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].CityZip_ft[0]": "court_city_zip",
    "FL-100[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party1_ft[0]": "petitioner_name",
    "FL-100[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party2_ft[0]": "respondent_name",
    "FL-100[0].Page1[0].PetitionerMeetsResidencyReqs_cb[0]": True,
    "FL-100[0].Page1[0].WeAreMarried_cb[0]": lambda d: d.get("marriage_type", "marriage") == "marriage",
    "FL-100[0].Page1[0].DateOfMarriage_dt[0]": "date_of_marriage",
    "FL-100[0].Page1[0].DateOfSeparation_dt[0]": "date_of_separation",
    "FL-100[0].Page1[0].ThereAreNoMinorChildren_cb[0]": lambda d: not d.get("has_children", False),
    "FL-100[0].Page1[0].MinorChildren_sf[0].MinorChildrenList_cb[0]": lambda d: d.get("has_children", False),
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child1Name_tf[0]": lambda d: d.get("children", [{}])[0].get("name", "") if d.get("children") else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child2Name_tf[0]": lambda d: d.get("children", [{}, {}])[1].get("name", "") if len(d.get("children", [])) > 1 else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child3Name_tf[0]": lambda d: d.get("children", [{}, {}, {}])[2].get("name", "") if len(d.get("children", [])) > 2 else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child1Age_tf[0]": lambda d: str(d.get("children", [{}])[0].get("age", "")) if d.get("children") else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child2Age_tf[0]": lambda d: str(d.get("children", [{}, {}])[1].get("age", "")) if len(d.get("children", [])) > 1 else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child1Birthdate_dt[0]": lambda d: d.get("children", [{}])[0].get("birthdate", "") if d.get("children") else "",
    "FL-100[0].Page1[0].MinorChildren_sf[0].Child2Birthdate_dt[0]": lambda d: d.get("children", [{}, {}])[1].get("birthdate", "") if len(d.get("children", [])) > 1 else "",
}

# ---------------------------------------------------------------------------
# CA FL-110 Summons
# ---------------------------------------------------------------------------
CA_FL110 = {
    "fl110[0].Page1[0].Caption_sf[0].AttyInfo[0].AttyFor_ft[0]": "petitioner_name",
    "fl110[0].Page1[0].Caption_sf[0].CourtInfo[0].CrtCounty_ft[0]": "county",
    "fl110[0].Page1[0].Caption_sf[0].CourtInfo[0].Branch_ft[0]": "court_branch",
    "fl110[0].Page1[0].Caption_sf[0].TitlePartyName[0].Party1_ft[0]": "petitioner_name",
    "fl110[0].Page1[0].Caption_sf[0].TitlePartyName[0].Party2_ft[0]": "respondent_name",
}

# ---------------------------------------------------------------------------
# CA FL-120 Response
# ---------------------------------------------------------------------------
CA_FL120 = {
    "FL-120[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].CrtCounty_ft[0]": "county",
    "FL-120[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].Branch_ft[0]": "court_branch",
    "FL-120[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].Street_ft[0]": "court_street",
    "FL-120[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].CityZip_ft[0]": "court_city_zip",
    "FL-120[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party1_ft[0]": "petitioner_name",
    "FL-120[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party2_ft[0]": "respondent_name",
    "FL-120[0].Page1[0].CaptionP1_sf[0].FormTitle[0].DissolutionOf_cb[0]": True,
    "FL-120[0].Page1[0].CaptionP1_sf[0].FormTitle[0].Marriage_cb[0]": lambda d: d.get("marriage_type", "marriage") == "marriage",
}

# ---------------------------------------------------------------------------
# CA FL-180 Judgment
# ---------------------------------------------------------------------------
CA_FL180 = {
    "FL-180[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].CrtCounty_ft[0]": "county",
    "FL-180[0].Page1[0].CaptionP1_sf[0].CourtInfo[0].Branch_ft[0]": "court_branch",
    "FL-180[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party1_ft[0]": "petitioner_name",
    "FL-180[0].Page1[0].CaptionP1_sf[0].TitlePartyName[0].Party2_ft[0]": "respondent_name",
    "FL-180[0].Page1[0].DissolutionOf_cb[0]": True,
    "FL-180[0].Page1[0].Marriage_cb[0]": lambda d: d.get("marriage_type", "marriage") == "marriage",
}

# ---------------------------------------------------------------------------
# IRS W-4
# ---------------------------------------------------------------------------
IRS_W4 = {
    "topmostSubform[0].Page1[0].f1_1[0]": "petitioner_first",
    "topmostSubform[0].Page1[0].f1_2[0]": "petitioner_last",
    "topmostSubform[0].Page1[0].f1_3[0]": "petitioner_address",
    "topmostSubform[0].Page1[0].f1_4[0]": lambda d: f"{d.get('petitioner_city','')} {d.get('petitioner_state','')} {d.get('petitioner_zip','')}",
    "topmostSubform[0].Page1[0].f1_5[0]": lambda d: f"{d.get('petitioner_ssn_1','')}-{d.get('petitioner_ssn_2','')}-{d.get('petitioner_ssn_3','')}",
    "topmostSubform[0].Page1[0].c1_3[0]": lambda d: d.get("has_children", False),
    "topmostSubform[0].Page1[0].c1_2[0]": lambda d: not d.get("has_children", False),
    "topmostSubform[0].Page1[0].f1_6[0]": "petitioner_employer",
}

# ---------------------------------------------------------------------------
# IRS 8822 Address Change
# ---------------------------------------------------------------------------
IRS_8822 = {
    "topmostSubform[0].Page1[0].f1_1[0]": "petitioner_first",
    "topmostSubform[0].Page1[0].f1_2[0]": "petitioner_last",
    "topmostSubform[0].Page1[0].f1_3[0]": lambda d: f"{d.get('petitioner_ssn_1','')}{d.get('petitioner_ssn_2','')}{d.get('petitioner_ssn_3','')}",
    "topmostSubform[0].Page1[0].f1_5[0]": "petitioner_address",
    "topmostSubform[0].Page1[0].f1_6[0]": "petitioner_city",
    "topmostSubform[0].Page1[0].f1_7[0]": "petitioner_state",
    "topmostSubform[0].Page1[0].f1_8[0]": "petitioner_zip",
}

# ---------------------------------------------------------------------------
# IRS 8332 Child Exemption Release
# ---------------------------------------------------------------------------
IRS_8332 = {
    "topmostSubform[0].Page1[0].f1_1[0]": lambda d: d.get("children", [{}])[0].get("name", "") if d.get("children") else "",
    "topmostSubform[0].Page1[0].f1_3[0]": "petitioner_name",
    "topmostSubform[0].Page1[0].f1_4[0]": lambda d: f"{d.get('petitioner_ssn_1','')}-{d.get('petitioner_ssn_2','')}-{d.get('petitioner_ssn_3','')}",
    "topmostSubform[0].Page1[0].f1_5[0]": "respondent_name",
}

# ---------------------------------------------------------------------------
# SSA SS-5 Name Change
# ---------------------------------------------------------------------------
SSA_SS5 = {
    "topmostSubform[0].Page1[0].P1_firstname_FLD[0]": "new_name_first",
    "topmostSubform[0].Page1[0].P1_middlename_FLD[0]": "new_name_middle",
    "topmostSubform[0].Page1[0].P1_lastname_FLD[0]": "new_name_last",
    "topmostSubform[0].Page2[0].P2_firstname_FLD[0]": "petitioner_first",
    "topmostSubform[0].Page2[0].P2_middlename_FLD[0]": "petitioner_middle",
    "topmostSubform[0].Page2[0].P2_lastname_FLD[0]": "petitioner_last",
    "topmostSubform[0].Page3[0].P3_date_of_birth_Date[0]": "petitioner_dob",
    "topmostSubform[0].Page3[0].P3_cityofbirth_FLD[0]": "petitioner_birth_city",
    "topmostSubform[0].Page3[0].P3_stateofbirth_FLD[0]": "petitioner_birth_state",
    "topmostSubform[0].Page3[0].P3_Male_Rb[0]": lambda d: d.get("petitioner_gender", "").lower() == "male",
    "topmostSubform[0].Page3[0].P3_Female_Rb[0]": lambda d: d.get("petitioner_gender", "").lower() == "female",
    "topmostSubform[0].Page4[0].P4_First_FLD[0]": "petitioner_ssn_1",
    "topmostSubform[0].Page4[0].P4_Second_FLD[0]": "petitioner_ssn_2",
    "topmostSubform[0].Page5[0].P5_firstname_FLD[0]": "petitioner_first",
    "topmostSubform[0].Page5[0].P5_Middlename_FLD[0]": "petitioner_middle",
    "topmostSubform[0].Page5[0].P5_LastName_FLD[0]": "petitioner_last",
    "topmostSubform[0].Page5[0].P5_streetaddress_FLD[0]": "petitioner_address",
    "topmostSubform[0].Page5[0].P5_mailingcity_FLD[0]": "petitioner_city",
    "topmostSubform[0].Page5[0].P5_state_FLD[0]": "petitioner_state",
    "topmostSubform[0].Page5[0].P5_zipcode_FLD[0]": "petitioner_zip",
    "topmostSubform[0].Page5[0].P5_areacode_FLD[0]": lambda d: d.get("petitioner_phone", "")[:3],
    "topmostSubform[0].Page5[0].P5_phonenumber_FLD[0]": lambda d: d.get("petitioner_phone", "")[3:],
    "topmostSubform[0].Page5[0].P5_4dateofbirth_Date[0]": "petitioner_dob",
    "topmostSubform[0].Page5[0].P5_cityofbirth_FLD[0]": "petitioner_birth_city",
    "topmostSubform[0].Page5[0].P5_stateatbirth_FLD[0]": "petitioner_birth_state",
    "topmostSubform[0].Page5[0].P5_oldssnXXX_FLD[0]": "petitioner_ssn_1",
    "topmostSubform[0].Page5[0].P5_oldssnXX_FLD[0]": "petitioner_ssn_2",
    "topmostSubform[0].Page5[0].P5_oldssnXXXX_FLD[0]": "petitioner_ssn_3",
    "topmostSubform[0].Page5[0].P5_Self_CB21[0]": True,
    "topmostSubform[0].Page5[0].P5_GenderM_CB14[0]": lambda d: d.get("petitioner_gender", "").lower() == "male",
    "topmostSubform[0].Page5[0].P5_GenderF_CB15[0]": lambda d: d.get("petitioner_gender", "").lower() == "female",
}

# ---------------------------------------------------------------------------
# Master registry — maps form filename prefix to its field dict
# ---------------------------------------------------------------------------
CA_FORM_MAPPINGS = {
    "fl-100": CA_FL100,
    "fl-110": CA_FL110,
    "fl-120": CA_FL120,
    "fl-180": CA_FL180,
    "fw4":    IRS_W4,
    "f8822":  IRS_8822,
    "f8332":  IRS_8332,
    "ss-5":   SSA_SS5,
}


def resolve_value(val, user_data: dict):
    if callable(val):
        return val(user_data)
    if isinstance(val, str):
        return user_data.get(val, "")
    return val  # bool or literal


def get_ca_fields(form_filename: str, user_data: dict) -> dict:
    """
    Given a PDF filename (e.g. 'fl-100.pdf') and user data,
    returns {field_name: value} for all mapped fields.
    """
    key = form_filename.lower().replace(".pdf", "").split("_")[0]
    mapping = CA_FORM_MAPPINGS.get(key, {})
    result = {}
    for field_name, val in mapping.items():
        resolved = resolve_value(val, user_data)
        if resolved is not None and resolved != "":
            result[field_name] = resolved
    return result


# ---------------------------------------------------------------------------
# PATCH: override get_ca_fields with filename-aware lookup
# ---------------------------------------------------------------------------
_FILENAME_MAP = {
    "ca_fl100_petition":        CA_FL100,
    "ca_fl110_summons":         CA_FL110,
    "ca_fl120_response":        CA_FL120,
    "ca_fl180_judgment":        CA_FL180,
    "irs_w4_withholding":       IRS_W4,
    "irs_w4p_pension":          IRS_W4,
    "irs_8822_address_change":  IRS_8822,
    "irs_8332_child_exemption": IRS_8332,
    "ssa_ss5_name_change":      SSA_SS5,
}

def get_ca_fields(form_filename: str, user_data: dict) -> dict:
    key = form_filename.lower().replace(".pdf", "")
    mapping = _FILENAME_MAP.get(key, {})
    result = {}
    for field_name, val in mapping.items():
        resolved = resolve_value(val, user_data)
        if resolved is not None and resolved != "":
            result[field_name] = resolved
    return result
