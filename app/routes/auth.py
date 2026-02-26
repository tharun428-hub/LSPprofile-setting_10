from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.user_settings import UserSettings
from app.models.user_session import UserSession

from app.core.auth import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ==========================================
# REGISTER USER
# ==========================================
@router.post("/register")
def register_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role="USER"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔥 Automatically create user settings
    new_settings = UserSettings(
        user_id=new_user.id
    )

    db.add(new_settings)
    db.commit()

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ==========================================
# LOGIN USER
# ==========================================
@router.post("/login")
def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    refresh_token = create_refresh_token()

    # Create user session
    session = UserSession(
        user_id=user.id,
        device_name="web",
        ip_address=request.client.host
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "role": user.role
    }