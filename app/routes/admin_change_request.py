from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.profile_change_request import ProfileChangeRequest
from app.core.permissions import super_admin_required

router = APIRouter(prefix="/admin/change-request", tags=["Admin Change Request"])





@router.get("/")
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):
    requests = db.query(ProfileChangeRequest)\
        .filter(ProfileChangeRequest.status == "PENDING")\
        .all()

    return requests



@router.put("/{request_id}")
def approve_or_reject(
    request_id: int,
    action: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    request = db.query(ProfileChangeRequest)\
        .filter(ProfileChangeRequest.id == request_id)\
        .first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if action == "approve":

        user = db.query(User)\
            .filter(User.id == request.user_id)\
            .first()

        setattr(user, request.field_name, request.new_value)

        request.status = "APPROVED"
        request.approved_at = datetime.utcnow()

    else:
        request.status = "REJECTED"

    db.commit()

    return {"message": f"Request {action} successfully"}
