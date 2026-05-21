from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FinancialRecordCreate(BaseModel):
    record_date: date
    revenue: float = Field(ge=0)
    operating_expenses: float = Field(ge=0)
    cost_of_goods_sold: float = Field(ge=0)
    inventory_value: float = Field(ge=0)
    debt_payment: float = Field(ge=0)
    cash_balance: float
    fuel_logistics_cost: float = Field(ge=0)
    other_income: float = Field(default=0, ge=0)


class FinancialRecordRead(FinancialRecordCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    business_id: UUID
    created_at: datetime


class UploadResponse(BaseModel):
    message: str
    records_processed: int
    status: str
