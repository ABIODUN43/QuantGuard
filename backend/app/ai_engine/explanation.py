def explain_risk(breakdown: dict[str, float]) -> str:
    top = sorted(breakdown.items(), key=lambda item: item[1], reverse=True)[:3]
    labels = {
        "expense_instability": "expense volatility",
        "liquidity_weakness": "declining cash reserves",
        "inventory_exposure": "inventory exposure",
        "debt_pressure": "debt pressure",
        "revenue_volatility": "revenue volatility",
        "fuel_cost_sensitivity": "fuel and logistics sensitivity",
    }
    drivers = ", ".join(labels[key] for key, _ in top)
    return f"Business shows elevated financial vulnerability driven primarily by {drivers}."


def explain_contributions(contributions: dict[str, float]) -> str:
    labels = {
        "expense_instability": "expense instability",
        "liquidity_weakness": "liquidity weakness",
        "inventory_exposure": "inventory exposure",
        "debt_pressure": "debt pressure",
        "revenue_volatility": "revenue volatility",
        "fuel_cost_sensitivity": "fuel-cost sensitivity",
    }
    top = sorted(contributions.items(), key=lambda item: item[1], reverse=True)[:3]
    return "; ".join(f"{labels.get(key, key)} contributes {value:.1f}%" for key, value in top)
