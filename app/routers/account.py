from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.account import BalanceResponse, TransferRequest, TransferResponse
from app.services import account_service

router = APIRouter(prefix="/api/account")


@router.get("/balance", response_model=BalanceResponse)
def get_balance(current_user: User = Depends(get_current_user)):
    return account_service.get_balance(current_user)


@router.post("/transfer", response_model=TransferResponse)
def transfer(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return account_service.transfer_money(db, current_user, payload)
