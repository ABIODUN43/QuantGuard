from statistics import stdev


def estimate_garch_volatility(values: list[float]) -> dict:
    """Estimate volatility, using GARCH only when enough history and dependency support exist."""

    if len(values) < 2:
        return {"method": "insufficient_data", "volatility": 0}
    returns = []
    for previous, current in zip(values, values[1:]):
        if previous:
            returns.append((current - previous) / previous)
    if not returns:
        return {"method": "no_returns", "volatility": 0}
    if len(returns) >= 24:
        try:
            from arch import arch_model

            scaled = [value * 100 for value in returns]
            model = arch_model(scaled, mean="Constant", vol="GARCH", p=1, q=1, rescale=False)
            result = model.fit(disp="off")
            forecast = result.forecast(horizon=1)
            variance = float(forecast.variance.iloc[-1, 0])
            return {"method": "garch_1_1", "volatility": round((variance**0.5) / 100, 4)}
        except Exception:
            pass
    volatility = stdev(returns) if len(returns) > 1 else abs(returns[-1])
    return {"method": "ewma_fallback", "volatility": round(volatility, 4)}
