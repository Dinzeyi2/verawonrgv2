"""
NY FLAT FORM COORDINATE MAPPINGS
NY forms are non-fillable PDFs — we stamp text at exact (x, y) coordinates.
Coordinate system: (0,0) = top-left of page, letter size = 612 x 792 pt.
"""


def _v(d, key, default=""):
    return str(d.get(key, default)) if d.get(key) else default


def _child(d, idx, field):
    children = d.get("children", [])
    if idx < len(children):
        return str(children[idx].get(field, ""))
    return ""


# ── UD-2: Verified Complaint ────────────────────────────────────────────────
def _ud2(d):
    children = d.get("children", [])
    overlays = [
        {"page": 0, "x": 200, "y": 83,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 465, "y": 116, "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 116, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 199, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 205, "y": 246, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 388, "y": 637, "text": _v(d, "date_of_marriage"), "size": 10},
        {"page": 0, "x": 294, "y": 659, "text": _v(d, "marriage_city_state"), "size": 10},
        {"page": 1, "x": 247, "y": 227, "text": str(len(children)) if children else "0", "size": 10},
        {"page": 1, "x": 220, "y": 373, "text": f"{_v(d,'petitioner_address')}, {_v(d,'petitioner_city')} {_v(d,'petitioner_state')}", "size": 9},
        {"page": 1, "x": 220, "y": 387, "text": _v(d, "respondent_address"), "size": 9},
    ]
    for i, cy in enumerate([283, 297, 311, 325]):
        if i < len(children):
            overlays += [
                {"page": 1, "x": 72,  "y": cy, "text": _child(d, i, "name"), "size": 9},
                {"page": 1, "x": 243, "y": cy, "text": _child(d, i, "birthdate"), "size": 9},
                {"page": 1, "x": 330, "y": cy, "text": _child(d, i, "address") or _v(d, "petitioner_address"), "size": 9},
            ]
    overlays.append({"page": 4, "x": 72, "y": 400, "text": _v(d, "petitioner_name"), "size": 10})
    return overlays


# ── UD-3: Affirmation of Service ─────────────────────────────────────────────
def _ud3(d):
    return [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 200, "y": 202, "text": _v(d, "server_name", "[SERVER NAME]"), "size": 10},
        {"page": 0, "x": 200, "y": 310, "text": _v(d, "service_date"), "size": 10},
        {"page": 0, "x": 300, "y": 360, "text": _v(d, "respondent_name"), "size": 10},
    ]


# ── UD-4: Barriers to Remarriage ─────────────────────────────────────────────
def _ud4(d):
    return [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 200, "y": 195, "text": "New York", "size": 10},
        {"page": 0, "x": 200, "y": 208, "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 72,  "y": 230, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 200, "y": 290, "text": _v(d, "petitioner_name"), "size": 10},
    ]


# ── UD-6: Sworn Affidavit of Plaintiff ───────────────────────────────────────
def _ud6(d):
    children = d.get("children", [])
    overlays = [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 200, "y": 260, "text": f"{_v(d,'petitioner_address')}, {_v(d,'petitioner_city')} NY {_v(d,'petitioner_zip')}", "size": 9},
        {"page": 0, "x": 310, "y": 260, "text": f"{_v(d,'petitioner_ssn_1')}-{_v(d,'petitioner_ssn_2')}-{_v(d,'petitioner_ssn_3')}", "size": 9},
        {"page": 0, "x": 200, "y": 273, "text": _v(d, "respondent_address"), "size": 9},
        {"page": 1, "x": 140, "y": 100, "text": _v(d, "date_of_marriage"), "size": 10},
        {"page": 1, "x": 250, "y": 100, "text": _v(d, "marriage_city"), "size": 10},
        {"page": 1, "x": 350, "y": 100, "text": _v(d, "marriage_county"), "size": 10},
        {"page": 1, "x": 430, "y": 100, "text": _v(d, "marriage_state"), "size": 10},
        {"page": 1, "x": 130, "y": 160, "text": str(len(children)) if children else "0", "size": 10},
    ]
    for i, cy in enumerate([190, 204, 218, 232, 246]):
        if i < len(children):
            overlays += [
                {"page": 1, "x": 72,  "y": cy, "text": f"{_child(d,i,'name')}  SSN: {_child(d,i,'ssn')}", "size": 9},
                {"page": 1, "x": 360, "y": cy, "text": _child(d, i, "birthdate"), "size": 9},
            ]
    return overlays


