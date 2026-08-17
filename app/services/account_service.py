from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.account import TransferRequest


def get_balance(current_user: User):
    return {
        "username": current_user.username,
        "balance": current_user.balance,
        "message": f"Chào mừng {current_user.username}, đây là số dư hiện tại của bạn.",
    }


def transfer_money(db: Session, sender: User, payload: TransferRequest):
    if payload.amount <= 0:
        raise HTTPException(
            status_code=422,
            detail={"error": "VALIDATION_ERROR", "detail": "Số tiền chuyển phải lớn hơn 0"},
        )

    if payload.to_username == sender.username:
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_TRANSFER", "detail": "Không thể tự chuyển tiền cho chính mình"},
        )

    recipient = db.query(User).filter(User.username == payload.to_username).first()
    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RECIPIENT_NOT_FOUND", "detail": "Không tìm thấy tài khoản người nhận"},
        )

    if sender.balance < payload.amount:
        raise HTTPException(
            status_code=400,
            detail={"error": "INSUFFICIENT_BALANCE", "detail": "Số dư tài khoản không đủ để thực hiện giao dịch"},
        )

    sender.balance = sender.balance - payload.amount
    recipient.balance = recipient.balance + payload.amount
    db.commit()
    db.refresh(sender)

    return {
        "from_username": sender.username,
        "to_username": recipient.username,
        "amount": payload.amount,
        "note": payload.note,
        "from_balance_after": sender.balance,
        "message": "Giao dịch chuyển tiền thành công.",
    }
