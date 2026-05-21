from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.forecast import ForecastResponse
from app.services import forecast_service

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/latest", response_model=ForecastResponse)
def latest(business: Business = Depends(get_current_business), db: Session = Depends(get_db)) -> dict:
    return forecast_service.latest_forecast(db, business)
