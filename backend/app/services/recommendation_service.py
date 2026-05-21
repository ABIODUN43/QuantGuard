from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.recommendation import Recommendation
from app.services.analysis_service import latest_analysis


def serialize_recommendation(row: Recommendation) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "description": row.description,
        "priority": row.priority,
        "impact": row.impact,
        "category": row.category,
        "created_at": row.created_at,
    }


def generate_recommendations(db: Session, business: Business) -> list[dict]:
    analysis = latest_analysis(db, business)
    breakdown = analysis["risk_breakdown"]
    rows: list[Recommendation] = []

    def add(title: str, description: str, priority: str, impact: str, category: str) -> None:
        rows.append(
            Recommendation(
                id=str(uuid4()),
                business_id=business.id,
                analysis_id=str(analysis["analysis_id"]),
                title=title,
                description=description,
                priority=priority,
                impact=impact,
                category=category,
            )
        )

    if breakdown["liquidity_weakness"] > 60:
        add(
            "Preserve Cash Reserves",
            "Build reserves to cover at least 3 months of operating expenses.",
            "High",
            "High",
            "Liquidity",
        )
    if breakdown["inventory_exposure"] > 55:
        add(
            "Reduce Inventory Exposure",
            "Inventory levels are above optimal. Reduce holding cost and obsolescence risk.",
            "High",
            "High",
            "Inventory",
        )
    if breakdown["expense_instability"] > 55:
        add(
            "Negotiate Better Payment Terms",
            "Reduce expense volatility by renegotiating supplier terms and payment cycles.",
            "Medium",
            "High",
            "Expenses",
        )
    if breakdown["fuel_cost_sensitivity"] > 55:
        add(
            "Monitor Fuel and Logistics Costs",
            "Optimize routes and fuel suppliers to limit logistics volatility.",
            "Medium",
            "Medium",
            "Macroeconomic",
        )
    if not rows:
        add(
            "Maintain Current Controls",
            "Your risk profile is stable. Continue monitoring liquidity and revenue trends.",
            "Low",
            "Medium",
            "Operations",
        )

    for row in rows:
        db.add(row)
    db.commit()
    return [serialize_recommendation(row) for row in rows]


def get_recommendations(db: Session, business: Business, limit: int, offset: int) -> tuple[list[dict], int]:
    query = db.query(Recommendation).filter(
        Recommendation.business_id == business.id, Recommendation.deleted_at.is_(None)
    )
    if query.count() == 0:
        generate_recommendations(db, business)
        query = db.query(Recommendation).filter(
            Recommendation.business_id == business.id, Recommendation.deleted_at.is_(None)
        )
    total = query.count()
    rows = query.order_by(Recommendation.created_at.desc()).offset(offset).limit(limit).all()
    return [serialize_recommendation(row) for row in rows], total
