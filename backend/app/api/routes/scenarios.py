from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.scenario import ScenarioResponse, ScenarioRunRequest
from app.services import scenario_service

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post(
    "/run",
    response_model=ScenarioResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "scenario_name": "Fuel Price Increase +20%",
                        "changes": {
                            "fuel_price_increase_percent": 20,
                            "sales_change_percent": 0,
                            "operating_expenses_change_percent": 5,
                            "inventory_level_change_percent": 0,
                            "new_loan_amount": 0,
                        },
                    }
                }
            }
        }
    },
)
def run(
    payload: ScenarioRunRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return scenario_service.run_scenario(db, business, payload)
