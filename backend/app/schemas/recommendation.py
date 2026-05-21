from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    priority: str
    impact: str
    category: str
    created_at: datetime


class RecommendationsResponse(BaseModel):
    recommendations: list[RecommendationRead]
    total: int = 0
    limit: int = 20
    offset: int = 0
