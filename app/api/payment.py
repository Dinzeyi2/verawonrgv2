from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel
import stripe
from app.core.config import settings
from app.core.database import get_db
from app.models.db import Session

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutRequest(BaseModel):
    session_id: str
    success_url: str
    cancel_url: str

@router.post("/checkout")
def create_checkout(body: CheckoutRequest, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == body.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.stage not in ["review", "interview"]:
        raise HTTPException(status_code=400, detail="Complete the interview first")

    data = session.data or {}
    name = data.get("petitioner_full_name", "Customer")

    # Build description based on what docs will be generated
    docs = ["Divorce Petition"]
    if data.get("petitioner_wants_name_change"):
        docs.append("Name Change Packet")
    if data.get("has_joint_bank_accounts") or data.get("has_retirement_accounts"):
        docs.append("Asset Transfer Letters")
    if data.get("has_minor_children"):
        docs.append("Co-Parenting Plan")
    docs.append("Financial Reset Guide")
    description = f"Complete packet: {', '.join(docs)}"

    checkout = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": settings.PRODUCT_PRICE_CENTS,
                "product_data": {
                    "name": "Legal-to-Go — Complete Filing Packet",
                    "description": description,
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=body.success_url + f"?session_id={body.session_id}",
        cancel_url=body.cancel_url,
        metadata={"legal_session_id": body.session_id},
        customer_email=data.get("petitioner_email"),
    )

    session.stripe_session_id = checkout.id
    db.commit()

    return {"checkout_url": checkout.url, "stripe_session_id": checkout.id}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: DBSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        stripe_session = event["data"]["object"]
        legal_session_id = stripe_session["metadata"].get("legal_session_id")

        if legal_session_id:
            session = db.query(Session).filter(Session.id == legal_session_id).first()
            if session:
                session.paid = True
                session.stripe_payment_intent = stripe_session.get("payment_intent")
                session.stage = "generating"
                db.commit()

    return {"status": "ok"}


@router.get("/status/{session_id}")
def payment_status(session_id: str, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"paid": session.paid, "stage": session.stage}
