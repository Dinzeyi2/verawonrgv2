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
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await run_intake_turn([], "__START__")

    session.conversation = result["updated_conversation"]
    session.stage = "interview"
    session.data = {}
    db.commit()

    return {"reply": result["reply"], "is_complete": False}


@router.post("/message")
async def send_message(body: MessageRequest, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    conversation = session.conversation or []
    result = await run_intake_turn(conversation, body.message)

    # Always merge — even partial data matters
    current_data = dict(session.data or {})
    if result["data_collected"]:
        current_data.update(result["data_collected"])

    session.conversation = result["updated_conversation"]
    session.data = current_data

    if result["is_complete"]:
        # Final extraction pass — pulls ALL data from full conversation
        final_data = await finalize_data_extraction(
            result["updated_conversation"],
            current_data
        )
        session.data = final_data
        session.stage = "complete"
    
    # Force SQLAlchemy to detect the dict change
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(session, "data")
    flag_modified(session, "conversation")
    db.commit()

    return {
        "reply": result["reply"],
        "is_complete": result["is_complete"],
        "stage": session.stage,
        "data_snapshot": session.data if result["is_complete"] else {}
    }


@router.get("/{session_id}/summary")
def get_summary(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"data": session.data, "stage": session.stage}
