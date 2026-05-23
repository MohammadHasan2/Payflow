from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Merchant
import secrets
from ..auth import get_current_merchant
from ..schemas import MerchantRegister
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_merchant(
    merchant_data: MerchantRegister,
    db: Session = Depends(get_db)
):

    # 1. check duplicate
    existing = db.query(Merchant).filter(
        Merchant.email == merchant_data.email
    ).first()

    if existing:
        return {"error": "Merchant already exists"}

    # 2. create API key
    api_key = "sk_test_" + secrets.token_hex(16)

    # 3. create merchant
    merchant = Merchant(
        email=merchant_data.email,
        password_hash=hash_password(merchant_data.password),
        api_key=api_key
    )

    db.add(merchant)
    db.commit()
    db.refresh(merchant)

    return {
        "id": merchant.id,
        "api_key": merchant.api_key
    }

@router.post("/login")
def login(merchant_data: MerchantRegister, db: Session = Depends(get_db)):

    merchant = db.query(Merchant).filter(
        Merchant.email == merchant_data.email
    ).first()

    if not merchant:
        return {"error": "Invalid credentials"}

    if not verify_password(merchant_data.password, merchant.password_hash):
        return {"error": "Invalid credentials"}

    token = create_access_token(
        {"merchant_id": merchant.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "api_key": merchant.api_key
    }

@router.get("/me")
def get_me(current_merchant: Merchant = Depends(get_current_merchant)):
    return {"email": current_merchant.email, "api_key": current_merchant.api_key}