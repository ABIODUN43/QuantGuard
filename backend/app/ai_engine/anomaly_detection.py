from statistics import mean, stdev


def detect_spikes(values: list[float], threshold: float = 2.0) -> list[int]:
    if len(values) < 3:
        return []
    avg = mean(values)
    deviation = stdev(values)
    if deviation == 0:
        return []
    return [index for index, value in enumerate(values) if abs(value - avg) / deviation >= threshold]


def detect_financial_anomalies(records: list[dict], threshold: float = 1.6) -> list[dict]:
    expenses = [float(row["operating_expenses"]) for row in records]
    revenue = [float(row["revenue"]) for row in records]
    anomalies: list[dict] = []
    for index in detect_spikes(expenses, threshold=threshold):
        anomalies.append(
            {
                "type": "expense_spike",
                "index": index,
                "date": records[index]["record_date"].isoformat(),
                "value": round(expenses[index], 2),
                "message": "Operating expenses spiked beyond the normal business range.",
            }
        )
    for index in range(1, len(revenue)):
        previous = revenue[index - 1]
        if previous > 0 and (revenue[index] - previous) / previous <= -0.18:
            anomalies.append(
                {
                    "type": "revenue_drop",
                    "index": index,
                    "date": records[index]["record_date"].isoformat(),
                    "value": round(revenue[index], 2),
                    "message": "Revenue dropped sharply compared with the previous period.",
                }
            )
    return anomalies
