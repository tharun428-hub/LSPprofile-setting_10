from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import oauth2_scheme
from app.core.permissions import user_required

from app.models.user_profile import UserProfile
from app.models.user import User
from app.schemas.user_profile import TemporaryAddressUpdate


router = APIRouter(
    prefix="",
    tags=["Profile"],
    dependencies=[Depends(oauth2_scheme)]   
)


@router.put("/api/v1/user/profile/temporary-address")
def update_temp_address(
    data: TemporaryAddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile.temporary_address = data.temporary_address
    db.commit()
    db.refresh(profile)

    return {
        "message": "Temporary address updated successfully",
        "temporary_address": profile.temporary_address
    }