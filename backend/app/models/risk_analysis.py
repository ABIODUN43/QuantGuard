from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class RiskAnalysis(UUIDTimestampMixin, Base):
    __tablename__ = "risk_analysis"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    risk_score: Mapped[float] = mapped_column(Numeric(6, 2))
    stress_probability: Mapped[float] = mapped_column(Numeric(5, 4))
    financial_stability_score: Mapped[float] = mapped_column(Numeric(6, 2))
    forecast_confidence: Mapped[float] = mapped_column(Numeric(5, 4))
    risk_level: Mapped[str] = mapped_column(String(50))
    revenue_volatility: Mapped[float] = mapped_column(Numeric(6, 2))
    expense_instability: Mapped[float] = mapped_column(Numeric(6, 2))
    liquidity_weakness: Mapped[float] = mapped_column(Numeric(6, 2))
    debt_pressure: Mapped[float] = mapped_column(Numeric(6, 2))
    inventory_exposure: Mapped[float] = mapped_column(Numeric(6, 2))
    fuel_cost_sensitivity: Mapped[float] = mapped_column(Numeric(6, 2))
    analysis_summary: Mapped[str] = mapped_column(Text)
