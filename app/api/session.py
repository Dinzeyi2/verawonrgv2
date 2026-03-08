from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from app.core.database import get_db
from app.models.db import Session

router = APIRouter()

class CreateSessionRequest(BaseModel):
    state: str
    county: str | None = None

@router.post("/create")
def create_session(body: CreateSessionRequest, db: DBSession = Depends(get_db)):
    session = Session(state=body.state, county=body.county)
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "stage": session.stage}

@router.get("/{session_id}")
def get_session(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session.id,
        "stage": session.stage,
        "state": session.state,
        "county": session.county,
        "paid": session.paid,
        "data": session.data,
    }
