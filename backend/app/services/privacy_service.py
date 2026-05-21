from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.financial_record import FinancialRecord
from app.models.forecast import Forecast
from app.models.recommendation import Recommendation
from app.models.report import Report
from app.models.risk_analysis import RiskAnalysis
from app.models.scenario import Scenario
from app.models.user import User
from app.services.audit_service import record_audit


def export_account_data(db: Session, user: User, business: Business | None = None) -> dict:
    payload: dict = {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        },
        "business": None,
        "financial_records": [],
        "risk_analysis": [],
        "forecasts": [],
        "recommendations": [],
        "scenarios": [],
        "reports": [],
    }
    if business:
        payload["business"] = {
            "id": business.id,
            "business_name": business.business_name,
            "industry": business.industry,
            "business_type": business.business_type,
            "country": business.country,
            "state": business.state,
            "city": business.city,
            "average_monthly_revenue": float(business.average_monthly_revenue),
            "average_monthly_expenses": float(business.average_monthly_expenses),
            "created_at": business.created_at,
        }
        bid = business.id
        payload["financial_records"] = [
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
            for row in db.query(FinancialRecord).filter(FinancialRecord.business_id == bid).all()
        ]
        payload["risk_analysis"] = [
            {"risk_score": float(row.risk_score), "risk_level": row.risk_level, "created_at": row.created_at}
            for row in db.query(RiskAnalysis).filter(RiskAnalysis.business_id == bid).all()
        ]
        payload["forecasts"] = [
            {"projected_cash_balance": float(row.projected_cash_balance), "created_at": row.created_at}
            for row in db.query(Forecast).filter(Forecast.business_id == bid).all()
        ]
        payload["recommendations"] = [
            {"title": row.title, "priority": row.priority, "impact": row.impact, "category": row.category}
            for row in db.query(Recommendation).filter(Recommendation.business_id == bid).all()
        ]
        payload["scenarios"] = [
            {"scenario_name": row.scenario_name, "risk_score": float(row.risk_score), "created_at": row.created_at}
            for row in db.query(Scenario).filter(Scenario.business_id == bid).all()
        ]
        payload["reports"] = [
            {"report_type": row.report_type, "file_url": row.file_url, "created_at": row.created_at}
            for row in db.query(Report).filter(Report.business_id == bid).all()
        ]
    record_audit(db, "data_export", "privacy", user_id=user.id, business_id=business.id if business else None)
    return payload


def soft_delete_account(db: Session, user: User, business: Business | None = None) -> dict:
    now = datetime.now(timezone.utc)
    user.deleted_at = now
    user.is_active = False
    if business:
        business.deleted_at = now
        for model in [FinancialRecord, RiskAnalysis, Forecast, Recommendation, Scenario, Report]:
            db.query(model).filter(model.business_id == business.id).update({"deleted_at": now})
    db.commit()
    record_audit(db, "account_deleted", "privacy", user_id=user.id, business_id=business.id if business else None)
    return {"message": "Account and business data were queued for deletion", "deleted_at": now}