# ── UD-7: Affirmation of Defendant ───────────────────────────────────────────
def _ud7(d):
    return [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 200, "y": 238, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 200, "y": 252, "text": f"{_v(d,'respondent_address')}, {_v(d,'respondent_city')} NY", "size": 9},
        {"page": 3, "x": 200, "y": 490, "text": _v(d, "respondent_name"), "size": 10},
    ]


# ── UD-9: Note of Issue ──────────────────────────────────────────────────────
def _ud9(d):
    return [
        {"page": 0, "x": 200, "y": 56,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 84,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 98,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 175, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 0, "x": 260, "y": 322, "text": _v(d, "summons_filed_date"), "size": 10},
        {"page": 0, "x": 260, "y": 336, "text": _v(d, "service_date"), "size": 10},
        {"page": 0, "x": 200, "y": 490, "text": _v(d, "petitioner_address"), "size": 9},
        {"page": 0, "x": 200, "y": 510, "text": _v(d, "petitioner_phone"), "size": 9},
    ]


# ── UD-10: Findings of Fact ──────────────────────────────────────────────────
def _ud10(d):
    children = d.get("children", [])
    overlays = [
        {"page": 0, "x": 200, "y": 56,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 84,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 98,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 175, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 1, "x": 270, "y": 236, "text": _v(d, "date_of_marriage"), "size": 10},
        {"page": 1, "x": 370, "y": 236, "text": _v(d, "marriage_city"), "size": 10},
        {"page": 1, "x": 180, "y": 250, "text": _v(d, "marriage_county"), "size": 10},
        {"page": 1, "x": 310, "y": 250, "text": _v(d, "marriage_state"), "size": 10},
        {"page": 1, "x": 400, "y": 335, "text": _v(d, "action_date"), "size": 10},
        {"page": 2, "x": 130, "y": 72,  "text": str(len(children)) if children else "0", "size": 10},
    ]
    for i, cy in enumerate([130, 144, 158, 172, 186]):
        if i < len(children):
            overlays += [
                {"page": 2, "x": 72,  "y": cy, "text": f"{_child(d,i,'name')}  {_child(d,i,'ssn')}", "size": 9},
                {"page": 2, "x": 310, "y": cy, "text": _child(d, i, "birthdate"), "size": 9},
            ]
    overlays += [
        {"page": 10, "x": 200, "y": 108, "text": _v(d, "petitioner_address"), "size": 9},
        {"page": 10, "x": 380, "y": 108, "text": f"{_v(d,'petitioner_ssn_1')}-{_v(d,'petitioner_ssn_2')}-{_v(d,'petitioner_ssn_3')}", "size": 9},
        {"page": 10, "x": 200, "y": 122, "text": _v(d, "respondent_address"), "size": 9},
    ]
    if d.get("wants_name_change"):
        overlays.append({"page": 11, "x": 300, "y": 108, "text": f"{_v(d,'new_name_first')} {_v(d,'new_name_last')}", "size": 10})
    return overlays


# ── UD-11: Judgment of Divorce ───────────────────────────────────────────────
def _ud11(d):
    children = d.get("children", [])
    overlays = [
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "courthouse"), "size": 10},
        {"page": 0, "x": 350, "y": 70,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 72,  "y": 105, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 350, "y": 120, "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 180, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 1, "x": 200, "y": 340, "text": _v(d, "petitioner_address"), "size": 9},
        {"page": 1, "x": 200, "y": 354, "text": f"{_v(d,'petitioner_ssn_1')}-{_v(d,'petitioner_ssn_2')}-{_v(d,'petitioner_ssn_3')}", "size": 9},
        {"page": 1, "x": 360, "y": 354, "text": _v(d, "respondent_address"), "size": 9},
        {"page": 2, "x": 360, "y": 148, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 2, "x": 200, "y": 162, "text": _v(d, "respondent_name"), "size": 10},
    ]
    for i, cy in enumerate([190, 208, 226, 244]):
        if i < len(children):
            overlays += [
                {"page": 3, "x": 72,  "y": cy, "text": _child(d, i, "name"), "size": 9},
                {"page": 3, "x": 270, "y": cy, "text": _child(d, i, "birthdate"), "size": 9},
                {"page": 3, "x": 395, "y": cy, "text": _child(d, i, "ssn"), "size": 9},
            ]
    if d.get("wants_name_change"):
        overlays.append({"page": 8, "x": 360, "y": 225, "text": f"{_v(d,'new_name_first')} {_v(d,'new_name_last')}", "size": 10})
    return overlays


