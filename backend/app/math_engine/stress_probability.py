import math

from app.math_engine.normalization import clamp
from app.math_engine.volatility import rolling_growth


def stress_probability(
    risk_score: float,
    liquidity_weakness: float,
    cash_balances: list[float] | None = None,
    anomaly_count: int = 0,
) -> float:
    cash_trend_penalty = 0
    if cash_balances and len(cash_balances) >= 3:
        growth = rolling_growth(cash_balances[-4:])
        negative_trend = sum(1 for value in growth if value < -0.05)
        cash_trend_penalty = negative_trend * 0.18

    blended = (risk_score * 0.055) + (liquidity_weakness * 0.035) + cash_trend_penalty
    blended += min(0.55, anomaly_count * 0.08)
    probability = 1 / (1 + math.exp(-(blended - 4.25)))
    return round(clamp(probability, 0.02, 0.98), 2)


def forecast_confidence(record_count: int, risk_score: float, anomaly_count: int = 0) -> float:
    data_confidence = min(0.95, 0.55 + record_count * 0.045)
    uncertainty_penalty = max(0, risk_score - 70) * 0.0015
    anomaly_penalty = min(0.12, anomaly_count * 0.025)
    return round(max(0.45, data_confidence - uncertainty_penalty - anomaly_penalty), 2)
