from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BusinessOnboardRequest(BaseModel):
    business_name: str = Field(min_length=2, max_length=180)
    business_type: str
    industry: str
    country: str = "Nigeria"
    state: str
    city: str
    years_in_operation: int = Field(ge=0)
    number_of_employees: int = Field(ge=1)
    average_monthly_revenue: float = Field(ge=0)
    average_monthly_expenses: float = Field(ge=0)


class BusinessOnboardResponse(BaseModel):
    message: str
    business_id: UUID


class BusinessRead(BusinessOnboardRequest):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
