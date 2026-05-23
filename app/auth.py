from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Merchant
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .logger import logger
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

security = HTTPBearer()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_merchant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    api_key = credentials.credentials
    print("API KEY:", api_key)

    merchant = db.query(Merchant).filter(Merchant.api_key == api_key).first()

    if not merchant:
        logger.warning("Invalid API key attempt")

    return merchant
    