from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.schemas.account import UserAdminResponse
from app.services import admin_service

router = APIRouter(prefix="/api/admin")


@router.get("/users", response_model=list[UserAdminResponse])
def get_all_users(db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    return admin_service.list_all_users(db)
