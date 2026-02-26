from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.profile_change_request import ProfileChangeRequest
from app.core.permissions import super_admin_required

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    total_users = db.query(User).count()

    active_users = db.query(User)\
        .filter(User.status == "ACTIVE").count()

    locked_users = db.query(User)\
        .filter(User.status == "LOCKED").count()

    pending_requests = db.query(ProfileChangeRequest)\
        .filter(ProfileChangeRequest.status == "PENDING").count()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "locked_users": locked_users,
        "pending_requests": pending_requests
    }
