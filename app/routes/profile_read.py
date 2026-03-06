from fastapi import APIRouter, Depends, HTTPException ,UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileResponse
from app.models.user import User
from app.core.auth import get_current_user

from firebase_admin import storage
from app.services.auth_dependency import verify_token
router = APIRouter(prefix="", tags=["Profile"])
import cloudinary.uploader
from fastapi import UploadFile, File, Depends

@router.post("/api/v1/user/profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    user = Depends(verify_token)
):

    result = cloudinary.uploader.upload(
        file.file,
        folder="profile_images",
        public_id=user["sub"]
    )

    return {
        "message": "Profile image uploaded successfully",
        "image_url": result["secure_url"]
    }
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

@router.put("/profile")
def update_profile(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):

    profile = db.query(User).filter(User.id == user.id).first()

    profile.name = data["name"]
    profile.designation = data["designation"]

    db.commit()

    return {
        "message": "Profile updated successfully"
    }
@router.get("/api/v1/user/profile-completion")
def profile_completion(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    completion = 0
    fields = {}

    if profile.user.name:
        completion += 20
        fields["name"] = True
    else:
        fields["name"] = False

    if profile.user.email:
        completion += 20
        fields["email"] = True
    else:
        fields["email"] = False

    if profile.primary_address:
        completion += 20
        fields["primary_address"] = True
    else:
        fields["primary_address"] = False

    if profile.designation:
        completion += 20
        fields["designation"] = True
    else:
        fields["designation"] = False

    if profile.date_of_birth:
        completion += 20
        fields["date_of_birth"] = True
    else:
        fields["date_of_birth"] = False

    return {
        "profile_completion_percentage": f"{completion}%",
        "fields_status": fields
    }
@router.delete("/api/v1/user/profile-image")
def delete_profile_image(user=Depends(verify_token)):

    cloudinary.uploader.destroy(f"profile_images/{user['sub']}")

    return {"message": "Profile image deleted"}