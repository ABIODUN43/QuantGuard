from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.economic import EconomicIndicatorCreate, EconomicIndicatorsResponse
from app.services import economic_service

router = APIRouter(prefix="/economic", tags=["economic intelligence"])


@router.get("/indicators", response_model=EconomicIndicatorsResponse)
def indicators(country: str = "Nigeria", db: Session = Depends(get_db)) -> dict:
    return economic_service.indicators(db, country)


@router.post("/indicators")
def create_indicator(
    payload: EconomicIndicatorCreate,
    _: User = Depends(require_roles("admin", "business_owner")),
    db: Session = Depends(get_db),
) -> dict:
    row = economic_service.add_indicator(db, payload)
    return {
        "message": "Economic indicator saved",
        "indicator": {
            "name": row.indicator_name,
            "value": float(row.indicator_value),
            "unit": row.unit,
            "date": row.record_date,
            "source": row.source,
        },
    }


@router.post("/seed-history")
def seed_history(
    country: str = "Nigeria",
    _: User = Depends(require_roles("admin", "business_owner")),
    db: Session = Depends(get_db),
) -> dict:
    return economic_service.seed_economic_history(db, country)
