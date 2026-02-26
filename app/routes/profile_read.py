from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileResponse
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter(prefix="", tags=["Profile"])
# get user profile
@router.get("/api/v1/user/profile", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return UserProfileResponse(
        name=profile.user.name,
        mobile=profile.user.mobile,
        email=profile.user.email,
        primary_address=profile.primary_address,
        temporary_address=profile.temporary_address,
        employment_type=profile.employment_type,
        company_or_college=profile.company_or_college,
        monthly_income=profile.monthly_income,
        designation=profile.designation,
        date_of_birth=profile.date_of_birth
    )

@router.post("/api/v1/user/unlock")
def unlock_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    
    if not current_user.account_locked:
        return {"message": "Account already unlocked"}

    
    current_user.account_locked = False
    db.commit()

    return {"message": "Account unlocked successfully"}