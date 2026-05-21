from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ScenarioChanges(BaseModel):
    fuel_price_increase_percent: float = Field(default=0, ge=-100, le=500)
    sales_change_percent: float = Field(default=0, ge=-100, le=500)
    operating_expenses_change_percent: float = Field(default=0, ge=-100, le=500)
    inventory_level_change_percent: float = Field(default=0, ge=-100, le=500)
    new_loan_amount: float = Field(default=0, ge=0)


class ScenarioRunRequest(BaseModel):
    scenario_name: str = Field(min_length=3, max_length=160)
    changes: ScenarioChanges


class ScenarioResponse(BaseModel):
    scenario_id: UUID
    scenario_name: str
    risk_score: float
    stress_probability: float
    cash_shortfall_probability: float
    impact: str
    summary: str
    created_at: datetime
