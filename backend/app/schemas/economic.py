from datetime import date

from pydantic import BaseModel, Field


class EconomicIndicatorCreate(BaseModel):
    country: str = Field(default="Nigeria", min_length=2, max_length=80)
    indicator_name: str = Field(min_length=3, max_length=120)
    indicator_value: float
    unit: str = Field(default="%", max_length=40)
    source: str = Field(default="manual", max_length=120)
    record_date: date


class EconomicIndicatorRead(BaseModel):
    name: str
    value: float
    unit: str
    date: date
    source: str = "manual"
    trend_percent: float = 0
    trend_label: str = "No prior data"


class EconomicHistoryPoint(BaseModel):
    date: date
    value: float


class EconomicRiskMapping(BaseModel):
    indicator: str
    risk_factor: str
    impact: str
    severity: str
    explanation: str


class EconomicAlert(BaseModel):
    indicator: str
    severity: str
    message: str
    date: date


class EconomicDataSource(BaseModel):
    name: str
    status: str
    note: str


class EconomicIndicatorsResponse(BaseModel):
    country: str
    indicators: list[EconomicIndicatorRead]
    history: dict[str, list[EconomicHistoryPoint]] = {}
    risk_mappings: list[EconomicRiskMapping] = []
    alerts: list[EconomicAlert] = []
    public_sources: list[EconomicDataSource] = []
