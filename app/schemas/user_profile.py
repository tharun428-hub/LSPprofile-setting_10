from pydantic import BaseModel, EmailStr
from datetime import date


class UserProfileResponse(BaseModel):
    name: str
    mobile: str
    email: EmailStr
    primary_address: str
    temporary_address: str | None

    employment_type: str | None
    company_or_college: str | None
    monthly_income: str | None
    designation: str | None
    date_of_birth: date | None

    class Config:
        from_attributes = True


class TemporaryAddressUpdate(BaseModel):
    temporary_address: str
