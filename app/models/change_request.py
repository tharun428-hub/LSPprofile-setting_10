from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    request_type = Column(String)   # lock | delete
    status = Column(String, default="pending")