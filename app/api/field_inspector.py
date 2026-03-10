"""
Field Inspector — add this as a router in main.py for one-time use.
Fetches each PDF and returns ALL AcroForm field names with their types.
Use this to fix ca_field_mappings.py with real field names.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.database import get_db
from app.services.form_registry import FORM_REGISTRY
import requests
from pypdf import PdfReader
import io

router = APIRouter()

@router.get("/inspect/{state}/{feature}")
def inspect_fields(state: str, feature: str, db: DBSession = Depends(get_db)):
    """
    GET /api/inspect/California/01_divorce
    Returns all AcroForm fields for every form in that feature/state combo.
    """
    feature_forms = FORM_REGISTRY.get(feature, {})
    forms = feature_forms.get(state, []) + feature_forms.get("_FEDERAL", [])

    results = {}
    for filename, url in forms:
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                results[filename] = {"error": f"HTTP {resp.status_code}"}
                continue

            reader = PdfReader(io.BytesIO(resp.content))
            fields = reader.get_fields()

            if fields:
                results[filename] = {
                    "type": "fillable",
                    "field_count": len(fields),
                    "fields": {
                        name: {
                            "type": str(field.get("/FT", "unknown")),
                            "label": str(field.get("/TU", field.get("/T", name))),
                            "value": str(field.get("/V", ""))
                        }
                        for name, field in fields.items()
                    }
                }
            else:
                results[filename] = {"type": "flat_pdf", "fields": None}

        except Exception as e:
            results[filename] = {"error": str(e)}

    return results


@router.get("/inspect-url")
def inspect_url(url: str):
    """
    GET /api/inspect-url?url=https://...
    Inspect any single PDF by URL.
    """
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        reader = PdfReader(io.BytesIO(resp.content))
        fields = reader.get_fields()

        if not fields:
            return {"type": "flat_pdf", "pages": len(reader.pages)}

        return {
            "type": "fillable",
            "field_count": len(fields),
            "fields": {
                name: {
                    "type": str(field.get("/FT", "unknown")),
                    "label": str(field.get("/TU", field.get("/T", name))),
                }
                for name, field in fields.items()
            }
        }
    except Exception as e:
        return {"error": str(e)}
