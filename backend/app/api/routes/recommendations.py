from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.pagination import Page
from app.schemas.recommendation import RecommendationRead, RecommendationsResponse
from app.services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationsResponse)
def list_recommendations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    rows, total = recommendation_service.get_recommendations(db, business, limit, offset)
    return {"recommendations": rows, "total": total, "limit": limit, "offset": offset}
