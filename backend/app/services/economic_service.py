from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.economic_indicator import EconomicIndicator
from app.schemas.economic import EconomicIndicatorCreate


PUBLIC_SOURCES = [
    {
        "name": "Central Bank of Nigeria (CBN)",
        "status": "planned",
        "note": "Use later for FX, interest rate, and monetary policy indicators.",
    },
    {
        "name": "National Bureau of Statistics (NBS)",
        "status": "planned",
        "note": "Use later for inflation, CPI, unemployment, and sector data.",
    },
    {
        "name": "World Bank",
        "status": "planned",
        "note": "Use later for macroeconomic and development indicators.",
    },
    {
        "name": "International Monetary Fund (IMF)",
        "status": "planned",
        "note": "Use later for economic outlook and international financial statistics.",
    },
]


def add_indicator(db: Session, payload: EconomicIndicatorCreate) -> EconomicIndicator:
    row = EconomicIndicator(
        id=str(uuid4()),
        country=payload.country,
        indicator_name=payload.indicator_name,
        indicator_value=payload.indicator_value,
        unit=payload.unit,
        source=payload.source,
        record_date=payload.record_date,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def seed_economic_history(db: Session, country: str = "Nigeria") -> dict:
    rows = [
        ("2025-12-01", "Inflation Rate", 24.3, "%"),
        ("2026-01-01", "Inflation Rate", 23.7, "%"),
        ("2026-02-01", "Inflation Rate", 23.1, "%"),
        ("2026-03-01", "Inflation Rate", 22.8, "%"),
        ("2026-04-01", "Inflation Rate", 22.4, "%"),
        ("2026-05-01", "Inflation Rate", 22.1, "%"),
        ("2025-12-01", "Official USD/NGN", 1468.5, "NGN"),
        ("2026-01-01", "Official USD/NGN", 1438.2, "NGN"),
        ("2026-02-01", "Official USD/NGN", 1418.9, "NGN"),
        ("2026-03-01", "Official USD/NGN", 1388.6, "NGN"),
        ("2026-04-01", "Official USD/NGN", 1343.79, "NGN"),
        ("2026-05-01", "Official USD/NGN", 1374.69, "NGN"),
        ("2025-12-01", "Parallel USD/NGN", 1495.0, "NGN"),
        ("2026-01-01", "Parallel USD/NGN", 1468.0, "NGN"),
        ("2026-02-01", "Parallel USD/NGN", 1442.0, "NGN"),
        ("2026-03-01", "Parallel USD/NGN", 1410.0, "NGN"),
        ("2026-04-01", "Parallel USD/NGN", 1370.0, "NGN"),
        ("2026-05-01", "Parallel USD/NGN", 1400.0, "NGN"),
        ("2025-12-01", "USD/NGN Spread", 26.5, "NGN"),
        ("2026-01-01", "USD/NGN Spread", 29.8, "NGN"),
        ("2026-02-01", "USD/NGN Spread", 23.1, "NGN"),
        ("2026-03-01", "USD/NGN Spread", 21.4, "NGN"),
        ("2026-04-01", "USD/NGN Spread", 26.21, "NGN"),
        ("2026-05-01", "USD/NGN Spread", 25.31, "NGN"),
        ("2025-12-01", "Fuel Price Index", 106.4, "index"),
        ("2026-01-01", "Fuel Price Index", 110.2, "index"),
        ("2026-02-01", "Fuel Price Index", 114.9, "index"),
        ("2026-03-01", "Fuel Price Index", 116.5, "index"),
        ("2026-04-01", "Fuel Price Index", 118.6, "index"),
        ("2026-05-01", "Fuel Price Index", 123.1, "index"),
        ("2025-12-01", "Interest Rate", 27.0, "%"),
        ("2026-01-01", "Interest Rate", 27.0, "%"),
        ("2026-02-01", "Interest Rate", 26.5, "%"),
        ("2026-03-01", "Interest Rate", 26.5, "%"),
        ("2026-04-01", "Interest Rate", 26.0, "%"),
        ("2026-05-01", "Interest Rate", 26.0, "%"),
        ("2025-12-01", "Business Confidence", 58.0, "/100"),
        ("2026-01-01", "Business Confidence", 59.0, "/100"),
        ("2026-02-01", "Business Confidence", 60.0, "/100"),
        ("2026-03-01", "Business Confidence", 61.0, "/100"),
        ("2026-04-01", "Business Confidence", 62.0, "/100"),
        ("2026-05-01", "Business Confidence", 63.0, "/100"),
    ]
    from datetime import date

    existing_keys = {
        (row.indicator_name, row.record_date)
        for row in db.query(EconomicIndicator).filter(EconomicIndicator.country == country).all()
    }
    processed = 0
    for record_date, name, value, unit in rows:
        parsed_date = date.fromisoformat(record_date)
        if (name, parsed_date) in existing_keys:
            continue
        db.add(
            EconomicIndicator(
                id=str(uuid4()),
                country=country,
                indicator_name=name,
                indicator_value=value,
                unit=unit,
                source="manual_seed",
                record_date=parsed_date,
            )
        )
        processed += 1
    db.commit()
    return {"message": "Economic history seeded", "records_processed": processed, "status": "processed"}


def _latest_by_indicator(rows: list[EconomicIndicator]) -> list[EconomicIndicator]:
    latest: dict[str, EconomicIndicator] = {}
    for row in sorted(rows, key=lambda item: item.record_date, reverse=True):
        latest.setdefault(row.indicator_name, row)
    return sorted(latest.values(), key=lambda item: item.indicator_name)


def _is_legacy_fx(row: EconomicIndicator) -> bool:
    return row.indicator_name == "USD/NGN Exchange Rate"


def _history(rows: list[EconomicIndicator]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for row in sorted(rows, key=lambda item: (item.indicator_name, item.record_date)):
        if _is_legacy_fx(row):
            continue
        grouped.setdefault(row.indicator_name, []).append({"date": row.record_date, "value": float(row.indicator_value)})
    return grouped


def _trend(history: list[dict]) -> float:
    if len(history) < 2:
        return 0
    previous = float(history[-2]["value"])
    current = float(history[-1]["value"])
    if previous == 0:
        return 0
    return (current - previous) / previous


def _trend_label(trend: float) -> str:
    if abs(trend) < 0.001:
        return "No meaningful change"
    direction = "↑" if trend > 0 else "↓"
    return f"{direction} {abs(trend) * 100:.1f}% this month"


def _severity(score: float) -> str:
    if score >= 75:
        return "high"
    if score >= 50:
        return "medium"
    return "low"


def _map_risk(indicator: str, value: float, trend: float) -> dict:
    name = indicator.lower()
    if "inflation" in name:
        score = min(100, value * 3.2 + max(0, trend) * 120)
        return {
            "indicator": indicator,
            "risk_factor": "Expense Instability",
            "impact": "Higher inflation increases operating costs and weakens margins.",
            "severity": _severity(score),
            "explanation": "Inflation pressure maps to expense volatility, purchasing power, and supplier pricing risk.",
        }
    if "spread" in name and "usd" in name:
        score = min(100, value * 1.8 + max(0, trend) * 250)
        return {
            "indicator": indicator,
            "risk_factor": "FX Spread Pressure",
            "impact": "A wider official-parallel spread signals FX scarcity and pricing uncertainty.",
            "severity": _severity(score),
            "explanation": "FX spread maps to macro stress, import pricing uncertainty, and working-capital pressure.",
        }
    if "exchange" in name or "fx" in name or "usd" in name:
        score = min(100, 35 + max(0, trend) * 550)
        return {
            "indicator": indicator,
            "risk_factor": "Inventory Exposure",
            "impact": "FX weakness raises import, replacement, and supplier costs.",
            "severity": _severity(score),
            "explanation": "Exchange-rate pressure maps to inventory replacement cost and cash conversion risk.",
        }
    if "fuel" in name:
        score = min(100, 30 + max(0, trend) * 700 + max(0, value - 100) * 1.2)
        return {
            "indicator": indicator,
            "risk_factor": "Fuel Cost Sensitivity",
            "impact": "Fuel increases raise logistics and operating expenses.",
            "severity": _severity(score),
            "explanation": "Fuel pressure maps directly to logistics cost and expense instability.",
        }
    if "interest" in name or "rate" in name:
        score = min(100, value * 2.6 + max(0, trend) * 100)
        return {
            "indicator": indicator,
            "risk_factor": "Debt Pressure",
            "impact": "Higher interest rates increase loan servicing pressure.",
            "severity": _severity(score),
            "explanation": "Interest-rate pressure maps to debt payment sustainability and refinancing risk.",
        }
    if "confidence" in name:
        score = max(0, 100 - value)
        return {
            "indicator": indicator,
            "risk_factor": "Revenue Volatility",
            "impact": "Lower confidence can weaken demand and revenue stability.",
            "severity": _severity(score),
            "explanation": "Business confidence maps to demand outlook and revenue volatility.",
        }
    return {
        "indicator": indicator,
        "risk_factor": "External Risk",
        "impact": "External macro movement may influence business stability.",
        "severity": "low",
        "explanation": "Indicator is tracked as a general macroeconomic pressure signal.",
    }


def _alerts(latest: list[EconomicIndicator], history: dict[str, list[dict]]) -> list[dict]:
    alerts: list[dict] = []
    for row in latest:
        points = history.get(row.indicator_name, [])
        trend = _trend(points)
        mapped = _map_risk(row.indicator_name, float(row.indicator_value), trend)
        if mapped["severity"] in {"medium", "high"}:
            direction = "increased" if trend > 0 else "remains elevated"
            alerts.append(
                {
                    "indicator": row.indicator_name,
                    "severity": mapped["severity"],
                    "message": f"{row.indicator_name} {direction}; watch {mapped['risk_factor'].lower()}.",
                    "date": row.record_date,
                }
            )
    return alerts


def indicators(db: Session, country: str = "Nigeria") -> dict:
    rows = (
        db.query(EconomicIndicator)
        .filter(EconomicIndicator.country == country, EconomicIndicator.deleted_at.is_(None))
        .order_by(EconomicIndicator.record_date.asc())
        .all()
    )
    rows = [row for row in rows if not _is_legacy_fx(row)]
    history = _history(rows)
    latest = _latest_by_indicator(rows)
    mappings = [
        _map_risk(row.indicator_name, float(row.indicator_value), _trend(history.get(row.indicator_name, [])))
        for row in latest
    ]
    return {
        "country": country,
        "indicators": [
            {
                "name": row.indicator_name,
                "value": float(row.indicator_value),
                "unit": row.unit,
                "date": row.record_date,
                "source": row.source,
                "trend_percent": round(_trend(history.get(row.indicator_name, [])) * 100, 2),
                "trend_label": _trend_label(_trend(history.get(row.indicator_name, []))),
            }
            for row in latest
        ],
        "history": history,
        "risk_mappings": mappings,
        "alerts": _alerts(latest, history),
        "public_sources": PUBLIC_SOURCES,
    }
