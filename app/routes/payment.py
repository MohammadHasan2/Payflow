import stripe
from fastapi import APIRouter, Depends
from ..config import STRIPE_SECRET_KEY, DOMAIN
from ..models import Payment
from sqlalchemy.orm import Session
from ..auth import get_current_merchant, get_db
from ..services.stripe_service import create_checkout_session
from fastapi import Header, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from ..limiter import limiter
from ..logger import logger

stripe.api_key = STRIPE_SECRET_KEY
router = APIRouter()


@router.post("/create-payment")
@limiter.limit("10/minute")
def create_payment(request: Request, amount: int,  idempotency_key: str = Header(None),merchant = Depends(get_current_merchant), db: Session = Depends(get_db)):
    if not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail="Missing Idempotency-Key"
        )

    existing_payment = db.query(Payment).filter(
        Payment.idempotency_key == idempotency_key
    ).first()

    if existing_payment:
        logger.warning(
            f"Duplicate payment attempt by merchant {merchant.id}"
        )
        return {
            "message": "Payment already exists",
            "checkout_url": existing_payment.stripe_session_id
        }
    session = create_checkout_session(amount, merchant)

    payment = Payment(
        merchant_id=merchant.id,
        amount=amount,
        status="pending",
        stripe_session_id=session.id,
        idempotency_key=idempotency_key
    )
    db.add(payment)
    db.commit()
    logger.info(
        f"Merchant {merchant.id} created payment of {amount} USD"
    )
    db.refresh(payment)

    return {"checkout_url": session.url}
    