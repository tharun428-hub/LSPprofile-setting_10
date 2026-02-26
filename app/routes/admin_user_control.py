from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.permissions import super_admin_required

router = APIRouter(prefix="/admin/user", tags=["Admin User Control"])


# LOCK USER
@router.put("/lock/{user_id}")
def lock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = "LOCKED"
    db.commit()

    return {"message": "User account locked"}


# UNLOCK USER
@router.put("/unlock/{user_id}")
def unlock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = "ACTIVE"
    db.commit()

    return {"message": "User account unlocked"}
