"""
Smart PDF Filler
- Detects if PDF has fillable form fields
- If yes: fills them directly using pypdf
- If no: overlays text annotations at correct positions using reportlab
- Falls back gracefully if anything fails
"""

import io
import logging
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, ArrayObject, DictionaryObject, TextStringObject
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter

logger = logging.getLogger(__name__)


def fill_pdf(pdf_bytes: bytes, fields: dict) -> bytes:
    """
    Main entry point.
    fields: { "label": "value" }
    Returns filled PDF bytes.
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        form_fields = _get_form_fields(reader)

        if form_fields:
            logger.info(f"PDF has {len(form_fields)} fillable fields — using field filling")
            return _fill_form_fields(pdf_bytes, fields, form_fields)
        else:
            logger.info("PDF has no fillable fields — using annotation overlay")
            return _fill_with_annotations(pdf_bytes, fields)

    except Exception as e:
        logger.error(f"PDF fill failed: {e}")
        return pdf_bytes


def _get_form_fields(reader: PdfReader) -> dict:
    """Returns dict of {field_name: field_obj} if PDF has AcroForm fields."""
    try:
        if "/AcroForm" not in reader.trailer["/Root"]:
            return {}
        fields = reader.get_fields()
        return fields if fields else {}
    except Exception:
        return {}


def _fill_form_fields(pdf_bytes: bytes, data: dict, form_fields: dict) -> bytes:
    """
    Fill actual AcroForm fields by matching field names to user data.
    Uses fuzzy matching to map our data keys to PDF field names.
    """
    writer = PdfWriter()
    reader = PdfReader(io.BytesIO(pdf_bytes))

    for page in reader.pages:
        writer.add_page(page)

    writer.clone_reader_document_root(reader)

    # Build field mapping: normalize both sides and match
    fill_data = {}
    for field_name in form_fields.keys():
        normalized = _normalize(field_name)
        matched_value = _find_best_match(normalized, data)
        if matched_value:
            fill_data[field_name] = matched_value

    if fill_data:
        writer.update_page_form_field_values(writer.pages[0], fill_data)

    # Need appearance streams so values show visually
    if "/AcroForm" in writer._root_object:
        writer._root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(True)

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def _fill_with_annotations(pdf_bytes: bytes, data: dict) -> bytes:
    """
    For non-fillable PDFs: place text annotations on the page.
    Tries to position text intelligently based on common form layouts.
    """
    try:
        # Create annotation layer
        packet = io.BytesIO()
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page = reader.pages[0]

        # Get page dimensions
        media_box = page.mediabox
        page_width = float(media_box.width)
        page_height = float(media_box.height)

        c = rl_canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Header banner
        c.setFillColorRGB(0.0, 0.2, 0.6, alpha=0.85)
        c.rect(0, page_height - 28, page_width, 28, fill=True, stroke=False)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10, page_height - 18, "PRE-FILLED BY LEGAL-TO-GO — Review before signing")

        # Place fields in two columns
        c.setFillColorRGB(0.05, 0.05, 0.4)
        c.setFont("Helvetica", 8)

        items = [(k, v) for k, v in data.items() if v and str(v).strip()]
        col_width = page_width / 2 - 20
        col1_x = 15
        col2_x = page_width / 2 + 10
        y = page_height - 45
        line_h = 16

        for i, (label, value) in enumerate(items):
            x = col1_x if i % 2 == 0 else col2_x
            if i % 2 == 0 and i > 0:
                y -= line_h
            if y < 40:
                break

            # Label
            c.setFont("Helvetica-Bold", 7)
            c.setFillColorRGB(0.3, 0.3, 0.6)
            c.drawString(x, y + 5, f"{label}:")

            # Value
            c.setFont("Helvetica", 8)
            c.setFillColorRGB(0.05, 0.05, 0.05)
            val_str = str(value)[:55]
            c.drawString(x, y - 4, val_str)

            # Underline
            c.setStrokeColorRGB(0.7, 0.7, 0.9)
            c.line(x, y - 6, x + col_width, y - 6)

        c.save()
        packet.seek(0)

        # Merge annotation layer onto each page
        overlay_reader = PdfReader(packet)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == 0:
                page.merge_page(overlay_reader.pages[0])
            writer.add_page(page)

        output = io.BytesIO()
        writer.write(output)
        return output.getvalue()

    except Exception as e:
        logger.error(f"Annotation overlay failed: {e}")
        return pdf_bytes


def _normalize(text: str) -> str:
    """Normalize field name for matching."""
    return text.lower().replace("_", " ").replace("-", " ").replace(".", " ").strip()


def _find_best_match(field_name: str, data: dict) -> str | None:
    """
    Find best matching value from user data for a given PDF field name.
    Uses keyword matching for common legal form fields.
    """
    field_lower = field_name.lower()

    # Direct keyword matching map
    KEYWORD_MAP = [
        (["petitioner", "plaintiff", "your name", "full name", "applicant name"], "Petitioner"),
        (["respondent", "defendant", "spouse", "other party"], "Respondent"),
        (["date of marriage", "marriage date", "wed"], "Date of Marriage"),
        (["separation", "date of separation"], "Date of Separation"),
        (["county", "filing county"], "Filing County"),
        (["state", "filing state"], "Filing State"),
        (["dob", "date of birth", "birth date", "petitioner dob"], "Petitioner DOB"),
        (["address", "street", "residence"], "Petitioner Address"),
        (["city", "zip", "postal"], "Petitioner Address"),
        (["child", "minor", "children"], "Minor Children"),
        (["custody"], "Custody Type"),
        (["child support", "support amount"], "Child Support"),
        (["new name", "name after", "name change", "restored name"], "New Name After Divorce"),
        (["current name", "present name"], "Current Legal Name"),
        (["property", "real estate", "real property"], "Real Property"),
        (["alimony", "spousal support", "maintenance"], "Alimony Amount"),
        (["filing status", "tax status"], "New Filing Status"),
        (["email", "e-mail"], "Email"),
        (["phone", "telephone", "tel"], "Phone"),
    ]

    for keywords, data_key in KEYWORD_MAP:
        if any(kw in field_lower for kw in keywords):
            # Find matching key in data
            for dk, dv in data.items():
                if _normalize(dk) == _normalize(data_key) and dv:
                    return str(dv)

    return None
