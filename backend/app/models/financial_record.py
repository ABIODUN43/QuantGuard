from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class FinancialRecord(UUIDTimestampMixin, Base):
    __tablename__ = "financial_records"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    record_date: Mapped[date] = mapped_column(Date, index=True)
    revenue: Mapped[float] = mapped_column(Numeric(14, 2))
    operating_expenses: Mapped[float] = mapped_column(Numeric(14, 2))
    cost_of_goods_sold: Mapped[float] = mapped_column(Numeric(14, 2))
    inventory_value: Mapped[float] = mapped_column(Numeric(14, 2))
    debt_payment: Mapped[float] = mapped_column(Numeric(14, 2))
    cash_balance: Mapped[float] = mapped_column(Numeric(14, 2))
    fuel_logistics_cost: Mapped[float] = mapped_column(Numeric(14, 2))
    other_income: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
