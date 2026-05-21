from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.pagination import Page
from app.schemas.report import ReportGenerateRequest, ReportGenerateResponse, ReportRead
from app.services import background_jobs, report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/templates")
def templates() -> dict:
    return report_service.list_report_templates()


@router.post("/generate", response_model=ReportGenerateResponse)
def generate(
    payload: ReportGenerateRequest,
    background_tasks: BackgroundTasks,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    result = report_service.generate_report(db, business, payload.report_type, payload.format)
    background_tasks.add_task(background_jobs.record_report_job, str(result["report_id"]))
    return result


@router.get("")
def reports(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    rows, total = report_service.list_reports(db, business, limit, offset)
    serialized = [ReportRead.model_validate(row).model_dump(mode="json") for row in rows]
    return {"items": serialized, "reports": serialized, "total": total, "limit": limit, "offset": offset}
