from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .db import Base
from datetime import datetime

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    stripe_account_id = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer,ForeignKey("merchants.id"))
    idempotency_key = Column(String, unique=True, nullable=True)
    amount = Column(Integer)
    status = Column(String,default="pending")
    stripe_session_id = Column(String)