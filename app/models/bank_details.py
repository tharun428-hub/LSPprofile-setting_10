from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class BankDetails(Base):
    __tablename__ = "bank_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    account_holder_name = Column(String)
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    account_type = Column(String)
    user = relationship("User", back_populates="bank")

