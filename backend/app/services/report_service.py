from uuid import uuid4
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import bad_request
from app.models.business import Business
from app.models.report import Report
from app.models.scenario import Scenario
from app.reports.excel_exporter import generate_excel_report
from app.reports.pdf_generator import generate_pdf_report
from app.services.analysis_service import latest_analysis
from app.services.forecast_service import latest_forecast
from app.services.recommendation_service import get_recommendations
from app.services.scenario_service import serialize_scenario


REPORT_TEMPLATES = {
    "risk": {
        "key": "risk",
        "title": "Risk Intelligence Report",
        "description": "Risk score, drivers, contributions, and recommended controls.",
    },
    "risk_assessment": {
        "key": "risk_assessment",
        "title": "Risk Assessment Report",
        "description": "Formal risk assessment for operational decision making.",
    },
    "forecast": {
        "key": "forecast",
        "title": "Cashflow Forecast Report",
        "description": "Projected cash balance, shortfall probability, and danger periods.",
    },
    "scenario": {
        "key": "scenario",
        "title": "Scenario Simulation Report",
        "description": "Latest what-if simulation and estimated business impact.",
    },
    "lender": {
        "key": "lender",
        "title": "Lender Readiness Report",
        "description": "Business profile, risk posture, cashflow outlook, and credit-facing summary.",
    },
}


def _business_payload(business: Business) -> dict:
    return {
        "id": business.id,
        "business_name": business.business_name,
        "business_type": business.business_type,
        "industry": business.industry,
        "country": business.country,
        "state": business.state,
        "city": business.city,
        "years_in_operation": business.years_in_operation,
        "number_of_employees": business.number_of_employees,
        "average_monthly_revenue": float(business.average_monthly_revenue),
        "average_monthly_expenses": float(business.average_monthly_expenses),
    }


def _latest_scenario(db: Session, business: Business) -> dict | None:
    row = (
        db.query(Scenario)
        .filter(Scenario.business_id == business.id, Scenario.deleted_at.is_(None))
        .order_by(Scenario.created_at.desc())
        .first()
    )
    return serialize_scenario(row) if row else None


def _report_payload(db: Session, business: Business, report_type: str) -> dict:
    template = REPORT_TEMPLATES.get(report_type)
    if not template:
        raise bad_request(f"Unsupported report type: {report_type}")
    analysis = latest_analysis(db, business)
    forecast = latest_forecast(db, business)
    recommendations, _ = get_recommendations(db, business, limit=20, offset=0)
    return {
        "template": template,
        "business": _business_payload(business),
        "analysis": analysis,
        "forecast": forecast,
        "recommendations": recommendations,
        "scenario": _latest_scenario(db, business),
    }


def generate_report(db: Session, business: Business, report_type: str, report_format: str) -> dict:
    normalized_type = "risk" if report_type == "risk_assessment" else report_type
    payload_type = report_type if report_type in REPORT_TEMPLATES else normalized_type
    payload = _report_payload(db, business, payload_type)
    report_id = str(uuid4())
    extension = "xlsx" if report_format.lower() in {"excel", "xlsx"} else "pdf"
    storage_dir = Path(settings.report_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)
    safe_type = payload["template"]["key"]
    filename = f"{safe_type}_{report_id}.{extension}"
    output_path = storage_dir / filename

    if extension == "xlsx":
        generate_excel_report(payload, output_path)
    elif extension == "pdf":
        generate_pdf_report(payload, output_path)
    else:
        raise bad_request(f"Unsupported report format: {report_format}")

    report = Report(
        id=report_id,
        business_id=business.id,
        analysis_id=str(payload["analysis"]["analysis_id"]),
        report_type=payload["template"]["key"],
        file_url=f"/reports/{filename}",
        status="completed",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {
        "message": "Report generated successfully",
        "report_id": report_id,
        "download_url": report.file_url,
    }


def list_report_templates() -> dict:
    return {"templates": list(REPORT_TEMPLATES.values()), "storage": "local", "cloud_storage": "planned"}


def list_reports(db: Session, business: Business, limit: int, offset: int) -> tuple[list[Report], int]:
    query = db.query(Report).filter(Report.business_id == business.id, Report.deleted_at.is_(None))
    total = query.count()
    rows = query.order_by(Report.created_at.desc()).offset(offset).limit(limit).all()
    return rows, total
