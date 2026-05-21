from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class Business(UUIDTimestampMixin, Base):
    __tablename__ = "businesses"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    business_name: Mapped[str] = mapped_column(String(180))
    business_type: Mapped[str] = mapped_column(String(100))
    industry: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(80))
    state: Mapped[str] = mapped_column(String(80))
    city: Mapped[str] = mapped_column(String(80))
    years_in_operation: Mapped[int] = mapped_column(Integer)
    number_of_employees: Mapped[int] = mapped_column(Integer)
    average_monthly_revenue: Mapped[float] = mapped_column(Numeric(14, 2))
    average_monthly_expenses: Mapped[float] = mapped_column(Numeric(14, 2))
