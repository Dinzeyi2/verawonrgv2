from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from app.core.database import get_db, SessionLocal
from app.models.db import Session, GeneratedPacket
from app.services.form_fetcher import get_cache_stats
import os

router = APIRouter()


async def _generate_and_save(session_id: str, data: dict):
    db = SessionLocal()
    try:
        zip_path = generate_full_packet(session_id, data, db)
        session = db.query(Session).filter(Session.id == session_id).first()
        if session:
            session.packet_path = zip_path
            session.stage = "complete"
            packet = GeneratedPacket(
                session_id=session_id,
                file_path=zip_path,
                document_types=list(data.keys())
            )
            db.add(packet)
            db.commit()
    except Exception as e:
        print(f"Generation error for {session_id}: {e}")
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if session:
                session.stage = "error"
                db.commit()
        except Exception:
            pass
    finally:
        db.close()


class GenerateRequest(BaseModel):
    session_id: str


@router.post("/generate")
async def generate_packet(
    body: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: DBSession = Depends(get_db)
):
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.packet_path and os.path.exists(session.packet_path):
        return {"status": "ready", "message": "Packet already generated"}
    session.stage = "generating"
    db.commit()
    background_tasks.add_task(_generate_and_save, session.id, session.data or {})
    return {"status": "generating", "message": "Your packet is being generated. Poll /status in a few seconds."}


@router.get("/status/{session_id}")
def packet_status(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "stage": session.stage,
        "ready": session.stage == "complete" and session.packet_path is not None,
        "error": session.stage == "error"
    }


@router.get("/download/{session_id}")
def download_packet(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.packet_path or not os.path.exists(session.packet_path):
        raise HTTPException(status_code=404, detail="Packet not ready yet")
    name = (session.data or {}).get("petitioner_name", "user").replace(" ", "_")
    return FileResponse(
        path=session.packet_path,
        media_type="application/zip",
        filename=f"LegalToGo_Complete_Packet_{name}.zip"
    )


@router.get("/cache/stats")
def cache_stats(db: DBSession = Depends(get_db)):
    return get_cache_stats(db)
