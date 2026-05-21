from calendar import month_name
from datetime import date
from statistics import mean, stdev

from app.ai_engine.garch_model import estimate_garch_volatility


def _add_months(start: date, months: int) -> date:
    month = start.month - 1 + months
    year = start.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def _trend(values: list[float]) -> float:
    if len(values) < 2:
        return 0
    return (values[-1] - values[0]) / max(1, len(values) - 1)


def _safe_series_forecast(values: list[float], periods: int, allow_arima: bool = True) -> tuple[list[float], str]:
    if not values:
        return [0] * periods, "empty"
    if len(values) >= 12 and allow_arima:
        try:
            from statsmodels.tsa.arima.model import ARIMA

            model = ARIMA(values, order=(1, 1, 1))
            result = model.fit()
            return [max(0, float(value)) for value in result.forecast(periods)], "arima_1_1_1"
        except Exception:
            pass
    if len(values) >= 4:
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing

            model = ExponentialSmoothing(values, trend="add", seasonal=None, initialization_method="estimated")
            result = model.fit(optimized=True)
            return [max(0, float(value)) for value in result.forecast(periods)], "exponential_smoothing"
        except Exception:
            pass

    base = mean(values[-3:] or values)
    step = _trend(values)
    return [max(0, base + step * index) for index in range(1, periods + 1)], "linear_trend"


def cashflow_forecast(records: list[dict], months: int = 6) -> dict:
    if not records:
        return {"points": [], "model": "empty", "volatility": {"method": "insufficient_data", "volatility": 0}}

    latest = records[-1]
    revenue_values = [float(row["revenue"]) for row in records]
    expense_values = [float(row["operating_expenses"]) for row in records]
    revenue_forecast, revenue_model = _safe_series_forecast(revenue_values, months)
    expense_forecast, expense_model = _safe_series_forecast(expense_values, months)
    cash_balance = float(latest["cash_balance"])
    start_date = latest["record_date"]
    cash_volatility = estimate_garch_volatility([float(row["cash_balance"]) for row in records])
    interval_scale = max(
        stdev([(float(row["revenue"]) - float(row["operating_expenses"])) for row in records])
        if len(records) > 1
        else 0,
        cash_balance * cash_volatility["volatility"],
        1,
    )

    points = []
    for index in range(1, months + 1):
        record_date = _add_months(start_date, index)
        projected_revenue = revenue_forecast[index - 1]
        projected_expenses = expense_forecast[index - 1]
        cash_balance += projected_revenue - projected_expenses
        margin = interval_scale * (index**0.5)
        points.append(
            {
                "month": f"{month_name[record_date.month]} {record_date.year}",
                "projected_revenue": round(projected_revenue, 2),
                "projected_expenses": round(projected_expenses, 2),
                "projected_cash_balance": round(cash_balance, 2),
                "low_cash_balance": round(cash_balance - margin, 2),
                "high_cash_balance": round(cash_balance + margin, 2),
                "record_date": record_date,
            }
        )
    return {
        "points": points,
        "model": f"{revenue_model}_revenue__{expense_model}_expenses",
        "volatility": cash_volatility,
    }


def linear_cashflow_forecast(records: list[dict], months: int = 6) -> list[dict]:
    return cashflow_forecast(records, months=months)["points"]


def danger_period(forecast: list[dict]) -> tuple[date | None, date | None, str]:
    danger = [row for row in forecast if row["projected_cash_balance"] < 0 or row.get("low_cash_balance", 0) < 0]
    if not danger:
        return None, None, "No critical danger period detected"
    start = danger[0]["record_date"]
    end = danger[-1]["record_date"]
    return start, end, f"{month_name[start.month]} - {month_name[end.month]} {end.year}"
