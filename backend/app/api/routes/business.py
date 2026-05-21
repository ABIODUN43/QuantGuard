from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.exceptions import not_found
from app.db.session import get_db
from app.schemas.business import BusinessOnboardRequest, BusinessOnboardResponse, BusinessRead
from app.services import business_service

router = APIRouter(prefix="/business", tags=["business"])


@router.post(
    "/onboard",
    response_model=BusinessOnboardResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "business_name": "GreenField Stores",
                        "business_type": "Retail Trade",
                        "industry": "Retail",
                        "country": "Nigeria",
                        "state": "Lagos",
                        "city": "Ikeja",
                        "years_in_operation": 4,
                        "number_of_employees": 12,
                        "average_monthly_revenue": 2500000,
                        "average_monthly_expenses": 1800000,
                    }
                }
            }
        }
    },
)
def onboard(
    payload: BusinessOnboardRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return business_service.onboard_business(db, user, payload)


@router.get("/me", response_model=BusinessRead)
def business_me(user=Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    business = business_service.current_business(db, user)
    if not business:
        raise not_found("Business profile not found")
    return business
