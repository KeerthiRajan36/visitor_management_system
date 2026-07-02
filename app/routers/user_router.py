from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.roles import admin_only

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return db.query(User).all()