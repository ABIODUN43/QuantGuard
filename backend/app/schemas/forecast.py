from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class CashflowForecastPoint(BaseModel):
    month: str
    projected_revenue: float
    projected_expenses: float
    projected_cash_balance: float
    low_cash_balance: float | None = None
    high_cash_balance: float | None = None


class ForecastResponse(BaseModel):
    forecast_id: UUID
    analysis_id: UUID
    projected_cash_balance: float
    cash_shortfall_probability: float
    forecast_confidence: float
    danger_period_start: date | None
    danger_period_end: date | None
    danger_period: str
    breakeven_revenue: float
    cashflow_forecast: list[CashflowForecastPoint]
    model: str | None = None
    confidence_interval_note: str | None = None
    volatility: dict | None = None
    created_at: datetime
