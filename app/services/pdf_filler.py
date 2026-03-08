"""
PDF FILLER
- CA forms: fillable AcroForm fields via pypdf
- NY forms: coordinate-based text stamps via pymupdf (fitz)
- Federal (IRS/SSA): fillable AcroForm fields via pypdf
"""

import io
import logging
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, ArrayObject, DictionaryObject

logger = logging.getLogger(__name__)

# Lazy import fitz only when needed (NY forms)
_fitz = None

def _get_fitz():
    global _fitz
    if _fitz is None:
        try:
            import fitz
            _fitz = fitz
        except ImportError:
            raise RuntimeError("pymupdf not installed. Add 'pymupdf' to requirements.txt")
    return _fitz


# ─────────────────────────────────────────────────────────────────────────────
# CA / FEDERAL: Fill AcroForm fillable PDFs
# ─────────────────────────────────────────────────────────────────────────────

def _fill_acroform(pdf_bytes: bytes, fields: dict) -> bytes:
    """
    Fill a fillable PDF's AcroForm fields.
    fields: {exact_field_name: value}  (value can be str, bool, or int)
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    writer.clone_reader_document_root(reader)

    # Try pypdf's built-in field writer first
    try:
        str_fields = {k: str(v) if not isinstance(v, bool) else v
                      for k, v in fields.items()}
        writer.update_page_form_field_values(
            writer.pages[0] if len(writer.pages) == 1 else None,
            str_fields
        )
    except Exception:
        pass

    # Walk all annotations across all pages and set values directly
    for page in writer.pages:
        if "/Annots" not in page:
            continue
        for annot_ref in page["/Annots"]:
            try:
                annot = annot_ref.get_object()
                if annot.get("/Subtype") != "/Widget":
                    continue
                field_name = annot.get("/T")
                if field_name is None:
                    continue
                full_name = str(field_name)
                # Try full qualified name match first, then short name
                value = fields.get(full_name)
                if value is None:
                    short = full_name.split(".")[-1]
                    value = fields.get(short)
                if value is None:
                    continue

                field_type = annot.get("/FT")
                if field_type == "/Tx":
                    annot.update({NameObject("/V"): annot.pdf.PdfObject.from_value(str(value))})
                    if "/AP" in annot:
                        del annot["/AP"]
                elif field_type == "/Btn":
                    if bool(value):
                        annot.update({NameObject("/V"): NameObject("/Yes"),
                                      NameObject("/AS"): NameObject("/Yes")})
                    else:
                        annot.update({NameObject("/V"): NameObject("/Off"),
                                      NameObject("/AS"): NameObject("/Off")})
                elif field_type == "/Ch":
                    annot.update({NameObject("/V"): annot.pdf.PdfObject.from_value(str(value))})
            except Exception as e:
                logger.debug(f"Field fill error: {e}")
                continue

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def fill_ca_form(pdf_bytes: bytes, form_filename: str, user_data: dict) -> bytes:
    """Fill a CA or federal fillable PDF form."""
    try:
        from app.services.ca_field_mappings import get_ca_fields
        fields = get_ca_fields(form_filename, user_data)
        if not fields:
            logger.warning(f"No field mapping found for {form_filename}")
            return pdf_bytes
        return _fill_acroform(pdf_bytes, fields)
    except Exception as e:
        logger.error(f"CA form fill failed for {form_filename}: {e}")
        return pdf_bytes


# ─────────────────────────────────────────────────────────────────────────────
# NY: Stamp text onto flat PDFs at exact coordinates
# ─────────────────────────────────────────────────────────────────────────────

def fill_ny_form(pdf_bytes: bytes, form_filename: str, user_data: dict) -> bytes:
    """Stamp user data onto a flat NY PDF using coordinate overlays."""
    try:
        from app.services.ny_field_mappings import get_ny_overlays
        overlays = get_ny_overlays(form_filename, user_data)
        if not overlays:
            logger.warning(f"No overlay mapping found for {form_filename}")
            return pdf_bytes

        fitz = _get_fitz()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for overlay in overlays:
            text = overlay.get("text", "")
            if not text or not str(text).strip():
                continue
            page_num = overlay.get("page", 0)
            if page_num >= len(doc):
                continue
            page = doc[page_num]
            page.insert_text(
                fitz.Point(overlay["x"], overlay["y"]),
                str(text),
                fontsize=overlay.get("size", 10),
                color=(0, 0, 0),
            )

        output = io.BytesIO()
        doc.save(output)
        doc.close()
        return output.getvalue()

    except Exception as e:
        logger.error(f"NY form stamp failed for {form_filename}: {e}")
        return pdf_bytes


# ─────────────────────────────────────────────────────────────────────────────
# Router: pick the right filler based on state + filename
# ─────────────────────────────────────────────────────────────────────────────

def fill_form(pdf_bytes: bytes, form_filename: str, user_data: dict) -> bytes:
    """
    Main entry point.
    Routes to the correct filler based on state and filename.
    
    Args:
        pdf_bytes:     Raw bytes of the government PDF
        form_filename: Filename like 'fl-100.pdf', 'ud-2.pdf', 'fw4.pdf'
        user_data:     Dict of user interview answers

    Returns:
        Filled PDF bytes
    """
    name = form_filename.lower()
    state = user_data.get("filing_state", "").upper()

    # NY forms (UD-*)
    if name.startswith("ud-") or state == "NY":
        return fill_ny_form(pdf_bytes, form_filename, user_data)

    # CA forms (FL-*) and federal forms (IRS, SSA)
    return fill_ca_form(pdf_bytes, form_filename, user_data)
