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
    prefix="/api/v1/user",
    tags=["User Privacy"]
)



# =====================================
# EXPORT USER DATA
# =====================================
@router.get("/export-data", response_model=ExportDataResponse)
def export_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return export_user_data(db, current_user.id)


# =====================================
# CONSENT HISTORY
# =====================================
@router.get("/consent-history")
def consent_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return db.query(Consent).filter(
        Consent.user_id == current_user.id
    ).all()


# =====================================
# REVOKE CONSENT
# =====================================
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


# =====================================
# DELETE ACCOUNT REQUEST (PARALLEL UPDATE)
# =====================================
@router.post("/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    # create change request
    request = ChangeRequest(
        user_id=current_user.id,
        field_name="delete_account",
        old_value=None,
        new_value=None,
        status="pending"
    )

    db.add(request)

    # ⭐ update users table also
    current_user.is_deleted = True

    db.commit()
    db.refresh(request)

    return {"message": "Account delete request submitted"}


# =====================================
# LOCK ACCOUNT REQUEST (PARALLEL UPDATE)
# =====================================
@router.post("/lock-account-request")
def lock_account_request(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    # create change request
    request = ChangeRequest(
        user_id=current_user.id,
        field_name="lock_account",
        old_value=None,
        new_value=None,
        status="pending"
    )

    db.add(request)

    # ⭐ update users table also
    current_user.account_locked = True

    db.commit()
    db.refresh(request)

    return {
        "message": "Lock account request sent to super admin"
    }