from app.core.database import SessionLocal
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.employee_details import EmployeeDetails
from app.models.bank_details import BankDetails
from app.models.user_settings import UserSettings
from app.core.auth import hash_password
from datetime import date


def create_default_users():
    db = SessionLocal()

    try:
        users_data = [
            {
                "name": "superadmin",
                "mobile": "9999999999",
                "email": "superadmin@gmail.com",
                "password": "123456",
                "role": "SUPER_ADMIN",
                "address": "Head Office",
                "employee": {
                    "employee_id": "ADMIN001",
                    "department": "Admin",
                    "designation": "Super Admin",
                    "date_of_birth": date(1995, 1, 1)
                },
                "bank": {
                    "account_holder_name": "Super Admin",
                    "bank_name": "SBI",
                    "account_number": "1111111111",
                    "ifsc_code": "SBIN0000001",
                    "account_type": "Savings"
                }
            },
            {
                "name": "admin",
                "mobile": "9999999998",
                "email": "admin@gmail.com",
                "password": "123456",
                "role": "ADMIN",
                "address": "Vijayawada",
                "employee": {
                    "employee_id": "ADMIN002",
                    "department": "Admin",
                    "designation": "Admin",
                    "date_of_birth": date(1996, 5, 10)
                },
                "bank": {
                    "account_holder_name": "Admin",
                    "bank_name": "HDFC",
                    "account_number": "2222222222",
                    "ifsc_code": "HDFC0000001",
                    "account_type": "Savings"
                }
            },
            {
                "name": "Tharun",
                "mobile": "6309931878",
                "email": "tharun1893@gmail.com",
                "password": "123456",
                "role": "USER",
                "address": "Lakshmi Nagar, Vijayawada",
                "employee": {
                    "employee_id": "USR001",
                    "department": "IT",
                    "designation": "Developer",
                    "date_of_birth": date(2000, 8, 29)
                },
                "bank": {
                    "account_holder_name": "Tharun",
                    "bank_name": "SBI",
                    "account_number": "1234567890",
                    "ifsc_code": "SBIN0001234",
                    "account_type": "Savings"
                }
            }
        ]

        for data in users_data:

            # 🔍 Check if user already exists by email
            existing_user = db.query(User).filter(
                User.email == data["email"]
            ).first()

            if existing_user:
                user = existing_user
            else:
                user = User(
                    name=data["name"],
                    mobile=data["mobile"],
                    email=data["email"],
                    password=hash_password(data["password"]),
                    role=data["role"]
                )
                db.add(user)
                db.flush()

            # ✅ Create UserSettings if missing
            existing_settings = db.query(UserSettings).filter(
                UserSettings.user_id == user.id
            ).first()

            if not existing_settings:
                settings = UserSettings(
                    user_id=user.id,
                    biometric_enabled=False,
                    pin_enabled=False,
                    account_locked=False,
                    is_deleted=False,
                    language="en",
                    push_notification=True,
                    sms_notification=True,
                    email_notification=True
                )
                db.add(settings)

            # ✅ Create Profile if missing
            existing_profile = db.query(UserProfile).filter(
                UserProfile.user_id == user.id
            ).first()

            if not existing_profile:
                profile = UserProfile(
                    user_id=user.id,
                    primary_address=data["address"],
                    temporary_address="",
                    employment_type="Full Time",
                    company_or_college="Company",
                    monthly_income="50000",
                    designation=data["employee"]["designation"],
                    date_of_birth=data["employee"]["date_of_birth"]
                )
                db.add(profile)

            # ✅ Create EmployeeDetails if missing
            existing_employee = db.query(EmployeeDetails).filter(
                EmployeeDetails.user_id == user.id
            ).first()

            if not existing_employee:
                employee = EmployeeDetails(
                    user_id=user.id,
                    employee_id=data["employee"]["employee_id"],
                    department=data["employee"]["department"],
                    designation=data["employee"]["designation"]
                )
                db.add(employee)

            # ✅ Create BankDetails if missing
            existing_bank = db.query(BankDetails).filter(
                BankDetails.user_id == user.id
            ).first()

            if not existing_bank:
                bank = BankDetails(
                    user_id=user.id,
                    account_holder_name=data["bank"]["account_holder_name"],
                    bank_name=data["bank"]["bank_name"],
                    account_number=data["bank"]["account_number"],
                    ifsc_code=data["bank"]["ifsc_code"],
                    account_type=data["bank"]["account_type"]
                )
                db.add(bank)

        db.commit()
        print("Default users and related data ensured successfully.")

    finally:
        db.close()