from sqlalchemy.orm import Session

from app.models.user import User


def list_all_users(db: Session):
    users = db.query(User).order_by(User.id).all()
    return users
