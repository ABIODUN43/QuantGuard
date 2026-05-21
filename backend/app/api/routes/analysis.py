from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business
from app.db.session import get_db
from app.models.business import Business
from app.schemas.analysis import AnalysisResponse
from app.services import analysis_service, background_jobs

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run", response_model=AnalysisResponse)
def run(
    background_tasks: BackgroundTasks,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    result = analysis_service.run_analysis(db, business)
    background_tasks.add_task(background_jobs.record_analysis_job, str(result["analysis_id"]))
    return result


@router.get("/latest", response_model=AnalysisResponse)
def latest(business: Business = Depends(get_current_business), db: Session = Depends(get_db)) -> dict:
    return analysis_service.latest_analysis(db, business)
