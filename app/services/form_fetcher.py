"""
Form Fetcher Service
- Fetches official court PDFs from government URLs
- Caches raw bytes in the court_forms DB table
- Returns cached version if URL goes down (fallback)
"""

import requests
import logging
from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from app.models.db import CourtForm

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get_or_fetch_form(
    db: DBSession,
    feature: str,
    state: str,
    filename: str,
    url: str
) -> bytes | None:
    """
    Main entry point. Returns PDF bytes for a form.
    1. Check DB cache first
    2. If not cached or stale, fetch from government URL
    3. Cache result in DB
    4. If fetch fails, return cached fallback if available
    """
    # Check DB cache
    cached = db.query(CourtForm).filter(
        CourtForm.feature == feature,
        CourtForm.state == state,
        CourtForm.filename == filename
    ).first()

    if cached and cached.fetch_status == "cached" and cached.pdf_data:
        logger.info(f"Cache hit: {feature}/{state}/{filename}")
        return cached.pdf_data

    # Fetch live from government URL
    logger.info(f"Fetching live: {url}")
    pdf_bytes = _fetch_url(url)

    if pdf_bytes:
        # Save or update in DB
        if cached:
            cached.pdf_data = pdf_bytes
            cached.fetch_status = "cached"
            cached.file_size_kb = len(pdf_bytes) // 1024
            cached.last_fetched = datetime.utcnow()
        else:
            cached = CourtForm(
                feature=feature,
                state=state,
                filename=filename,
                source_url=url,
                pdf_data=pdf_bytes,
                fetch_status="cached",
                file_size_kb=len(pdf_bytes) // 1024,
                last_fetched=datetime.utcnow()
            )
            db.add(cached)
        db.commit()
        return pdf_bytes

    # Fetch failed — return stale cache if we have it
    if cached and cached.pdf_data:
        logger.warning(f"Using stale cache for: {feature}/{state}/{filename}")
        return cached.pdf_data

    # Nothing available
    logger.error(f"No PDF available for: {feature}/{state}/{filename} — {url}")
    if not cached:
        cached = CourtForm(
            feature=feature,
            state=state,
            filename=filename,
            source_url=url,
            fetch_status="failed"
        )
        db.add(cached)
        db.commit()
    return None


def _fetch_url(url: str) -> bytes | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 500:
            return resp.content
        return None
    except Exception as e:
        logger.error(f"Fetch error for {url}: {e}")
        return None


def fetch_all_forms_for_session(
    db: DBSession,
    needed_forms: dict
) -> dict:
    """
    Fetch all forms needed for a session.
    Returns: { feature: { filename: bytes } }
    """
    results = {}
    for feature, forms in needed_forms.items():
        results[feature] = {}
        for filename, url in forms:
            # Parse state from feature/filename context
            state = _infer_state(filename, url)
            pdf_bytes = get_or_fetch_form(db, feature, state, filename, url)
            if pdf_bytes:
                results[feature][filename] = pdf_bytes
            else:
                logger.warning(f"Skipping unavailable form: {filename}")
    return results


def _infer_state(filename: str, url: str) -> str:
    """Infer state from filename prefix for DB storage."""
    prefix = filename.split("_")[0].upper()
    state_map = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
        "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
        "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
        "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
        "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
        "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
        "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
        "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
        "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
        "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
        "WI": "Wisconsin", "WY": "Wyoming", "DC": "Washington DC",
        "IRS": "_FEDERAL", "SSA": "_FEDERAL", "DOL": "_FEDERAL",
        "STATE": "_FEDERAL", "DS": "_FEDERAL",
    }
    return state_map.get(prefix, "_FEDERAL")


def get_cache_stats(db: DBSession) -> dict:
    """Returns cache statistics for the admin endpoint."""
    total = db.query(CourtForm).count()
    cached = db.query(CourtForm).filter(CourtForm.fetch_status == "cached").count()
    failed = db.query(CourtForm).filter(CourtForm.fetch_status == "failed").count()
    pending = db.query(CourtForm).filter(CourtForm.fetch_status == "pending").count()
    return {
        "total_registered": total,
        "cached": cached,
        "failed": failed,
        "pending": pending,
        "cache_hit_rate": f"{round(cached/total*100, 1)}%" if total > 0 else "0%"
    }
