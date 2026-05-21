from uuid import uuid4
from io import BytesIO

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import bad_request, not_found
from app.math_engine.validation import REQUIRED_COLUMNS, missing_columns
from app.models.business import Business
from app.models.financial_record import FinancialRecord
from app.schemas.financial_record import FinancialRecordCreate
from app.services.audit_service import record_audit


SUSPICIOUS_SIGNATURES = [
    b"<script",
    b"powershell",
    b"cmd.exe",
    b"auto_open",
    b"vbaProject.bin",
    b"mso-application",
]


def add_manual_record(db: Session, business: Business, payload: FinancialRecordCreate) -> FinancialRecord:
    if not business:
        raise not_found("Business profile not found")
    record = FinancialRecord(id=str(uuid4()), business_id=business.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    record_audit(db, "manual_financial_record", "financial_records", business_id=business.id)
    return record


def seed_demo_records(db: Session, business: Business) -> dict:
    if not business:
        raise not_found("Business profile not found")
    existing = (
        db.query(FinancialRecord)
        .filter(FinancialRecord.business_id == business.id)
        .filter(FinancialRecord.deleted_at.is_(None), FinancialRecord.archived_at.is_(None))
        .count()
    )
    if existing:
        return {
            "message": "Business already has financial records",
            "records_processed": 0,
            "status": "skipped",
            "required_columns": sorted(REQUIRED_COLUMNS),
        }

    from datetime import date

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
                id=str(uuid4()),
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
    db.commit()
    return {
        "message": "Demo financial records loaded",
        "records_processed": len(rows),
        "status": "processed",
        "required_columns": sorted(REQUIRED_COLUMNS),
    }


async def process_upload(db: Session, business: Business, file: UploadFile) -> dict:
    if not business:
        raise not_found("Business profile not found")

    name = file.filename or ""
    if not name.endswith((".csv", ".xlsx", ".xls")):
        raise bad_request("Only CSV and Excel uploads are supported")
    content_type = file.content_type or ""
    if content_type and not any(
        allowed in content_type
        for allowed in [
            "csv",
            "excel",
            "spreadsheet",
            "octet-stream",
            "vnd.ms-excel",
            "vnd.openxmlformats",
        ]
    ):
        raise bad_request("Unsupported file content type")

    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise bad_request(f"Upload exceeds maximum size of {settings.max_upload_bytes} bytes")
    lowered = content[:4096].lower()
    if any(signature.lower() in lowered for signature in SUSPICIOUS_SIGNATURES):
        raise bad_request("Upload failed security scan")
    if not content:
        raise bad_request("Uploaded file is empty")

    if name.endswith(".csv"):
        import pandas as pd

        frame = pd.read_csv(BytesIO(content))
    else:
        import pandas as pd

        frame = pd.read_excel(BytesIO(content))

    normalized = {column.strip().lower() for column in frame.columns}
    missing = missing_columns(normalized)
    if missing:
        raise bad_request(f"Missing required columns: {', '.join(sorted(missing))}")

    frame.columns = [column.strip().lower() for column in frame.columns]
    processed = 0
    for row in frame.to_dict(orient="records"):
        payload = FinancialRecordCreate(
            record_date=row.get("record_date") or row.get("date"),
            revenue=row["revenue"],
            operating_expenses=row["operating_expenses"],
            cost_of_goods_sold=row["cost_of_goods_sold"],
            inventory_value=row["inventory_value"],
            debt_payment=row["debt_payment"],
            cash_balance=row["cash_balance"],
            fuel_logistics_cost=row["fuel_logistics_cost"],
            other_income=row.get("other_income", 0) or 0,
        )
        add_manual_record(db, business, payload)
        processed += 1

    record_audit(
        db,
        "financial_upload",
        "financial_records",
        business_id=business.id,
        metadata={"filename": name, "records_processed": processed, "bytes": len(content)},
    )

    return {
        "message": "Data uploaded successfully",
        "records_processed": processed,
        "status": "processed",
        "required_columns": sorted(REQUIRED_COLUMNS),
    }


def list_records(db: Session, business: Business, limit: int, offset: int) -> tuple[list[FinancialRecord], int]:
    query = db.query(FinancialRecord).filter(FinancialRecord.business_id == business.id)
    query = query.filter(FinancialRecord.deleted_at.is_(None), FinancialRecord.archived_at.is_(None))
    total = query.count()
    rows = query.order_by(FinancialRecord.record_date.asc()).offset(offset).limit(limit).all()
    return rows, total
