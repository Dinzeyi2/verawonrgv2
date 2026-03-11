from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
from app.core.database import get_db
from app.models.db import Session
from app.services.intake_agent import run_intake_turn, finalize_data_extraction, get_forms_and_fields
from sqlalchemy.orm.attributes import flag_modified

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

    result = await run_intake_turn([], "__START__", {"stage": "screening"})

    session.conversation = result["updated_conversation"]
    session.stage = "screening"
    session.data = {}
    flag_modified(session, "data")
    db.commit()

    return {"reply": result["reply"], "is_complete": False}


@router.post("/message")
async def send_message(body: MessageRequest, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    conversation = session.conversation or []
    current_data = dict(session.data or {})
    current_stage = session.stage or "screening"

    # Build session_meta
    session_meta = {
        "stage": current_stage,
        "forms_with_fields": current_data.get("_forms_with_fields", []),
    }

    result = await run_intake_turn(conversation, body.message, session_meta)

    # Merge collected data
    if result["data_collected"]:
        current_data.update(result["data_collected"])

    session.conversation = result["updated_conversation"]

    # ── Screening just completed → fetch real PDF fields ──────────
    if result.get("screening_complete") and current_stage == "screening":
        state = current_data.get("state", "California")
        has_children = current_data.get("has_children", False)
        wants_name_change = current_data.get("wants_name_change", False)
        has_assets = current_data.get("has_assets", False)

        # Fetch real fields from PDFs
        forms_with_fields = get_forms_and_fields(state, has_children, wants_name_change, has_assets)
        current_data["_forms_with_fields"] = forms_with_fields
        current_data["filing_state"] = state

        session.stage = "interview"

        # Kick off the interview with the first question group
        interview_meta = {
            "stage": "interview",
            "forms_with_fields": forms_with_fields
        }
        first_question = await run_intake_turn(
            result["updated_conversation"],
            "Please start asking me the questions needed to fill out my forms.",
            interview_meta
        )
        session.conversation = first_question["updated_conversation"]
        reply = first_question["reply"]
        if first_question["data_collected"]:
            current_data.update(first_question["data_collected"])

    else:
        reply = result["reply"]

    # ── Interview complete ────────────────────────────────────────
    if result["is_complete"]:
        final_data = await finalize_data_extraction(result["updated_conversation"], current_data)
        # Remove internal metadata before saving
        final_data.pop("_forms_with_fields", None)
        session.data = final_data
        session.stage = "complete"
    else:
        session.data = current_data

    flag_modified(session, "data")
    flag_modified(session, "conversation")
    db.commit()

    return {
        "reply": reply,
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
