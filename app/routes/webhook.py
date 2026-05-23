import stripe
from fastapi import APIRouter, Request
from ..config import STRIPE_SECRET_KEY
from ..models import Payment
from ..db import SessionLocal

stripe.api_key = STRIPE_SECRET_KEY
router = APIRouter()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    event = stripe.Event.construct_from(
        await request.json(), stripe.api_key
    )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        db = SessionLocal()
        payment = db.query(Payment).filter(Payment.stripe_session_id == session.id).first()
        if payment:
            payment.status = "completed"
            db.commit()
            db.refresh(payment)
        db.close()
        return {"status": "success"}