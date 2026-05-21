"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-18
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def lifecycle_columns() -> list[sa.Column]:
    return [
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    ]


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "businesses",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("business_name", sa.String(180), nullable=False),
        sa.Column("business_type", sa.String(100), nullable=False),
        sa.Column("industry", sa.String(100), nullable=False),
        sa.Column("country", sa.String(80), nullable=False),
        sa.Column("state", sa.String(80), nullable=False),
        sa.Column("city", sa.String(80), nullable=False),
        sa.Column("years_in_operation", sa.Integer(), nullable=False),
        sa.Column("number_of_employees", sa.Integer(), nullable=False),
        sa.Column("average_monthly_revenue", sa.Numeric(14, 2), nullable=False),
        sa.Column("average_monthly_expenses", sa.Numeric(14, 2), nullable=False),
    )
    op.create_index("ix_businesses_user_id", "businesses", ["user_id"])
    op.create_index("ix_businesses_deleted_at", "businesses", ["deleted_at"])
    op.create_index("ix_businesses_archived_at", "businesses", ["archived_at"])
    op.create_table(
        "financial_records",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("record_date", sa.Date(), nullable=False),
        sa.Column("revenue", sa.Numeric(14, 2), nullable=False),
        sa.Column("operating_expenses", sa.Numeric(14, 2), nullable=False),
        sa.Column("cost_of_goods_sold", sa.Numeric(14, 2), nullable=False),
        sa.Column("inventory_value", sa.Numeric(14, 2), nullable=False),
        sa.Column("debt_payment", sa.Numeric(14, 2), nullable=False),
        sa.Column("cash_balance", sa.Numeric(14, 2), nullable=False),
        sa.Column("fuel_logistics_cost", sa.Numeric(14, 2), nullable=False),
        sa.Column("other_income", sa.Numeric(14, 2), nullable=False),
    )
    op.create_index("ix_financial_records_business_id", "financial_records", ["business_id"])
    op.create_index("ix_financial_records_record_date", "financial_records", ["record_date"])
    op.create_index("ix_financial_records_business_date", "financial_records", ["business_id", "record_date"])
    op.create_index("ix_financial_records_deleted_at", "financial_records", ["deleted_at"])
    op.create_table(
        "economic_indicators",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("country", sa.String(80), nullable=False),
        sa.Column("indicator_name", sa.String(120), nullable=False),
        sa.Column("indicator_value", sa.Numeric(14, 4), nullable=False),
        sa.Column("unit", sa.String(40), nullable=False),
        sa.Column("source", sa.String(120), nullable=False),
        sa.Column("record_date", sa.Date(), nullable=False),
    )
    op.create_index("ix_economic_indicators_country_date", "economic_indicators", ["country", "record_date"])
    op.create_index("ix_economic_indicators_name_date", "economic_indicators", ["indicator_name", "record_date"])
    op.create_table(
        "risk_analysis",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("risk_score", sa.Numeric(6, 2), nullable=False),
        sa.Column("stress_probability", sa.Numeric(5, 4), nullable=False),
        sa.Column("financial_stability_score", sa.Numeric(6, 2), nullable=False),
        sa.Column("forecast_confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("risk_level", sa.String(50), nullable=False),
        sa.Column("revenue_volatility", sa.Numeric(6, 2), nullable=False),
        sa.Column("expense_instability", sa.Numeric(6, 2), nullable=False),
        sa.Column("liquidity_weakness", sa.Numeric(6, 2), nullable=False),
        sa.Column("debt_pressure", sa.Numeric(6, 2), nullable=False),
        sa.Column("inventory_exposure", sa.Numeric(6, 2), nullable=False),
        sa.Column("fuel_cost_sensitivity", sa.Numeric(6, 2), nullable=False),
        sa.Column("analysis_summary", sa.Text(), nullable=False),
    )
    op.create_index("ix_risk_analysis_business_id", "risk_analysis", ["business_id"])
    op.create_index("ix_risk_analysis_business_created", "risk_analysis", ["business_id", "created_at"])
    op.create_index("ix_risk_analysis_risk_level", "risk_analysis", ["risk_level"])
    op.create_table(
        "forecasts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("analysis_id", sa.String(), sa.ForeignKey("risk_analysis.id"), nullable=False),
        sa.Column("forecast_horizon_days", sa.Integer(), nullable=False),
        sa.Column("projected_cash_balance", sa.Numeric(14, 2), nullable=False),
        sa.Column("cash_shortfall_probability", sa.Numeric(5, 4), nullable=False),
        sa.Column("forecast_confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("danger_period_start", sa.Date(), nullable=True),
        sa.Column("danger_period_end", sa.Date(), nullable=True),
        sa.Column("breakeven_revenue", sa.Numeric(14, 2), nullable=False),
        sa.Column("forecast_data", sa.JSON(), nullable=False),
    )
    op.create_index("ix_forecasts_business_id", "forecasts", ["business_id"])
    op.create_index("ix_forecasts_business_created", "forecasts", ["business_id", "created_at"])
    op.create_index("ix_forecasts_danger_start", "forecasts", ["danger_period_start"])
    op.create_table(
        "recommendations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("analysis_id", sa.String(), sa.ForeignKey("risk_analysis.id"), nullable=False),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(40), nullable=False),
        sa.Column("impact", sa.String(40), nullable=False),
        sa.Column("category", sa.String(80), nullable=False),
    )
    op.create_index("ix_recommendations_business_id", "recommendations", ["business_id"])
    op.create_index("ix_recommendations_business_created", "recommendations", ["business_id", "created_at"])
    op.create_index("ix_recommendations_priority", "recommendations", ["priority"])
    op.create_table(
        "scenarios",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("scenario_name", sa.String(160), nullable=False),
        sa.Column("scenario_type", sa.String(80), nullable=False),
        sa.Column("input_changes", sa.JSON(), nullable=False),
        sa.Column("result_summary", sa.JSON(), nullable=False),
        sa.Column("risk_score", sa.Numeric(6, 2), nullable=False),
        sa.Column("stress_probability", sa.Numeric(5, 4), nullable=False),
        sa.Column("cash_shortfall_probability", sa.Numeric(5, 4), nullable=False),
    )
    op.create_index("ix_scenarios_business_id", "scenarios", ["business_id"])
    op.create_index("ix_scenarios_business_created", "scenarios", ["business_id", "created_at"])
    op.create_index("ix_scenarios_scenario_type", "scenarios", ["scenario_type"])
    op.create_table(
        "reports",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("business_id", sa.String(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("analysis_id", sa.String(), sa.ForeignKey("risk_analysis.id"), nullable=True),
        sa.Column("report_type", sa.String(80), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
    )
    op.create_index("ix_reports_business_id", "reports", ["business_id"])
    op.create_index("ix_reports_status", "reports", ["status"])
    op.create_index("ix_reports_business_status", "reports", ["business_id", "status"])
    op.create_index("ix_reports_business_created", "reports", ["business_id", "created_at"])
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("business_id", sa.String(), nullable=True),
        sa.Column("action", sa.String(120), nullable=False),
        sa.Column("resource", sa.String(120), nullable=False),
        sa.Column("ip_address", sa.String(80), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_business_id", "audit_logs", ["business_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_resource", "audit_logs", ["resource"])
    op.create_index("ix_audit_logs_created", "audit_logs", ["created_at"])
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        *lifecycle_columns(),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"])
    op.create_index("ix_password_reset_tokens_token_hash", "password_reset_tokens", ["token_hash"])
    op.create_index("ix_password_reset_tokens_expires_at", "password_reset_tokens", ["expires_at"])


def downgrade() -> None:
    for table in [
        "password_reset_tokens",
        "audit_logs",
        "reports",
        "scenarios",
        "recommendations",
        "forecasts",
        "risk_analysis",
        "economic_indicators",
        "financial_records",
        "businesses",
        "users",
    ]:
        op.drop_table(table)
