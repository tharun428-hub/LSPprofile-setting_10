from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.change_request import (
    ChangeRequestCreate,
    ChangeRequestResponse
)
from app.services.change_request_service import (
    create_change_request,
    approve_request
)

router = APIRouter(
    prefix="/settings",
    tags=["Change Request"]
)


@router.post(
    "/request-change",
    response_model=ChangeRequestResponse
)
def request_change(
    user_id: int,
    data: ChangeRequestCreate,
    db: Session = Depends(get_db)
):
    return create_change_request(db, user_id, data)


@router.put(
    "/approve/{request_id}",
    response_model=ChangeRequestResponse
)
def approve_change(
    request_id: int,
    db: Session = Depends(get_db)
):
    return approve_request(db, request_id)