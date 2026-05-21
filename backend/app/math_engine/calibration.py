from __future__ import annotations

SECTOR_THRESHOLDS = {
    "default": {
        "revenue_volatility_midpoint": 0.14,
        "expense_instability_midpoint": 0.12,
        "fuel_sensitivity_midpoint": 0.13,
        "liquidity_safe_months": 3.0,
        "debt_pressure_midpoint": 0.22,
        "inventory_exposure_midpoint": 0.38,
    },
    "retail": {
        "revenue_volatility_midpoint": 0.12,
        "expense_instability_midpoint": 0.10,
        "fuel_sensitivity_midpoint": 0.12,
        "liquidity_safe_months": 3.0,
        "debt_pressure_midpoint": 0.20,
        "inventory_exposure_midpoint": 0.34,
    },
    "agriculture": {
        "revenue_volatility_midpoint": 0.22,
        "expense_instability_midpoint": 0.16,
        "fuel_sensitivity_midpoint": 0.18,
        "liquidity_safe_months": 4.0,
        "debt_pressure_midpoint": 0.24,
        "inventory_exposure_midpoint": 0.48,
    },
    "manufacturing": {
        "revenue_volatility_midpoint": 0.15,
        "expense_instability_midpoint": 0.11,
        "fuel_sensitivity_midpoint": 0.10,
        "liquidity_safe_months": 3.5,
        "debt_pressure_midpoint": 0.25,
        "inventory_exposure_midpoint": 0.45,
    },
    "logistics": {
        "revenue_volatility_midpoint": 0.14,
        "expense_instability_midpoint": 0.10,
        "fuel_sensitivity_midpoint": 0.08,
        "liquidity_safe_months": 3.0,
        "debt_pressure_midpoint": 0.23,
        "inventory_exposure_midpoint": 0.28,
    },
    "pharmacy": {
        "revenue_volatility_midpoint": 0.10,
        "expense_instability_midpoint": 0.09,
        "fuel_sensitivity_midpoint": 0.12,
        "liquidity_safe_months": 3.5,
        "debt_pressure_midpoint": 0.20,
        "inventory_exposure_midpoint": 0.42,
    },
}

DEFAULT_WEIGHTS = {
    "revenue_volatility": 0.16,
    "expense_instability": 0.21,
    "liquidity_weakness": 0.25,
    "debt_pressure": 0.13,
    "inventory_exposure": 0.13,
    "fuel_cost_sensitivity": 0.12,
}

SECTOR_WEIGHTS = {
    "retail": {
        "revenue_volatility": 0.17,
        "expense_instability": 0.20,
        "liquidity_weakness": 0.24,
        "debt_pressure": 0.12,
        "inventory_exposure": 0.17,
        "fuel_cost_sensitivity": 0.10,
    },
    "agriculture": {
        "revenue_volatility": 0.22,
        "expense_instability": 0.16,
        "liquidity_weakness": 0.24,
        "debt_pressure": 0.12,
        "inventory_exposure": 0.14,
        "fuel_cost_sensitivity": 0.12,
    },
    "manufacturing": {
        "revenue_volatility": 0.14,
        "expense_instability": 0.22,
        "liquidity_weakness": 0.23,
        "debt_pressure": 0.14,
        "inventory_exposure": 0.13,
        "fuel_cost_sensitivity": 0.14,
    },
    "logistics": {
        "revenue_volatility": 0.14,
        "expense_instability": 0.23,
        "liquidity_weakness": 0.24,
        "debt_pressure": 0.12,
        "inventory_exposure": 0.08,
        "fuel_cost_sensitivity": 0.19,
    },
    "pharmacy": {
        "revenue_volatility": 0.13,
        "expense_instability": 0.18,
        "liquidity_weakness": 0.25,
        "debt_pressure": 0.12,
        "inventory_exposure": 0.20,
        "fuel_cost_sensitivity": 0.12,
    },
}


def sector_key(sector: str | None) -> str:
    text = (sector or "").strip().lower()
    for key in SECTOR_THRESHOLDS:
        if key != "default" and key in text:
            return key
    if "retail" in text or "store" in text or "supermarket" in text:
        return "retail"
    if "agro" in text or "farm" in text:
        return "agriculture"
    return "default"


def thresholds_for_sector(sector: str | None) -> dict[str, float]:
    key = sector_key(sector)
    return {**SECTOR_THRESHOLDS["default"], **SECTOR_THRESHOLDS.get(key, {})}


def weights_for_sector(sector: str | None) -> dict[str, float]:
    weights = {**DEFAULT_WEIGHTS, **SECTOR_WEIGHTS.get(sector_key(sector), {})}
    total = sum(weights.values()) or 1
    return {key: value / total for key, value in weights.items()}
