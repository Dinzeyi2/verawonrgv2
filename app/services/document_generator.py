"""
Document Generator
- Fetches real government PDFs via form_fetcher (cached in DB)
- Overlays user data onto forms using pypdf + reportlab
- Packages everything into a zip
"""

import os, io, zipfile, logging
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from pypdf import PdfWriter, PdfReader
from sqlalchemy.orm import Session as DBSession
from app.services.form_registry import get_forms_for_session
from app.services.form_fetcher import fetch_all_forms_for_session
from app.services.pdf_filler import fill_pdf

logger = logging.getLogger(__name__)


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=13, fontName='Helvetica-Bold',
                               spaceAfter=8, spaceBefore=16, textColor=colors.HexColor('#1a1a2e')))
    styles.add(ParagraphStyle(name='FieldValue', fontSize=10, fontName='Helvetica', spaceAfter=6))
    styles.add(ParagraphStyle(name='Note', fontSize=8, fontName='Helvetica-Oblique',
                               textColor=colors.HexColor('#888888')))
    return styles


def _overlay_text_on_pdf(pdf_bytes: bytes, fields: dict) -> bytes:
    """Overlay user data as text on top of government PDF page 1."""
    try:
        packet = io.BytesIO()
        c = rl_canvas.Canvas(packet, pagesize=letter)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(0.1, 0.1, 0.5)
        y = 750
        c.drawString(40, y, "PRE-FILLED BY LEGAL-TO-GO")
        y -= 18
        c.setFont("Helvetica", 9)
        for label, value in fields.items():
            if value and str(value).strip():
                c.drawString(40, y, f"{label}: {str(value)[:90]}")
                y -= 13
                if y < 50:
                    break
        c.save()
        packet.seek(0)
        overlay_reader = PdfReader(packet)
        base_reader = PdfReader(io.BytesIO(pdf_bytes))
        writer = PdfWriter()
        for i, page in enumerate(base_reader.pages):
            if i == 0:
                page.merge_page(overlay_reader.pages[0])
            writer.add_page(page)
        output = io.BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception as e:
        logger.error(f"PDF overlay failed: {e}")
        return pdf_bytes


