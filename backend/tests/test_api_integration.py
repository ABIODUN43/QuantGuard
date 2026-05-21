from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.init_db import seed_demo_data
from app.main import app


seed_demo_data()
client = TestClient(app)


def unique_email() -> str:
    return f"owner-{uuid4().hex[:10]}@example.com"


def register_and_login(email: str | None = None) -> tuple[dict, dict]:
    email = email or unique_email()
    register = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Ada Test", "email": email, "password": "securepassword"},
    )
    assert register.status_code == 200, register.text
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "securepassword"})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, register.json()


def onboard(headers: dict) -> dict:
    response = client.post(
        "/api/v1/business/onboard",
        headers=headers,
        json={
            "business_name": "Flow Test Stores",
            "business_type": "Retail Trade",
            "industry": "Retail",
            "country": "Nigeria",
            "state": "Lagos",
            "city": "Ikeja",
            "years_in_operation": 3,
            "number_of_employees": 8,
            "average_monthly_revenue": 2_500_000,
            "average_monthly_expenses": 1_700_000,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_full_business_flow_register_onboard_upload_analyze_forecast_recommend_report() -> None:
    headers, _ = register_and_login()
    onboard(headers)

    seed = client.post("/api/v1/data/demo-seed", headers=headers)
    assert seed.status_code == 200, seed.text
    assert seed.json()["records_processed"] == 6

    analysis = client.post("/api/v1/analysis/run", headers=headers)
    assert analysis.status_code == 200, analysis.text
    assert 0 <= analysis.json()["risk_score"] <= 100
    assert analysis.json()["contribution_percentages"]

    forecast = client.get("/api/v1/forecast/latest", headers=headers)
    assert forecast.status_code == 200, forecast.text
    assert len(forecast.json()["cashflow_forecast"]) == 6

    recommendations = client.get("/api/v1/recommendations", headers=headers)
    assert recommendations.status_code == 200, recommendations.text
    assert recommendations.json()["recommendations"]

    scenario = client.post(
        "/api/v1/scenarios/run",
        headers=headers,
        json={
            "scenario_name": "Sales Drop -20%",
            "changes": {"sales_change_percent": -20, "operating_expenses_change_percent": 5},
        },
    )
    assert scenario.status_code == 200, scenario.text
    assert scenario.json()["impact"]

    report = client.post(
        "/api/v1/reports/generate",
        headers=headers,
        json={"report_type": "lender", "format": "pdf"},
    )
    assert report.status_code == 200, report.text
    assert report.json()["download_url"].endswith(".pdf")


def test_upload_csv_and_reject_suspicious_upload() -> None:
    headers, _ = register_and_login()
    onboard(headers)
    csv = (
        "date,revenue,operating_expenses,cost_of_goods_sold,inventory_value,"
        "debt_payment,cash_balance,fuel_logistics_cost,other_income\n"
        "2026-01-01,2450000,1870000,1120000,850000,210000,580000,250000,0\n"
    )
    response = client.post(
        "/api/v1/data/upload",
        headers=headers,
        files={"file": ("records.csv", BytesIO(csv.encode("utf-8")), "text/csv")},
    )
    assert response.status_code == 200, response.text
    assert response.json()["records_processed"] == 1

    rejected = client.post(
        "/api/v1/data/upload",
        headers=headers,
        files={"file": ("bad.csv", BytesIO(b"<script>alert(1)</script>"), "text/csv")},
    )
    assert rejected.status_code == 400
    assert "security scan" in rejected.json()["error"]["message"].lower()


def test_password_reset_privacy_export_and_audit_logs() -> None:
    email = unique_email()
    headers, _ = register_and_login(email)
    onboard(headers)
    client.post("/api/v1/data/demo-seed", headers=headers)

    reset = client.post("/api/v1/auth/password-reset/request", json={"email": email})
    assert reset.status_code == 200
    token = reset.json()["reset_token"]
    confirm = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"token": token, "new_password": "securepassword"},
    )
    assert confirm.status_code == 200

    export = client.get("/api/v1/settings/privacy/export", headers=headers)
    assert export.status_code == 200
    assert export.json()["financial_records"]

    audit = client.get("/api/v1/settings/audit-logs", headers=headers)
    assert audit.status_code == 200
    assert audit.json()["items"]


def test_economic_indicator_manual_entry_and_mapping() -> None:
    headers, _ = register_and_login()
    response = client.post(
        "/api/v1/economic/indicators",
        headers=headers,
        json={
            "country": "Nigeria",
            "indicator_name": "Interest Rate",
            "indicator_value": 27.5,
            "unit": "%",
            "source": "manual_test",
            "record_date": "2026-06-01",
        },
    )
    assert response.status_code == 200, response.text
    indicators = client.get("/api/v1/economic/indicators?country=Nigeria")
    assert indicators.status_code == 200
    payload = indicators.json()
    names = {item["name"]: item for item in payload["indicators"]}
    assert names["Official USD/NGN"]["value"] == 1374.69
    assert names["Parallel USD/NGN"]["value"] == 1400
    assert names["USD/NGN Spread"]["value"] == 25.31
    assert names["Official USD/NGN"]["trend_label"] == "↑ 2.3% this month"
    assert any(item["risk_factor"] == "Debt Pressure" for item in payload["risk_mappings"])
    assert any(item["risk_factor"] == "FX Spread Pressure" for item in payload["risk_mappings"])
