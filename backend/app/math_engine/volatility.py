from statistics import mean, stdev


def coefficient_of_variation(values: list[float]) -> float:
    if len(values) < 2:
        return 0
    avg = mean(values)
    if avg == 0:
        return 0
    return abs(stdev(values) / avg)


def rolling_growth(values: list[float]) -> list[float]:
    growth: list[float] = []
    for previous, current in zip(values, values[1:]):
        if previous:
            growth.append((current - previous) / previous)
    return growth