def _build_cover_sheet(data: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                             rightMargin=inch, leftMargin=inch,
                             topMargin=inch, bottomMargin=inch)
    styles = _styles()
    story = []
    story.append(Paragraph("LEGAL-TO-GO", ParagraphStyle(
        name='Brand', fontSize=9, fontName='Helvetica', textColor=colors.HexColor('#aaaaaa'))))
    story.append(Paragraph("Complete Filing Packet", ParagraphStyle(
        name='Title', fontSize=22, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a1a2e'), spaceAfter=4)))
    story.append(Paragraph(f"Prepared for: {data.get('petitioner_full_name', '')}",
        ParagraphStyle(name='Sub', fontSize=12, fontName='Helvetica',
                       textColor=colors.HexColor('#555555'), spaceAfter=4)))
    story.append(Paragraph(
        f"State: {data.get('filing_state', '')} | Generated: {datetime.now().strftime('%B %d, %Y')}",
        styles['Note']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e0e0e0'), spaceAfter=16))
    story.append(Paragraph("WHAT'S IN YOUR PACKET", styles['SectionHeader']))
    included = [
        ("01", "Divorce Petition Forms", "Official state court forms pre-filled with your information"),
    ]
    if data.get("petitioner_wants_name_change"):
        included.append(("02", "Name Change Packet", "SSA SS-5, Passport DS-82/DS-11, state DMV application"))
    if data.get("has_real_property") or data.get("has_retirement_accounts") or data.get("has_joint_bank_accounts"):
        included.append(("03", "Asset Transfer Documents", "Financial affidavits, property settlement, QDRO notice"))
    if data.get("has_minor_children"):
        included.append(("04", "Co-Parenting Plan", "Parenting schedule, child support worksheet"))
    included.append(("05", "Financial Reset Guide", "IRS W-4, beneficiary checklist, COBRA notice"))
    for num, title, desc in included:
        story.append(Paragraph(f"<b>{num}. {title}</b>", styles['FieldValue']))
        story.append(Paragraph(desc, styles['Note']))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 16))
    story.append(Paragraph("NEXT STEPS", styles['SectionHeader']))
    story.append(Paragraph(
        "1. Review all documents carefully before signing.\n"
        "2. Sign where indicated on each form.\n"
        "3. File the divorce petition at your county courthouse.\n"
        "4. Bring certified divorce decree to update name change documents.\n"
        "5. Update W-4 and beneficiaries with your employer and financial institutions.",
        styles['BodyText']))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "DISCLAIMER: Legal-to-Go is a document preparation service, not a law firm. "
        "These documents do not constitute legal advice. Consult a licensed attorney for legal guidance.",
        styles['Note']))
    doc.build(story)
    return buf.getvalue()


def _build_overlays(data: dict) -> dict:
    state = data.get("filing_state", "")
    county = data.get("filing_county", "")
    petitioner = data.get("petitioner_full_name", "")
    respondent = data.get("respondent_full_name", "")
    return {
        "01_divorce": {
            "Petitioner": petitioner,
            "Respondent": respondent,
            "Date of Marriage": data.get("marriage_date", ""),
            "Date of Separation": data.get("separation_date", ""),
            "Filing County": county,
            "Filing State": state,
            "Petitioner DOB": data.get("petitioner_dob", ""),
            "Petitioner Address": f"{data.get('petitioner_address','')} {data.get('petitioner_city','')} {state} {data.get('petitioner_zip','')}",
            "Respondent DOB": data.get("respondent_dob", ""),
            "Minor Children": "Yes" if data.get("has_minor_children") else "No",
            "Custody Type": data.get("custody_type", "").replace("_", " ").title(),
            "Child Support": f"${data.get('child_support_amount', '')} / month",
        },
        "02_name_change": {
            "Current Legal Name": petitioner,
            "New Name After Divorce": data.get("new_name_after_divorce", ""),
            "Date of Birth": data.get("petitioner_dob", ""),
            "Filing State": state,
            "Email": data.get("petitioner_email", ""),
            "Phone": data.get("petitioner_phone", ""),
        },
        "03_asset": {
            "Petitioner": petitioner,
            "Respondent": respondent,
            "Real Property": data.get("real_property_address", ""),
            "Property Disposition": data.get("real_property_disposition", "").replace("_", " ").title(),
            "Alimony Amount": f"${data.get('alimony_amount', '')}",
            "Alimony Duration": data.get("alimony_duration", ""),
            "Filing County": county,
            "Filing State": state,
        },
        "04_coparenting": {
            "Petitioner": petitioner,
            "Respondent": respondent,
            "Custody Type": data.get("custody_type", "").replace("_", " ").title(),
            "Child Support": f"${data.get('child_support_amount', '')} / month",
            "Payor": data.get("child_support_payor", ""),
            "Schedule": data.get("parenting_schedule_description", ""),
            "Filing County": county,
        },
        "05_financial": {
            "Petitioner": petitioner,
            "New Filing Status": "Head of Household" if data.get("has_minor_children") else "Single",
            "Alimony": f"${data.get('alimony_amount', '')} / month" if data.get("alimony_requested") else "None",
            "Child Support": f"${data.get('child_support_amount', '')} / month" if data.get("has_minor_children") else "None",
            "Filing State": state,
        },
    }


def generate_full_packet(session_id: str, data: dict, db: DBSession) -> str:
    """
    Main entry point.
    1. Determine which forms are needed
    2. Fetch from DB cache or live government URLs
    3. Overlay user data onto each PDF
    4. Zip everything and return path
    """
    state = data.get("filing_state", "")
    has_children = bool(data.get("has_minor_children"))
    wants_name_change = bool(data.get("petitioner_wants_name_change"))
    has_assets = bool(
        data.get("has_real_property") or
        data.get("has_retirement_accounts") or
        data.get("has_joint_bank_accounts")
    )

    needed_forms = get_forms_for_session(state, has_children, wants_name_change, has_assets)
    fetched_forms = fetch_all_forms_for_session(db, needed_forms)
    overlays = _build_overlays(data)

    name = data.get("petitioner_full_name", "user").replace(" ", "_")
    zip_dir = f"/tmp/packets/{session_id}"
    os.makedirs(zip_dir, exist_ok=True)
    zip_path = f"{zip_dir}/LegalToGo_Complete_Packet_{name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("00_Cover_Sheet.pdf", _build_cover_sheet(data))
        for feature, forms in fetched_forms.items():
            feature_overlay = overlays.get(feature, {})
            for filename, pdf_bytes in forms.items():
                modified = fill_pdf(pdf_bytes, feature_overlay)
                zipf.writestr(f"{feature}/{filename}", modified)

    logger.info(f"Packet generated: {zip_path}")
    return zip_path
