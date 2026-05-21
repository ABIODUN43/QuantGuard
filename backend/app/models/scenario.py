from sqlalchemy import ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class Scenario(UUIDTimestampMixin, Base):
    __tablename__ = "scenarios"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    scenario_name: Mapped[str] = mapped_column(String(160))
    scenario_type: Mapped[str] = mapped_column(String(80))
    input_changes: Mapped[dict] = mapped_column(JSON)
    result_summary: Mapped[dict] = mapped_column(JSON)
    risk_score: Mapped[float] = mapped_column(Numeric(6, 2))
    stress_probability: Mapped[float] = mapped_column(Numeric(5, 4))
    cash_shortfall_probability: Mapped[float] = mapped_column(Numeric(5, 4))
