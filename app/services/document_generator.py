"""
Document Generator
1. Determines which forms are needed (based on state/children/assets/name change)
2. Fetches real government PDFs via form_fetcher (cached in DB)
3. Fills each PDF with user data (CA: AcroForm fields, NY: coordinate stamps)
4. Packages everything into a zip for download
"""

import os, io, zipfile, logging
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from sqlalchemy.orm import Session as DBSession

from app.services.form_registry import get_forms_for_session
from app.services.form_fetcher import fetch_all_forms_for_session
from app.services.pdf_filler import fill_form

logger = logging.getLogger(__name__)


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Brand',  fontSize=9,  fontName='Helvetica',
                               textColor=colors.HexColor('#aaaaaa')))
    styles.add(ParagraphStyle(name='Title',  fontSize=22, fontName='Helvetica-Bold',
                               textColor=colors.HexColor('#1a1a2e'), spaceAfter=4))
    styles.add(ParagraphStyle(name='Sub',    fontSize=12, fontName='Helvetica',
                               textColor=colors.HexColor('#555555'), spaceAfter=4))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=13, fontName='Helvetica-Bold',
                               spaceAfter=8, spaceBefore=16, textColor=colors.HexColor('#1a1a2e')))
    styles.add(ParagraphStyle(name='FieldValue', fontSize=10, fontName='Helvetica', spaceAfter=6))
    styles.add(ParagraphStyle(name='Note',   fontSize=8,  fontName='Helvetica-Oblique',
                               textColor=colors.HexColor('#888888')))
    return styles


def _build_cover_sheet(data: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                             rightMargin=inch, leftMargin=inch,
                             topMargin=inch, bottomMargin=inch)
    styles = _styles()
    story = []

    story.append(Paragraph("LEGAL-TO-GO", styles['Brand']))
    story.append(Paragraph("Complete Filing Packet", styles['Title']))
    story.append(Paragraph(
        f"Prepared for: {data.get('petitioner_name', '')}",
        styles['Sub']))
    story.append(Paragraph(
        f"State: {data.get('filing_state', '')} &nbsp;|&nbsp; Generated: {datetime.now().strftime('%B %d, %Y')}",
        styles['Note']))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#e0e0e0'), spaceAfter=16))

    story.append(Paragraph("WHAT'S IN YOUR PACKET", styles['SectionHeader']))

    sections = [("01", "Divorce Petition Forms",
                 "Official state court forms pre-filled with your information")]
    if data.get("wants_name_change") or data.get("petitioner_wants_name_change"):
        sections.append(("02", "Name Change Packet",
                          "SSA SS-5, Passport DS-82/DS-11, state DMV application"))
    if data.get("has_assets") or data.get("has_real_property") or data.get("has_retirement_accounts"):
        sections.append(("03", "Asset Transfer Documents",
                          "Financial affidavits, property settlement, QDRO notice"))
    if data.get("has_children") or data.get("has_minor_children"):
        sections.append(("04", "Co-Parenting Plan",
                          "Parenting schedule, child support worksheet"))
    sections.append(("05", "Financial Reset Guide",
                     "IRS W-4, beneficiary checklist, COBRA notice"))

    for num, title, desc in sections:
        story.append(Paragraph(f"<b>{num}. {title}</b>", styles['FieldValue']))
        story.append(Paragraph(desc, styles['Note']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 16))
    story.append(Paragraph("NEXT STEPS", styles['SectionHeader']))
    story.append(Paragraph(
        "1. Review all documents carefully before signing.<br/>"
        "2. Sign where indicated (look for signature lines).<br/>"
        "3. File the divorce petition at your county courthouse.<br/>"
        "4. Bring certified divorce decree to update name change documents.<br/>"
        "5. Update your W-4 and beneficiaries with your employer.",
        styles['FieldValue']))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "DISCLAIMER: Legal-to-Go is a document preparation service, not a law firm. "
        "These documents do not constitute legal advice. Consult a licensed attorney for legal guidance.",
        styles['Note']))

    doc.build(story)
    return buf.getvalue()


def _normalize(data: dict) -> dict:
    """Reconcile interview field names to what the mapping files expect."""
    d = dict(data)

    if "petitioner_full_name" in d and "petitioner_name" not in d:
        d["petitioner_name"] = d["petitioner_full_name"]
    if "respondent_full_name" in d and "respondent_name" not in d:
        d["respondent_name"] = d["respondent_full_name"]

    if "petitioner_name" in d and "petitioner_first" not in d:
        parts = d["petitioner_name"].split()
        d["petitioner_first"] = parts[0] if parts else ""
        d["petitioner_last"]  = parts[-1] if len(parts) > 1 else ""

    if "respondent_name" in d and "respondent_first" not in d:
        parts = d["respondent_name"].split()
        d["respondent_first"] = parts[0] if parts else ""
        d["respondent_last"]  = parts[-1] if len(parts) > 1 else ""

    if "has_minor_children" in d and "has_children" not in d:
        d["has_children"] = d["has_minor_children"]
    if "petitioner_wants_name_change" in d and "wants_name_change" not in d:
        d["wants_name_change"] = d["petitioner_wants_name_change"]

    if "new_name_after_divorce" in d and "new_name_last" not in d:
        parts = d["new_name_after_divorce"].split()
        d["new_name_first"] = parts[0] if parts else ""
        d["new_name_last"]  = parts[-1] if len(parts) > 1 else ""

    if "marriage_date" in d and "date_of_marriage" not in d:
        d["date_of_marriage"] = d["marriage_date"]
    if "separation_date" in d and "date_of_separation" not in d:
        d["date_of_separation"] = d["separation_date"]

    if "filing_state" in d:
        d["filing_state"] = d["filing_state"].upper()

    return d


def generate_full_packet(session_id: str, data: dict, db: DBSession) -> str:
    """
    Main entry point called by the /api/documents/generate endpoint.
    Returns the path to the generated zip file.
    """
    data = _normalize(data)

    state             = data.get("filing_state", "")
    has_children      = bool(data.get("has_children") or data.get("has_minor_children"))
    wants_name_change = bool(data.get("wants_name_change") or data.get("petitioner_wants_name_change"))
    has_assets        = bool(
        data.get("has_assets") or
        data.get("has_real_property") or
        data.get("has_retirement_accounts") or
        data.get("has_joint_bank_accounts")
    )

    needed_forms  = get_forms_for_session(state, has_children, wants_name_change, has_assets)
    fetched_forms = fetch_all_forms_for_session(db, needed_forms)

    petitioner_name = data.get("petitioner_name", "user").replace(" ", "_")
    zip_dir  = f"/tmp/packets/{session_id}"
    os.makedirs(zip_dir, exist_ok=True)
    zip_path = f"{zip_dir}/LegalToGo_{petitioner_name}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("00_Cover_Sheet.pdf", _build_cover_sheet(data))

        for feature, forms in fetched_forms.items():
            for filename, pdf_bytes in forms.items():
                try:
                    filled = fill_form(pdf_bytes, filename, data)
                except Exception as e:
                    logger.error(f"fill_form failed for {filename}: {e}")
                    filled = pdf_bytes
                zipf.writestr(f"{feature}/{filename}", filled)

    logger.info(f"Packet generated: {zip_path}")
    return zip_path
