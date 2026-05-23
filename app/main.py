from fastapi import FastAPI
from .db import Base, engine
from .routes import merchant, payment,webhook
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from .limiter import limiter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
Base.metadata.create_all(bind=engine)
app.include_router(merchant.router, prefix="/merchants")
app.include_router(webhook.router)
app.include_router(payment.router)
@app.get("/")
def root():
    return {"message": "Payment Gateway API running 🚀"}

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):

    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded"
        }
    )