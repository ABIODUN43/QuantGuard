from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def record_audit(
    db: Session,
    action: str,
    resource: str,
    user_id: str | None = None,
    business_id: str | None = None,
    ip_address: str | None = None,
    metadata: dict | None = None,
) -> AuditLog:
    row = AuditLog(
        id=str(uuid4()),
        user_id=user_id,
        business_id=business_id,
        action=action,
        resource=resource,
        ip_address=ip_address,
        metadata_json=metadata or {},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_audit_logs(
    db: Session, user_id: str | None = None, business_id: str | None = None, limit: int = 20
) -> list[dict]:
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if business_id:
        query = query.filter(AuditLog.business_id == business_id)
    rows = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [
        {
            "id": row.id,
            "action": row.action,
            "resource": row.resource,
            "ip_address": row.ip_address,
            "metadata": row.metadata_json,
            "created_at": row.created_at,
        }
        for row in rows
    ]
