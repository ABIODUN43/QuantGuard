from datetime import date

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class EconomicIndicator(UUIDTimestampMixin, Base):
    __tablename__ = "economic_indicators"

    country: Mapped[str] = mapped_column(String(80), index=True)
    indicator_name: Mapped[str] = mapped_column(String(120), index=True)
    indicator_value: Mapped[float] = mapped_column(Numeric(14, 4))
    unit: Mapped[str] = mapped_column(String(40))
    source: Mapped[str] = mapped_column(String(120), default="manual")
    record_date: Mapped[date] = mapped_column(Date, index=True)
