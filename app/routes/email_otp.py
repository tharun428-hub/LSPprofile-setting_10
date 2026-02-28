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
    tags=["Email"]
)


# ==================================
# SEND OTP TO OLD EMAIL (LOGIN REQUIRED)
# ==================================
@router.post(
    "/send-old-email-otp",
    dependencies=[Depends(oauth2_scheme)]
)
async def send_old_email_otp(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    otp = str(random.randint(100000, 999999))

    current_user.email_otp = otp
    db.commit()

    await send_otp_email(current_user.email, otp)

    return {"message": "OTP sent to old email"}


# ==================================
# VERIFY OLD EMAIL OTP (LOGIN REQUIRED)
# ==================================
@router.post(
    "/verify-old-email-otp",
    dependencies=[Depends(oauth2_scheme)]
)
def verify_old_email_otp(
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    if current_user.email_otp != otp:
        raise HTTPException(400, "Invalid OTP")

    current_user.email_otp = None
    db.commit()

    return {"message": "Old email verified"}


# ==================================
# SEND OTP TO NEW EMAIL (LOGIN REQUIRED)
# ==================================
@router.post(
    "/send-new-email-otp",
    dependencies=[Depends(oauth2_scheme)]
)
async def send_new_email_otp(
    new_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    # prevent same email
    if new_email == current_user.email:
        raise HTTPException(400, "New email cannot be same")

    # check existing email
    existing_user = db.query(User).filter(
        User.email == new_email
    ).first()

    if existing_user:
        raise HTTPException(400, "Email already exists")

    otp = str(random.randint(100000, 999999))

    current_user.new_email = new_email
    current_user.new_email_otp = otp
    db.commit()

    await send_otp_email(new_email, otp)

    return {"message": "OTP sent to new email"}


# ==================================
# VERIFY NEW EMAIL OTP (LOGIN REQUIRED)
# ==================================
@router.post(
    "/verify-new-email-otp",
    dependencies=[Depends(oauth2_scheme)]
)
def verify_new_email_otp(
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    if current_user.new_email_otp != otp:
        raise HTTPException(400, "Invalid OTP")

    # update email (NO new user created)
    current_user.email = current_user.new_email

    # clear temp fields
    current_user.new_email = None
    current_user.new_email_otp = None

    db.commit()

    return {"message": "Email updated successfully"}


# ==================================
# SEND UNLOCK OTP (NO LOGIN REQUIRED)
# ==================================
@router.post("/send-unlock-otp")
async def send_unlock_otp(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    if not user.account_locked:
        raise HTTPException(400, "Account is already active")

    otp = str(random.randint(100000, 999999))

    user.email_otp = otp
    db.commit()

    await send_otp_email(email, otp)

    return {"message": "Unlock OTP sent to email"}


# ==================================
# VERIFY OTP & UNLOCK ACCOUNT (NO LOGIN)
# ==================================
@router.post("/unlock-account")
def unlock_account(
    email: str,
    otp: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    if user.email_otp != otp:
        raise HTTPException(400, "Invalid OTP")

    # unlock account
    user.account_locked = False
    user.email_otp = None

    db.commit()

    return {"message": "Account unlocked successfully"}