from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import INITIAL_BALANCE
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, ChangePasswordRequest


def register_user(db: Session, payload: UserRegisterRequest):
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail={"error": "USER_ALREADY_EXISTS", "detail": "Tên đăng nhập đã tồn tại"},
        )

    new_user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        balance=INITIAL_BALANCE,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, payload: UserLoginRequest):
    user = db.query(User).filter(User.username == payload.username).first()

    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_CREDENTIALS", "detail": "Sai tên đăng nhập hoặc mật khẩu"},
        )

    token = create_access_token(username=user.username, role=user.role)
    return token


def change_password(db: Session, current_user: User, payload: ChangePasswordRequest):
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_CREDENTIALS", "detail": "Mật khẩu cũ không chính xác"},
        )

    if payload.old_password == payload.new_password:
        raise HTTPException(
            status_code=400,
            detail={"error": "SAME_PASSWORD", "detail": "Mật khẩu mới không được trùng mật khẩu cũ"},
        )

    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()
