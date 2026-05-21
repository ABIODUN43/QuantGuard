from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, JSON, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class Forecast(UUIDTimestampMixin, Base):
    __tablename__ = "forecasts"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    analysis_id: Mapped[str] = mapped_column(ForeignKey("risk_analysis.id"))
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, default=180)
    projected_cash_balance: Mapped[float] = mapped_column(Numeric(14, 2))
    cash_shortfall_probability: Mapped[float] = mapped_column(Numeric(5, 4))
    forecast_confidence: Mapped[float] = mapped_column(Numeric(5, 4), default=0)
    danger_period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    danger_period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    breakeven_revenue: Mapped[float] = mapped_column(Numeric(14, 2))
    forecast_data: Mapped[dict] = mapped_column(JSON)
