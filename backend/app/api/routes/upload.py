from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.financial_record import FinancialRecordCreate, FinancialRecordRead, UploadResponse
from app.schemas.pagination import Page
from app.services import upload_service

router = APIRouter(prefix="/data", tags=["financial data"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return await upload_service.process_upload(db, business, file)


@router.post("/manual-entry", response_model=FinancialRecordRead)
def manual_entry(
    payload: FinancialRecordCreate,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return upload_service.add_manual_record(db, business, payload)


@router.post("/demo-seed", response_model=UploadResponse)
def demo_seed(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return upload_service.seed_demo_records(db, business)


@router.get("/records")
def records(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    rows, total = upload_service.list_records(db, business, limit, offset)
    serialized = [FinancialRecordRead.model_validate(row).model_dump(mode="json") for row in rows]
    return {
        "items": serialized,
        "records": serialized,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
