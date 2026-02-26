from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import user_required
from app.core.auth import oauth2_scheme

from app.models.user import User
from app.models.user_settings import UserSettings
from app.models.user_session import UserSession

from app.schemas.user_settings import SettingsUpdate

router = APIRouter(
    prefix="/api/v1/user",
    tags=["Settings"],
    dependencies=[Depends(oauth2_scheme)]
)

# ==========================================
# GET USER SETTINGS
# ==========================================
@router.get("/settings")
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    if not settings:
        # Auto create if missing
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


# ==========================================
# UPDATE USER SETTINGS
# ==========================================
@router.put("/settings")
def update_settings(
    data: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)

    settings.biometric_enabled = data.biometric_enabled
    settings.pin_enabled = data.pin_enabled
    settings.language = data.language
    settings.push_notification = data.push_notification
    settings.sms_notification = data.sms_notification
    settings.email_notification = data.email_notification

    db.commit()
    db.refresh(settings)

    return {"message": "Settings updated successfully"}


# ==========================================
# DOWNLOAD CONSENT RECORD
# ==========================================
@router.get("/consent-download")
def download_consent_record(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()

    return {
        "user_id": current_user.id,
        "consent_status": "Accepted",
        "language": settings.language if settings else "en"
    }


# ==========================================
# ACTIVE SESSIONS
# ==========================================
@router.get("/active-sessions")
def active_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    sessions = db.query(UserSession).filter(
        UserSession.user_id == current_user.id,
        UserSession.is_active == True
    ).all()

    return sessions


# ==========================================
# LOGOUT ALL DEVICES
# ==========================================
@router.post("/logout-all")
def logout_all_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    db.query(UserSession).filter(
        UserSession.user_id == current_user.id
    ).update({"is_active": False})

    db.commit()

    return {"message": "Logged out from all devices"}