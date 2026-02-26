from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime

from app.core.database import Base


class ConsentHistory(Base):
    __tablename__ = "consent_history"

    id = Column(Integer, primary_key=True, index=True)


    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    
    consent_type = Column(String, nullable=False)


    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
