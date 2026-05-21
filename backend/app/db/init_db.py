from datetime import date

from sqlalchemy import inspect, text

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import engine
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.business import Business
from app.models.economic_indicator import EconomicIndicator
from app.models.financial_record import FinancialRecord
from app.models.forecast import Forecast  # noqa: F401
from app.models.password_reset_token import PasswordResetToken  # noqa: F401
from app.models.recommendation import Recommendation  # noqa: F401
from app.models.report import Report  # noqa: F401
from app.models.risk_analysis import RiskAnalysis  # noqa: F401
from app.models.scenario import Scenario  # noqa: F401
from app.models.user import User
from app.db.session import SessionLocal


LIFECYCLE_TABLES = [
    "users",
    "businesses",
    "financial_records",
    "economic_indicators",
    "risk_analysis",
    "forecasts",
    "recommendations",
    "scenarios",
    "reports",
    "audit_logs",
    "password_reset_tokens",
]


def _ensure_sqlite_lifecycle_columns() -> None:
    if engine.dialect.name != "sqlite":
        return
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    with engine.begin() as connection:
        for table in LIFECYCLE_TABLES:
            if table not in existing_tables:
                continue
            columns = {column["name"] for column in inspector.get_columns(table)}
            if "deleted_at" not in columns:
                connection.execute(text(f"ALTER TABLE {table} ADD COLUMN deleted_at DATETIME"))
            if "archived_at" not in columns:
                connection.execute(text(f"ALTER TABLE {table} ADD COLUMN archived_at DATETIME"))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_lifecycle_columns()


def seed_demo_data() -> None:
    init_db()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "daniel@example.com").first()
        if not user:
            user = User(
                full_name="Daniel Okafor",
                email="daniel@example.com",
                hashed_password=hash_password("securepassword"),
                role="business_owner",
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        business = db.query(Business).filter(Business.user_id == user.id).first()
        if not business:
            business = Business(
                user_id=user.id,
                business_name="GreenField Stores",
                business_type="Retail Trade",
                industry="Retail",
                country="Nigeria",
                state="Lagos",
                city="Ikeja",
                years_in_operation=4,
                number_of_employees=12,
                average_monthly_revenue=2_500_000,
                average_monthly_expenses=1_800_000,
            )
            db.add(business)
            db.commit()
            db.refresh(business)

        if not db.query(FinancialRecord).filter(FinancialRecord.business_id == business.id).first():
            rows = [
                ("2025-12-01", 2_100_000, 1_480_000, 980_000, 760_000, 240_000, 1_900_000, 180_000),
                ("2026-01-01", 2_450_000, 1_870_000, 1_120_000, 850_000, 230_000, 1_680_000, 250_000),
                ("2026-02-01", 2_780_000, 1_920_000, 1_250_000, 880_000, 220_000, 1_540_000, 260_000),
                ("2026-03-01", 2_620_000, 1_950_000, 1_180_000, 900_000, 210_000, 1_390_000, 275_000),
                ("2026-04-01", 2_350_000, 2_180_000, 1_070_000, 990_000, 205_000, 1_090_000, 315_000),
                ("2026-05-01", 2_420_000, 2_260_000, 1_120_000, 1_030_000, 200_000, 1_250_000, 340_000),
            ]
            for row in rows:
                db.add(
                    FinancialRecord(
                        business_id=business.id,
                        record_date=date.fromisoformat(row[0]),
                        revenue=row[1],
                        operating_expenses=row[2],
                        cost_of_goods_sold=row[3],
                        inventory_value=row[4],
                        debt_payment=row[5],
                        cash_balance=row[6],
                        fuel_logistics_cost=row[7],
                        other_income=0,
                    )
                )

        economic_rows = [
            ("Inflation Rate", 22.4, "%", date(2026, 5, 1)),
            ("Official USD/NGN", 1374.69, "NGN", date(2026, 5, 1)),
            ("Parallel USD/NGN", 1400.00, "NGN", date(2026, 5, 1)),
            ("USD/NGN Spread", 25.31, "NGN", date(2026, 5, 1)),
            ("Fuel Price Index", 118.6, "index", date(2026, 5, 1)),
            ("Business Confidence", 62, "/100", date(2026, 5, 1)),
        ]
        for name, value, unit, record_date in economic_rows:
            exists = (
                db.query(EconomicIndicator)
                .filter(
                    EconomicIndicator.country == "Nigeria",
                    EconomicIndicator.indicator_name == name,
                    EconomicIndicator.record_date == record_date,
                )
                .first()
            )
            if not exists:
                db.add(
                    EconomicIndicator(
                        country="Nigeria",
                        indicator_name=name,
                        indicator_value=value,
                        unit=unit,
                        source="manual",
                        record_date=record_date,
                    )
                )
        from app.services.economic_service import seed_economic_history

        seed_economic_history(db, "Nigeria")
        db.commit()
    finally:
        db.close()
