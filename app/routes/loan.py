from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.loan import LoanApply
from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.loan import LoanApplication
from app.models.user import User

router = APIRouter(prefix="/loan", tags=["Loan"])




@router.get("/status/{application_id}") 
def loan_status(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    loan = db.query(LoanApplication).filter(
        LoanApplication.id == application_id
    ).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    
    if loan.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this loan"
        )

    return {
        "application_id": loan.id,
        "status": loan.status
    }


@router.get("/history")
def loan_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    loans = db.query(LoanApplication).filter(
        LoanApplication.user_id == user.id
    ).all()

    result = []

    for loan in loans:
        result.append({
            "loan_id": loan.id,
            "amount": loan.loan_amount,
            "status": loan.status
        })

    return result