# ── UD-13: RJI ───────────────────────────────────────────────────────────────
def _ud13(d):
    return [
        {"page": 0, "x": 200, "y": 56,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 200, "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 310, "y": 245, "text": _v(d, "petitioner_first"), "size": 9},
        {"page": 0, "x": 460, "y": 245, "text": _v(d, "petitioner_last"), "size": 9},
        {"page": 0, "x": 310, "y": 270, "text": _v(d, "petitioner_address"), "size": 9},
        {"page": 0, "x": 460, "y": 270, "text": _v(d, "petitioner_city"), "size": 9},
        {"page": 0, "x": 550, "y": 270, "text": _v(d, "petitioner_zip"), "size": 9},
        {"page": 0, "x": 310, "y": 283, "text": _v(d, "petitioner_phone"), "size": 9},
        {"page": 0, "x": 400, "y": 283, "text": _v(d, "petitioner_email"), "size": 9},
        {"page": 0, "x": 310, "y": 340, "text": _v(d, "respondent_first"), "size": 9},
        {"page": 0, "x": 460, "y": 340, "text": _v(d, "respondent_last"), "size": 9},
        {"page": 0, "x": 310, "y": 366, "text": _v(d, "respondent_address"), "size": 9},
        {"page": 0, "x": 460, "y": 366, "text": _v(d, "respondent_city"), "size": 9},
        {"page": 0, "x": 550, "y": 366, "text": _v(d, "respondent_zip"), "size": 9},
    ]


# ── UD-8(1): Annual Income Worksheet ─────────────────────────────────────────
def _ud8_1(d):
    return [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 1, "x": 390, "y": 180, "text": str(d.get("petitioner_income", "")), "size": 10},
        {"page": 1, "x": 500, "y": 180, "text": str(d.get("respondent_income", "")), "size": 10},
    ]


# ── UD-8(2): Maintenance Worksheet ───────────────────────────────────────────
def _ud8_2(d):
    p_income = d.get("petitioner_income", 0) or 0
    r_income = d.get("respondent_income", 0) or 0
    return [
        {"page": 0, "x": 200, "y": 27,  "text": _v(d, "county"), "size": 10},
        {"page": 0, "x": 350, "y": 56,  "text": _v(d, "index_no"), "size": 9},
        {"page": 0, "x": 72,  "y": 70,  "text": _v(d, "petitioner_name"), "size": 10},
        {"page": 0, "x": 72,  "y": 130, "text": _v(d, "respondent_name"), "size": 10},
        {"page": 1, "x": 390, "y": 195, "text": str(p_income) if p_income else "", "size": 10},
        {"page": 1, "x": 390, "y": 210, "text": str(r_income) if r_income else "", "size": 10},
        {"page": 1, "x": 390, "y": 265, "text": str(max(p_income, r_income)) if p_income or r_income else "", "size": 10},
        {"page": 1, "x": 390, "y": 280, "text": str(min(p_income, r_income)) if p_income or r_income else "", "size": 10},
        {"page": 1, "x": 200, "y": 370, "text": _v(d, "date_of_marriage"), "size": 10},
        {"page": 1, "x": 350, "y": 370, "text": _v(d, "action_date"), "size": 10},
    ]


# ── Master registry ───────────────────────────────────────────────────────────
NY_FORM_OVERLAYS = {
    "ud-2":    _ud2,
    "ud-3":    _ud3,
    "ud-4":    _ud4,
    "ud-6":    _ud6,
    "ud-7":    _ud7,
    "ud-9":    _ud9,
    "ud-10":   _ud10,
    "ud-11":   _ud11,
    "ud-13":   _ud13,
    "ud-8_1":  _ud8_1,
    "ud-8_2":  _ud8_2,
}


def get_ny_overlays(form_filename: str, user_data: dict) -> list:
    """
    Given a PDF filename (e.g. 'ud-2.pdf') and user data,
    returns list of {page, x, y, text, size} overlay dicts.
    """
    # Normalize: 'UD-2.pdf' → 'ud-2'
    key = form_filename.lower().replace(".pdf", "")
    fn = NY_FORM_OVERLAYS.get(key)
    if not fn:
        return []
    return fn(user_data)
