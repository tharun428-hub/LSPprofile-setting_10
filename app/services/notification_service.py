from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.notification import Notification


# get notification (auto create if not exists) 
def get_notification(db: Session, user_id: int):

    notification = db.query(Notification).filter(
        Notification.user_id == user_id
    ).first()

    # create default notification if not exists
    if not notification:
        notification = Notification(user_id=user_id)
        db.add(notification)
        db.commit()
        db.refresh(notification)

    return notification


# Update Notification
def update_notification(
    db: Session,
    user_id: int,
    data
):

    notification = db.query(Notification).filter(
        Notification.user_id == user_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification settings not found"
        )

    notification.sms = data.sms
    notification.email = data.email
    notification.loan_updates = data.loan_updates
    notification.emi_reminders = data.emi_reminders
    notification.payment_alerts = data.payment_alerts
    notification.push_notification = data.push_notification

    db.commit()
    db.refresh(notification)

    return notification
