from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import oauth2_scheme
from app.core.permissions import user_required

from app.models.language import Language
from app.models.user import User
from app.schemas.language import LanguageUpdate

router = APIRouter(
    prefix="/settings/language",
    tags=["Settings - Language"],
    dependencies=[Depends(oauth2_scheme)]   
)
# GET LANGUAGE
@router.get("/")
def get_language(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    language = db.query(Language).filter(
        Language.user_id == current_user.id
    ).first()

    if not language:
        language = Language(
            user_id=current_user.id,
            language="en"
        )
        db.add(language)
        db.commit()
        db.refresh(language)

    return {
        "user_id": current_user.id,
        "language": language.language
    }
# UPDATE LANGUAGE
@router.put("/")
def update_language(
    data: LanguageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    language = db.query(Language).filter(
        Language.user_id == current_user.id
    ).first()

    if not language:
        language = Language(
            user_id=current_user.id,
            language=data.language
        )
        db.add(language)
    else:
        language.language = data.language

    db.commit()
    db.refresh(language)

    return {
        "message": "Language updated successfully",
        "language": language.language
    }