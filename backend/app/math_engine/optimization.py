from statistics import stdev


def required_cash_buffer(records: list[dict], reserve_months: int = 3) -> dict[str, float]:
    expenses = [float(row["operating_expenses"]) for row in records]
    if not expenses:
        return {
            "required_cash_buffer": 0,
            "recommended_reserve_months": reserve_months,
            "inventory_reduction_percent": 0,
        }
    avg_expense = sum(expenses) / len(expenses)
    volatility = stdev(expenses) if len(expenses) > 1 else 0
    required = avg_expense * reserve_months + volatility
    return {
        "required_cash_buffer": round(required, 2),
        "recommended_reserve_months": reserve_months,
        "inventory_reduction_percent": 15,
    }
