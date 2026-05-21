from uuid import uuid4

from sqlalchemy.orm import Session

from app.ai_engine.anomaly_detection import detect_financial_anomalies
from app.ai_engine.explanation import explain_contributions, explain_risk
from app.core.exceptions import not_found
from app.math_engine.risk_score import (
    composite_risk_score,
    contribution_percentages,
    compute_risk_breakdown,
    financial_stability_score,
    risk_level,
)
from app.math_engine.stress_probability import forecast_confidence, stress_probability
from app.models.business import Business
from app.models.financial_record import FinancialRecord
from app.models.risk_analysis import RiskAnalysis


def _record_dicts(records) -> list[dict]:
    return [
        {
            "record_date": row.record_date,
            "revenue": float(row.revenue),
            "operating_expenses": float(row.operating_expenses),
            "cost_of_goods_sold": float(row.cost_of_goods_sold),
            "inventory_value": float(row.inventory_value),
            "debt_payment": float(row.debt_payment),
            "cash_balance": float(row.cash_balance),
            "fuel_logistics_cost": float(row.fuel_logistics_cost),
            "other_income": float(row.other_income or 0),
        }
        for row in records
    ]


def serialize_analysis(row: RiskAnalysis, sector: str | None = None, anomalies: list[dict] | None = None) -> dict:
    breakdown = {
        "expense_instability": float(row.expense_instability),
        "liquidity_weakness": float(row.liquidity_weakness),
        "inventory_exposure": float(row.inventory_exposure),
        "debt_pressure": float(row.debt_pressure),
        "revenue_volatility": float(row.revenue_volatility),
        "fuel_cost_sensitivity": float(row.fuel_cost_sensitivity),
    }
    contributions = contribution_percentages(breakdown, sector)
    return {
        "analysis_id": row.id,
        "risk_score": float(row.risk_score),
        "stress_probability": float(row.stress_probability),
        "financial_stability_score": float(row.financial_stability_score),
        "forecast_confidence": float(row.forecast_confidence),
        "risk_level": row.risk_level,
        "risk_breakdown": breakdown,
        "contribution_percentages": contributions,
        "anomalies": anomalies or [],
        "model_notes": {
            "weighting": "sector_tuned_simulated_sme_weights",
            "contribution_summary": explain_contributions(contributions),
        },
        "summary": row.analysis_summary,
        "created_at": row.created_at,
    }


def run_analysis(db: Session, business: Business, records_override: list[dict] | None = None) -> dict:
    records = records_override
    if records_override is None:
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

    sector = f"{business.industry} {business.business_type}"
    anomalies = detect_financial_anomalies(records)
    breakdown = compute_risk_breakdown(records, sector)
    score = composite_risk_score(breakdown, sector)
    cash_balances = [float(row["cash_balance"]) for row in records]
    row = RiskAnalysis(
        id=str(uuid4()),
        business_id=business.id,
        risk_score=score,
        stress_probability=stress_probability(
            score,
            breakdown["liquidity_weakness"],
            cash_balances=cash_balances,
            anomaly_count=len(anomalies),
        ),
        financial_stability_score=financial_stability_score(score),
        forecast_confidence=forecast_confidence(len(records), score, anomaly_count=len(anomalies)),
        risk_level=risk_level(score),
        revenue_volatility=breakdown["revenue_volatility"],
        expense_instability=breakdown["expense_instability"],
        liquidity_weakness=breakdown["liquidity_weakness"],
        debt_pressure=breakdown["debt_pressure"],
        inventory_exposure=breakdown["inventory_exposure"],
        fuel_cost_sensitivity=breakdown["fuel_cost_sensitivity"],
        analysis_summary=f"{explain_risk(breakdown)} {explain_contributions(contribution_percentages(breakdown, sector))}.",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize_analysis(row, sector=sector, anomalies=anomalies)


def latest_analysis(db: Session, business: Business) -> dict:
    analysis = (
        db.query(RiskAnalysis)
        .filter(RiskAnalysis.business_id == business.id)
        .filter(RiskAnalysis.deleted_at.is_(None))
        .order_by(RiskAnalysis.created_at.desc())
        .first()
    )
    return serialize_analysis(analysis, sector=f"{business.industry} {business.business_type}") if analysis else run_analysis(db, business)
