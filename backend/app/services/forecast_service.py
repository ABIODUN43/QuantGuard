from statistics import mean
from uuid import uuid4

from sqlalchemy.orm import Session

from app.ai_engine.forecasting import cashflow_forecast, danger_period
from app.core.exceptions import not_found
from app.models.business import Business
from app.models.financial_record import FinancialRecord
from app.models.forecast import Forecast
from app.services.analysis_service import latest_analysis
from app.services.analysis_service import _record_dicts


def serialize_forecast(row: Forecast) -> dict:
    data = row.forecast_data or {}
    return {
        "forecast_id": row.id,
        "analysis_id": row.analysis_id,
        "projected_cash_balance": float(row.projected_cash_balance),
        "cash_shortfall_probability": float(row.cash_shortfall_probability),
        "forecast_confidence": float(row.forecast_confidence),
        "danger_period_start": row.danger_period_start,
        "danger_period_end": row.danger_period_end,
        "danger_period": data.get("danger_period", "No critical danger period detected"),
        "breakeven_revenue": float(row.breakeven_revenue),
        "cashflow_forecast": data.get("cashflow_forecast", []),
        "model": data.get("model"),
        "confidence_interval_note": data.get("confidence_interval_note"),
        "volatility": data.get("volatility"),
        "created_at": row.created_at,
    }


def latest_forecast(db: Session, business: Business) -> dict:
    existing = (
        db.query(Forecast)
        .filter(Forecast.business_id == business.id)
        .filter(Forecast.deleted_at.is_(None))
        .order_by(Forecast.created_at.desc())
        .first()
    )
    if existing:
        return serialize_forecast(existing)

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
    analysis = latest_analysis(db, business)
    forecast_result = cashflow_forecast(records)
    forecast = forecast_result["points"]
    start, end, label = danger_period(forecast)
    forecast_json = [{k: v for k, v in row.items() if k != "record_date"} for row in forecast]
    expenses = [float(row["operating_expenses"]) for row in records[-3:]]
    revenue = [float(row["revenue"]) for row in records[-3:]]
    breakeven = mean(expenses) * 1.18 if expenses else 0
    latest_cash = forecast[-1]["projected_cash_balance"] if forecast else records[-1]["cash_balance"]
    cash_shortfall_probability = max(
        0.1,
        min(0.95, analysis["stress_probability"] - (0.18 if latest_cash > 0 else -0.1)),
    )
    row = Forecast(
        id=str(uuid4()),
        business_id=business.id,
        analysis_id=str(analysis["analysis_id"]),
        forecast_horizon_days=180,
        projected_cash_balance=round(latest_cash, 2),
        cash_shortfall_probability=round(cash_shortfall_probability, 2),
        forecast_confidence=analysis["forecast_confidence"],
        danger_period_start=start,
        danger_period_end=end,
        breakeven_revenue=round(max(breakeven, mean(revenue) if revenue else 0), 2),
        forecast_data={
            "danger_period": label,
            "cashflow_forecast": forecast_json,
            "model": forecast_result["model"],
            "volatility": forecast_result["volatility"],
            "confidence_interval_note": "Low/high ranges are approximate 80% planning bands from cashflow volatility.",
        },
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize_forecast(row)
