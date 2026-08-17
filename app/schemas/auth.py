from datetime import datetime
from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "customer"


class UserLoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    balance: float
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
