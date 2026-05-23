from pydantic import BaseModel

class MerchantRegister(BaseModel):
    email: str
    password: str