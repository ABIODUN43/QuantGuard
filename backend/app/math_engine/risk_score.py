from statistics import mean

from app.math_engine.calibration import thresholds_for_sector, weights_for_sector
from app.math_engine.liquidity import debt_pressure, inventory_exposure, liquidity_weakness
from app.math_engine.normalization import clamp, logistic_score
from app.math_engine.volatility import coefficient_of_variation

RISK_KEYS = (
    "expense_instability",
    "liquidity_weakness",
    "inventory_exposure",
    "debt_pressure",
    "revenue_volatility",
    "fuel_cost_sensitivity",
)


def compute_risk_breakdown(records: list[dict], sector: str | None = None) -> dict[str, float]:
    if not records:
        return {key: 0 for key in RISK_KEYS}

    thresholds = thresholds_for_sector(sector)
    revenue = [float(row["revenue"]) for row in records]
    expenses = [float(row["operating_expenses"]) for row in records]
    fuel = [float(row["fuel_logistics_cost"]) for row in records]
    latest = records[-1]

    revenue_volatility = logistic_score(
        coefficient_of_variation(revenue),
        midpoint=thresholds["revenue_volatility_midpoint"],
        steepness=12,
    )
    expense_instability = logistic_score(
        coefficient_of_variation(expenses),
        midpoint=thresholds["expense_instability_midpoint"],
        steepness=13,
    )
    fuel_sensitivity = logistic_score(
        coefficient_of_variation(fuel), midpoint=thresholds["fuel_sensitivity_midpoint"], steepness=10
    )

    return {
        "expense_instability": expense_instability,
        "liquidity_weakness": liquidity_weakness(
            float(latest["cash_balance"]),
            mean(expenses[-3:] or expenses),
            safe_months=thresholds["liquidity_safe_months"],
        ),
        "inventory_exposure": inventory_exposure(
            float(latest["inventory_value"]), revenue, midpoint=thresholds["inventory_exposure_midpoint"]
        ),
        "debt_pressure": debt_pressure(
            float(latest["debt_payment"]),
            float(latest["revenue"]),
            midpoint=thresholds["debt_pressure_midpoint"],
        ),
        "revenue_volatility": revenue_volatility,
        "fuel_cost_sensitivity": fuel_sensitivity,
    }


def composite_risk_score(breakdown: dict[str, float], sector: str | None = None) -> float:
    score = sum(breakdown[key] * weight for key, weight in weights_for_sector(sector).items())
    return round(clamp(score), 2)


def contribution_percentages(breakdown: dict[str, float], sector: str | None = None) -> dict[str, float]:
    weighted = {key: breakdown[key] * weight for key, weight in weights_for_sector(sector).items()}
    total = sum(weighted.values())
    if total <= 0:
        return {key: 0 for key in weighted}
    return {key: round(value / total * 100, 2) for key, value in weighted.items()}


def risk_level(score: float) -> str:
    if score <= 30:
        return "Low Risk"
    if score <= 60:
        return "Moderate Risk"
    if score <= 80:
        return "High Risk"
    return "Critical Risk"


def financial_stability_score(risk_score: float) -> float:
    return round(clamp(100 - risk_score), 2)
