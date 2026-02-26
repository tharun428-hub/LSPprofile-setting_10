from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    primary_address = Column(String)
    temporary_address = Column(String)
    employment_type = Column(String)
    company_or_college = Column(String)
    monthly_income = Column(String)
    designation = Column(String)
    date_of_birth = Column(Date)

    user = relationship("User", back_populates="profile")
