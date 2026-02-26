from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import user_required

from app.models.user import User
from app.models.consent import Consent
from app.models.change_request import ChangeRequest

from app.services.privacy_service import export_user_data
from app.schemas.export_schema import ExportDataResponse


router = APIRouter(
    prefix="/user",
    tags=["User Privacy"]
)


@router.get("/export-data", response_model=ExportDataResponse)
def export_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return export_user_data(db, current_user.id)



@router.get("/consent-history")
def consent_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return db.query(Consent).filter(
        Consent.user_id == current_user.id
    ).all()



@router.post("/revoke-consent")
def revoke_consent(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    consent = db.query(Consent).filter(
        Consent.user_id == current_user.id
    ).first()

    if consent and consent.status != "revoked":
        consent.status = "revoked"
        db.commit()

    return {"message": "Consent revoked successfully"}


@router.post("/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    current_user.is_deleted = True
    db.commit()

    return {"message": "Account delete request submitted"}


@router.post("/lock-account-request")
def lock_account_request(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    request = ChangeRequest(
        user_id=current_user.id,
        request_type="lock_account",
        status="pending"
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "message": "Lock account request sent to super admin"
    }