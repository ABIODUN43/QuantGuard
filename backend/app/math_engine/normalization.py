import math


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def logistic_score(value: float, midpoint: float, steepness: float = 8) -> float:
    """Map a raw ratio to a 0-100 risk score."""

    score = 100 / (1 + math.exp(-steepness * (value - midpoint)))
    return round(clamp(score), 2)


def inverse_ratio_score(value: float, safe_level: float) -> float:
    """High score when a positive reserve/coverage ratio falls below safe level."""

    if safe_level <= 0:
        return 100
    weakness = max(0, safe_level - value) / safe_level
    return round(clamp(weakness * 100), 2)
