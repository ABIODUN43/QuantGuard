from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportGenerateRequest(BaseModel):
    report_type: Literal["risk", "forecast", "scenario", "lender", "risk_assessment"] = "risk"
    format: Literal["pdf", "excel", "xlsx"] = "pdf"


class ReportGenerateResponse(BaseModel):
    message: str
    report_id: UUID
    download_url: str


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    report_type: str
    file_url: str
    status: str
    created_at: datetime
