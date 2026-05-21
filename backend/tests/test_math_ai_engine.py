from datetime import date

from app.ai_engine.anomaly_detection import detect_financial_anomalies
from app.ai_engine.forecasting import cashflow_forecast, danger_period
from app.ai_engine.garch_model import estimate_garch_volatility
from app.math_engine.calibration import thresholds_for_sector, weights_for_sector
from app.math_engine.normalization import inverse_ratio_score, logistic_score
from app.math_engine.risk_score import (
    composite_risk_score,
    contribution_percentages,
    compute_risk_breakdown,
    risk_level,
)
from app.math_engine.stress_probability import forecast_confidence, stress_probability


def sample_records() -> list[dict]:
    rows = [
        ("2025-12-01", 2_100_000, 1_480_000, 980_000, 760_000, 240_000, 1_900_000, 180_000),
        ("2026-01-01", 2_450_000, 1_870_000, 1_120_000, 850_000, 230_000, 1_680_000, 250_000),
        ("2026-02-01", 2_780_000, 1_920_000, 1_250_000, 880_000, 220_000, 1_540_000, 260_000),
        ("2026-03-01", 2_620_000, 1_950_000, 1_180_000, 900_000, 210_000, 1_390_000, 275_000),
        ("2026-04-01", 2_350_000, 2_180_000, 1_070_000, 990_000, 205_000, 1_090_000, 315_000),
        ("2026-05-01", 1_760_000, 3_420_000, 1_120_000, 1_030_000, 200_000, 750_000, 340_000),
    ]
    return [
        {
            "record_date": date.fromisoformat(row[0]),
            "revenue": row[1],
            "operating_expenses": row[2],
            "cost_of_goods_sold": row[3],
            "inventory_value": row[4],
            "debt_payment": row[5],
            "cash_balance": row[6],
            "fuel_logistics_cost": row[7],
            "other_income": 0,
        }
        for row in rows
    ]


def test_normalization_scores_stay_bounded() -> None:
    assert 0 <= logistic_score(0.2, midpoint=0.1) <= 100
    assert inverse_ratio_score(1, safe_level=3) > inverse_ratio_score(2, safe_level=3)


def test_sector_thresholds_and_weights_are_normalized() -> None:
    retail = thresholds_for_sector("Retail Trade")
    assert retail["inventory_exposure_midpoint"] < thresholds_for_sector(None)["inventory_exposure_midpoint"]
    assert round(sum(weights_for_sector("Retail Trade").values()), 6) == 1


def test_risk_breakdown_and_contributions() -> None:
    breakdown = compute_risk_breakdown(sample_records(), "Retail Trade")
    score = composite_risk_score(breakdown, "Retail Trade")
    contributions = contribution_percentages(breakdown, "Retail Trade")
    assert 0 <= score <= 100
    assert risk_level(score) in {"Low Risk", "Moderate Risk", "High Risk", "Critical Risk"}
    assert round(sum(contributions.values())) == 100


def test_stress_probability_responds_to_cash_trend_and_anomalies() -> None:
    base = stress_probability(60, 60, cash_balances=[2_000_000, 1_900_000, 1_850_000], anomaly_count=0)
    stressed = stress_probability(60, 60, cash_balances=[2_000_000, 1_500_000, 900_000], anomaly_count=2)
    assert stressed > base
    assert forecast_confidence(6, 80, anomaly_count=2) < forecast_confidence(6, 80, anomaly_count=0)


def test_detects_expense_spikes_and_revenue_drops() -> None:
    anomalies = detect_financial_anomalies(sample_records())
    anomaly_types = {item["type"] for item in anomalies}
    assert "expense_spike" in anomaly_types
    assert "revenue_drop" in anomaly_types


def test_cashflow_forecast_contains_series_and_intervals() -> None:
    result = cashflow_forecast(sample_records(), months=4)
    points = result["points"]
    assert len(points) == 4
    assert points[0]["month"]
    assert "low_cash_balance" in points[0]
    assert result["model"]
    start, end, label = danger_period(points)
    assert label
    assert (start is None and end is None) or start <= end


def test_garch_uses_fallback_until_enough_history() -> None:
    result = estimate_garch_volatility([100, 110, 105, 115])
    assert result["method"] in {"ewma_fallback", "insufficient_data", "no_returns"}
    assert result["volatility"] >= 0
