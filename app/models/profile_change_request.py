from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base


class ProfileChangeRequest(Base):
    __tablename__ = "profile_change_requests"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    field_name = Column(String)
    old_value = Column(String)
    new_value = Column(String)

    status = Column(String, default="PENDING")
    # PENDING | APPROVED | REJECTED

    requested_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
