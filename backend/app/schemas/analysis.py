from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RiskBreakdown(BaseModel):
    expense_instability: float
    liquidity_weakness: float
    inventory_exposure: float
    debt_pressure: float
    revenue_volatility: float
    fuel_cost_sensitivity: float


class AnalysisResponse(BaseModel):
    analysis_id: UUID
    risk_score: float
    stress_probability: float
    financial_stability_score: float
    forecast_confidence: float
    risk_level: str
    risk_breakdown: RiskBreakdown
    contribution_percentages: dict[str, float] = {}
    anomalies: list[dict] = []
    model_notes: dict = {}
    summary: str
    created_at: datetime
