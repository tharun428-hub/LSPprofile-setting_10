from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.change_request import ChangeRequest
from app.models.user import User
from app.models.user_settings import UserSettings

from app.core.database import get_db
from app.core.permissions import (
    admin_required,
    super_admin_required
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ===============================
# GET ALL PENDING CHANGE REQUESTS
# ===============================
@router.get("/change-request")
def get_requests(
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required)
):
    return db.query(ChangeRequest).filter(
        ChangeRequest.status == "pending"
    ).all()


# ===============================
# APPROVE OR REJECT REQUEST
# ===============================
@router.put("/change-request/{request_id}")
def approve_or_reject(
    request_id: int,
    action: str,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required)
):

    request = db.query(ChangeRequest).filter(
        ChangeRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )

    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_settings = db.query(UserSettings).filter(
        UserSettings.user_id == user.id
    ).first()

    if not user_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found"
        )

    # ===============================
    # APPROVE LOGIC
    # ===============================
    if action.lower() == "approve":

        # LOCK ACCOUNT
        if request.field_name.lower() == "lock_account":
            user_settings.account_locked = True

        # DELETE ACCOUNT
        elif request.field_name.lower() == "delete_account":
            user_settings.is_deleted = True

        # EMAIL CHANGE
        elif request.field_name.lower() == "email":
            user.email = request.new_value

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request type"
            )

        request.status = "approved"

    # ===============================
    # REJECT LOGIC
    # ===============================
    elif action.lower() == "reject":
        request.status = "rejected"

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be approve or reject"
        )

    db.commit()

    return {
        "message": f"Request {request.status}",
        "user_id": user.id
    }


# ===============================
# ADMIN DASHBOARD
# ===============================
@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    total_users = db.query(User).filter(
        User.role == "USER"
    ).count()

    locked_users = db.query(UserSettings).filter(
        UserSettings.account_locked == True
    ).count()

    deleted_users = db.query(UserSettings).filter(
        UserSettings.is_deleted == True
    ).count()

    active_users = total_users - locked_users - deleted_users

    return {
        "total_users": total_users,
        "active_users": active_users,
        "locked_users": locked_users,
        "deleted_users": deleted_users
    }


# ===============================
# ADMIN VIEW USERS
# ===============================
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    users = db.query(User).filter(
        User.role == "USER"
    ).all()

    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "mobile": u.mobile,
            "role": u.role
        }
        for u in users
    ]


# ===============================
# SUPER ADMIN VIEW ALL USERS
# ===============================
@router.get("/all-users")
def all_users(
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required)
):

    users = db.query(User).filter(
        User.role.in_(["USER", "ADMIN"])
    ).all()

    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "mobile": u.mobile,
            "role": u.role
        }
        for u in users
    ]