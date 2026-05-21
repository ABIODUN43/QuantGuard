from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDTimestampMixin


class Report(UUIDTimestampMixin, Base):
    __tablename__ = "reports"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    analysis_id: Mapped[str | None] = mapped_column(ForeignKey("risk_analysis.id"), nullable=True)
    report_type: Mapped[str] = mapped_column(String(80))
    file_url: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(40), default="completed")
