from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from app.core.database import get_db
from app.core.auth import oauth2_scheme
from app.core.permissions import user_required
from app.models.user import User
from app.core.email_service import send_otp_email


router = APIRouter(
    prefix="/email",
    tags=["Email"],
    dependencies=[Depends(oauth2_scheme)]
)


# SEND OTP TO OLD EMAIL
@router.post("/send-old-email-otp")
async def send_old_email_otp(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    otp = str(random.randint(100000, 999999))

    current_user.email_otp = otp
    db.commit()

    await send_otp_email(current_user.email, otp)

    return {"message": "OTP sent to old email"}
# VERIFY OLD EMAIL OTP
@router.post("/verify-old-email-otp")
def verify_old_email_otp(
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    if current_user.email_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    current_user.email_otp = None
    db.commit()

    return {"message": "Old email verified"}
# SEND OTP TO NEW EMAIL
@router.post("/send-new-email-otp")
async def send_new_email_otp(
    new_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    otp = str(random.randint(100000, 999999))

    current_user.new_email = new_email
    current_user.new_email_otp = otp
    db.commit()

    await send_otp_email(new_email, otp)

    return {"message": "OTP sent to new email"}
# VERIFY NEW EMAIL OTP
@router.post("/verify-new-email-otp")
def verify_new_email_otp(
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    if current_user.new_email_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    current_user.email = current_user.new_email
    current_user.new_email = None
    current_user.new_email_otp = None

    db.commit()

    return {"message": "Email updated successfully"}