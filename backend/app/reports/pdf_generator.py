from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BRAND_GREEN = colors.HexColor("#009b63")
INK = colors.HexColor("#0f172a")
MUTED = colors.HexColor("#64748b")


def _money(value: float | int | None) -> str:
    return f"NGN {float(value or 0):,.0f}"


def _percent(value: float | int | None) -> str:
    number = float(value or 0)
    if number <= 1:
        number *= 100
    return f"{number:.0f}%"


def _metric_table(rows: list[tuple[str, object]]) -> Table:
    table = Table([[label, str(value)] for label, value in rows], colWidths=[2.8 * inch, 3.6 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ecfdf5")),
                ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d7dee8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def _section(story: list, title: str, styles) -> None:
    story.append(Spacer(1, 0.16 * inch))
    story.append(Paragraph(title, styles["Section"]))
    story.append(Spacer(1, 0.08 * inch))


def _header(story: list, payload: dict, styles) -> None:
    business = payload["business"]
    story.append(Paragraph("QuantGuard AI", styles["Brand"]))
    story.append(Paragraph(payload["template"]["title"], styles["ReportTitle"]))
    story.append(
        Paragraph(
            f"{business['business_name']} | {business['industry']} | {business['city']}, {business['country']}",
            styles["Muted"],
        )
    )
    story.append(Spacer(1, 0.2 * inch))


def _risk_section(story: list, payload: dict, styles) -> None:
    analysis = payload["analysis"]
    _section(story, "Risk Summary", styles)
    story.append(
        _metric_table(
            [
                ("Risk Score", f"{analysis['risk_score']:.0f}/100"),
                ("Risk Level", analysis["risk_level"]),
                ("Stress Probability", _percent(analysis["stress_probability"])),
                ("Financial Stability Score", f"{analysis['financial_stability_score']:.0f}/100"),
                ("Forecast Confidence", _percent(analysis["forecast_confidence"])),
            ]
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(analysis["summary"], styles["Body"]))

    _section(story, "Risk Drivers", styles)
    rows = [("Driver", "Score", "Contribution")]
    contributions = analysis.get("contribution_percentages", {})
    for key, value in analysis["risk_breakdown"].items():
        rows.append((key.replace("_", " ").title(), f"{float(value):.0f}/100", f"{float(contributions.get(key, 0)):.1f}%"))
    story.append(_simple_table(rows))


def _forecast_section(story: list, payload: dict, styles) -> None:
    forecast = payload["forecast"]
    _section(story, "Forecast Outlook", styles)
    story.append(
        _metric_table(
            [
                ("Projected Cash Balance", _money(forecast["projected_cash_balance"])),
                ("Cash Shortfall Probability", _percent(forecast["cash_shortfall_probability"])),
                ("Danger Period", forecast["danger_period"]),
                ("Breakeven Revenue", _money(forecast["breakeven_revenue"])),
                ("Forecast Model", forecast.get("model") or "Not available"),
            ]
        )
    )
    rows = [("Month", "Revenue", "Expenses", "Projected Cash", "Low", "High")]
    for point in forecast.get("cashflow_forecast", []):
        rows.append(
            (
                point["month"],
                _money(point["projected_revenue"]),
                _money(point["projected_expenses"]),
                _money(point["projected_cash_balance"]),
                _money(point.get("low_cash_balance")),
                _money(point.get("high_cash_balance")),
            )
        )
    if len(rows) > 1:
        _section(story, "Cashflow Forecast", styles)
        story.append(_simple_table(rows))


def _scenario_section(story: list, payload: dict, styles) -> None:
    scenario = payload.get("scenario")
    _section(story, "Scenario Simulation", styles)
    if not scenario:
        story.append(Paragraph("No scenario has been generated yet for this business.", styles["Body"]))
        return
    story.append(
        _metric_table(
            [
                ("Scenario", scenario["scenario_name"]),
                ("Risk Score", f"{scenario['risk_score']:.0f}/100"),
                ("Stress Probability", _percent(scenario["stress_probability"])),
                ("Cash Shortfall Probability", _percent(scenario["cash_shortfall_probability"])),
                ("Impact", scenario["impact"]),
                ("Summary", scenario["summary"]),
            ]
        )
    )


def _recommendations_section(story: list, payload: dict, styles) -> None:
    _section(story, "Recommended Actions", styles)
    rows = [("Action", "Priority", "Impact", "Category")]
    for item in payload.get("recommendations", []):
        rows.append((item["title"], item["priority"], item["impact"], item["category"]))
    story.append(_simple_table(rows))


def _lender_section(story: list, payload: dict, styles) -> None:
    business = payload["business"]
    analysis = payload["analysis"]
    forecast = payload["forecast"]
    _section(story, "Lender View", styles)
    story.append(
        _metric_table(
            [
                ("Business", business["business_name"]),
                ("Industry", business["industry"]),
                ("Monthly Revenue Baseline", _money(business["average_monthly_revenue"])),
                ("Monthly Expense Baseline", _money(business["average_monthly_expenses"])),
                ("Risk Level", analysis["risk_level"]),
                ("Stress Probability", _percent(analysis["stress_probability"])),
                ("Breakeven Revenue", _money(forecast["breakeven_revenue"])),
            ]
        )
    )


def _simple_table(rows: list[tuple]) -> Table:
    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d7dee8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def generate_pdf_report(payload: dict, output_path: Path) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Brand", fontName="Helvetica-Bold", fontSize=14, textColor=BRAND_GREEN))
    styles.add(ParagraphStyle(name="ReportTitle", fontName="Helvetica-Bold", fontSize=22, leading=28, textColor=INK))
    styles.add(ParagraphStyle(name="Section", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=INK))
    styles.add(ParagraphStyle(name="Muted", fontSize=9, textColor=MUTED))
    styles.add(ParagraphStyle(name="Body", fontSize=9, leading=13, textColor=INK))

    story: list = []
    _header(story, payload, styles)
    template = payload["template"]["key"]

    if template in {"risk", "risk_assessment", "lender"}:
        _risk_section(story, payload, styles)
    if template in {"forecast", "lender"}:
        _forecast_section(story, payload, styles)
    if template == "scenario":
        _scenario_section(story, payload, styles)
    if template == "lender":
        story.append(PageBreak())
        _lender_section(story, payload, styles)
    if template in {"risk", "risk_assessment", "forecast", "lender"}:
        _recommendations_section(story, payload, styles)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title=payload["template"]["title"],
    )
    doc.build(story)
