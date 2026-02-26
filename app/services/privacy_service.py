from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.employee_details import EmployeeDetails
from app.models.bank_details import BankDetails


def export_user_data(db: Session, user_id: int):

    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    employee = db.query(EmployeeDetails).filter(EmployeeDetails.user_id == user_id).first()
    bank = db.query(BankDetails).filter(BankDetails.user_id == user_id).first()

    return {
        "user": user,
        "profile": profile,
        "employee": employee,
        "bank_details": bank
    }
