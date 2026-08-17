from datetime import datetime
from pydantic import BaseModel


class TransferRequest(BaseModel):
    to_username: str
    amount: float
    note: str = None


class BalanceResponse(BaseModel):
    username: str
    balance: float
    message: str


class TransferResponse(BaseModel):
    from_username: str
    to_username: str
    amount: float
    note: str = None
    from_balance_after: float
    message: str


class UserAdminResponse(BaseModel):
    id: int
    username: str
    role: str
    balance: float
    created_at: datetime

    model_config = {"from_attributes": True}
