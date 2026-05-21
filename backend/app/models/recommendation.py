from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class Recommendation(UUIDTimestampMixin, Base):
    __tablename__ = "recommendations"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    analysis_id: Mapped[str] = mapped_column(ForeignKey("risk_analysis.id"))
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(40))
    impact: Mapped[str] = mapped_column(String(40))
    category: Mapped[str] = mapped_column(String(80))
