from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import oauth2_scheme
from app.core.permissions import user_required
from app.models.user import User

from app.schemas.notification import (
    NotificationUpdate,
    NotificationResponse
)

from app.services.notification_service import (
    get_notification,
    update_notification
)

router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    dependencies=[Depends(oauth2_scheme)]   
)

@router.get("/", response_model=NotificationResponse)
def read_notification(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return get_notification(db, current_user.id)

@router.put("/", response_model=NotificationResponse)
def update_notification_settings(
    data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return update_notification(db, current_user.id, data)