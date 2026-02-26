from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from app.core.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)

    # link settings to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Security Settings
    biometric_enabled = Column(Boolean, default=False, nullable=False)
    pin_enabled = Column(Boolean, default=False, nullable=False)
    account_locked = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False)

    # Language Setting
    language = Column(String, default="en")

    # Notification Settings
    push_notification = Column(Boolean, default=True)
    sms_notification = Column(Boolean, default=True)
    email_notification = Column(Boolean, default=True)