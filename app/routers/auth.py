from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    ChangePasswordRequest,
    UserResponse,
    TokenResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/api/auth")


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, payload)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, payload)
    return TokenResponse(access_token=token, expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    auth_service.change_password(db, current_user, payload)
    return {"message": "Đổi mật khẩu thành công."}
