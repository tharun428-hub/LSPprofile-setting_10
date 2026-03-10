from pydantic import BaseModel, EmailStr
from datetime import date


class UserResponse(BaseModel):
    id: int
    name: str
    mobile: str
    email: EmailStr

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    primary_address: str
    temporary_address: str | None
    employment_type: str | None
    company_or_college: str | None
    monthly_income: str | None
    designation: str | None
    date_of_birth: date | None

    class Config:
        from_attributes = True


class EmployeeResponse(BaseModel):
    employee_id: str
    department: str
    designation: str

    class Config:
        from_attributes = True


class BankResponse(BaseModel):
    account_holder_name: str
    bank_name: str
    account_number: str
    ifsc_code: str
    account_type: str

    class Config:
        from_attributes = True


class ExportDataResponse(BaseModel):
    user: UserResponse
    profile: ProfileResponse | None
    employee: EmployeeResponse | None
    bank_details: BankResponse | None
