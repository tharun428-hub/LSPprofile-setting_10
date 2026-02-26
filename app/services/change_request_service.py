from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.change_request import ChangeRequest
from app.models.user import User


# user request
def create_change_request(db: Session, user_id: int, data):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.field_name == "mobile":
        old_value = user.mobile
    elif data.field_name == "email":
        old_value = user.email
    else:
        raise HTTPException(status_code=400, detail="Invalid field")

    request = ChangeRequest(
        user_id=user_id,
        field_name=data.field_name,
        old_value=old_value,
        new_value=data.new_value
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request


# admin approve
def approve_request(db: Session, request_id: int):

    request = db.query(ChangeRequest).filter(
        ChangeRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if request.field_name == "mobile":
        user.mobile = request.new_value

    elif request.field_name == "email":
        user.email = request.new_value

    request.status = "approved"

    db.commit()
    return request
