from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    loan_amount = Column(Float)
    loan_type = Column(String)
    tenure = Column(Integer)
    monthly_income = Column(Float)
    status = Column(String, default="pending")