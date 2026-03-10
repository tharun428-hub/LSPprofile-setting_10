from pydantic import BaseModel

class LoanApply(BaseModel):
    loan_amount: float
    loan_type: str
    tenure: int
    monthly_income: float