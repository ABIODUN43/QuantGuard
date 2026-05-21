from uuid import uuid4

from sqlalchemy.orm import Session

from app.ai_engine.scenario_model import apply_scenario
from app.core.exceptions import not_found
from app.ai_engine.anomaly_detection import detect_financial_anomalies
from app.math_engine.risk_score import composite_risk_score, compute_risk_breakdown
from app.math_engine.stress_probability import stress_probability
from app.models.business import Business
from app.models.financial_record import FinancialRecord
from app.models.scenario import Scenario
from app.schemas.scenario import ScenarioRunRequest
from app.services.analysis_service import _record_dicts


def serialize_scenario(row: Scenario) -> dict:
    summary = row.result_summary or {}
    return {
        "scenario_id": row.id,
        "scenario_name": row.scenario_name,
        "risk_score": float(row.risk_score),
        "stress_probability": float(row.stress_probability),
        "cash_shortfall_probability": float(row.cash_shortfall_probability),
        "impact": summary.get("impact", "Unknown"),
        "summary": summary.get("summary", ""),
        "created_at": row.created_at,
    }


def run_scenario(db: Session, business: Business, payload: ScenarioRunRequest) -> dict:
    record_models = (
        db.query(FinancialRecord)
        .filter(FinancialRecord.business_id == business.id)
        .filter(FinancialRecord.deleted_at.is_(None), FinancialRecord.archived_at.is_(None))
        .order_by(FinancialRecord.record_date.asc())
        .all()
    )
    records = _record_dicts(record_models)
    if not records:
        raise not_found("No financial records found")
    adjusted = apply_scenario(records, payload.changes.model_dump())
    sector = f"{business.industry} {business.business_type}"
    breakdown = compute_risk_breakdown(adjusted, sector)
    score = composite_risk_score(breakdown, sector)
    anomalies = detect_financial_anomalies(adjusted)
    probability = stress_probability(
        score,
        breakdown["liquidity_weakness"],
        cash_balances=[float(row["cash_balance"]) for row in adjusted],
        anomaly_count=len(anomalies),
    )
    cash_shortfall = min(0.95, probability + 0.1)
    impact = "High Negative" if score >= 75 else "Moderate Negative" if score >= 55 else "Positive"
    row = Scenario(
        id=str(uuid4()),
        business_id=business.id,
        scenario_name=payload.scenario_name,
        scenario_type=payload.scenario_name,
        input_changes=payload.changes.model_dump(),
        result_summary={
            "impact": impact,
            "summary": f"{payload.scenario_name} changes the business risk profile to {impact.lower()}.",
        },
        risk_score=score,
        stress_probability=probability,
        cash_shortfall_probability=round(cash_shortfall, 2),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize_scenario(row)
