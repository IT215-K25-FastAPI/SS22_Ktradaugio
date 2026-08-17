from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
import jwt

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_TOKEN", "detail": "Thiếu token xác thực"},
        )

    token = authorization.replace("Bearer ", "")

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_TOKEN", "detail": "Token đã hết hạn"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_TOKEN", "detail": "Token không hợp lệ hoặc bị giả mạo"},
        )

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "INVALID_TOKEN", "detail": "Người dùng trong token không tồn tại"},
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail={"error": "PERMISSION_DENIED", "detail": "Chỉ quản trị viên mới được truy cập"},
        )
    return current_user
