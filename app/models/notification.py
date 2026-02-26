from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    sms = Column(Boolean, default=True)
    email = Column(Boolean, default=True)
    loan_updates = Column(Boolean, default=True)
    emi_reminders = Column(Boolean, default=True)
    payment_alerts = Column(Boolean, default=True)
    push_notification = Column(Boolean, default=True)
