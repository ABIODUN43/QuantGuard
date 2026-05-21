from statistics import mean

from app.math_engine.normalization import inverse_ratio_score, logistic_score


def liquidity_ratio(cash_balance: float, expected_expenses: float) -> float:
    if expected_expenses <= 0:
        return 999
    return cash_balance / expected_expenses


def liquidity_weakness(cash_balance: float, monthly_expenses: float, safe_months: float = 3) -> float:
    return inverse_ratio_score(liquidity_ratio(cash_balance, monthly_expenses), safe_level=safe_months)


def debt_pressure(debt_payment: float, revenue: float, midpoint: float = 0.22) -> float:
    if revenue <= 0:
        return 100
    return logistic_score(debt_payment / revenue, midpoint=midpoint, steepness=10)


def inventory_exposure(
    inventory_value: float, revenue_values: list[float], midpoint: float = 0.38
) -> float:
    avg_revenue = mean(revenue_values) if revenue_values else 0
    if avg_revenue <= 0:
        return 100
    return logistic_score(inventory_value / avg_revenue, midpoint=midpoint, steepness=7)
