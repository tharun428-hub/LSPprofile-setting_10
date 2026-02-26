from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class EmployeeDetails(Base):
    __tablename__ = "employee_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    employee_id = Column(String)
    department = Column(String)
    designation = Column(String)

    user = relationship("User", back_populates="employee")
