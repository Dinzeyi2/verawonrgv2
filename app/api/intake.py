from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from app.core.database import get_db
from app.models.db import Session
from app.services.intake_agent import run_intake_turn, finalize_data_extraction

router = APIRouter()

class MessageRequest(BaseModel):
    session_id: str
    message: str

class StartRequest(BaseModel):
    session_id: str

@router.post("/start")
async def start_intake(body: StartRequest, db: DBSession = Depends(get_db)):
    """Start the intake interview — returns the first AI message."""
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await run_intake_turn([], "__START__")
    
    session.conversation = result["updated_conversation"]
    session.stage = "interview"
    db.commit()

    return {"reply": result["reply"], "is_complete": False}

@router.post("/message")
async def send_message(body: MessageRequest, db: DBSession = Depends(get_db)):
    """Send a user message and get the next interview question."""
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.paid:
        raise HTTPException(status_code=400, detail="Session already completed")

    conversation = session.conversation or []
    result = await run_intake_turn(conversation, body.message)

    # Merge any newly extracted data
    current_data = session.data or {}
    if result["data_collected"]:
        current_data.update(result["data_collected"])

    session.conversation = result["updated_conversation"]
    session.data = current_data

    if result["is_complete"]:
        # Do final clean extraction pass
        final_data = await finalize_data_extraction(result["updated_conversation"], current_data)
        session.data = final_data
        session.stage = "review"

    db.commit()

    return {
        "reply": result["reply"],
        "is_complete": result["is_complete"],
        "stage": session.stage,
        "data_snapshot": session.data if result["is_complete"] else {}
    }

@router.get("/{session_id}/summary")
def get_summary(session_id: str, db: DBSession = Depends(get_db)):
    """Get collected data summary before payment."""
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"data": session.data, "stage": session.stage}
