from sqlalchemy import Column, Integer, String, Enum,Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    user = "user"
    super_admin = "super_admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobile = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default="user")
    email_otp = Column(String, nullable=True)
    email_otp_verified = Column(Boolean, default=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    employee = relationship("EmployeeDetails", back_populates="user", uselist=False)
    bank = relationship("BankDetails", back_populates="user", uselist=False)
    account_locked = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)