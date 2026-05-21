from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_current_user
from app.db.session import get_db
from app.models.business import Business
from app.models.user import User
from app.services import audit_service, privacy_service

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def settings(user: User = Depends(get_current_user)) -> dict:
    return {
        "profile": {
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "language": "English",
            "timezone": "West Africa Time",
        },
        "notifications": {"risk_alerts": True, "weekly_reports": True, "economic_updates": True},
        "currency": "NGN",
    }


@router.get("/privacy/export")
def export_data(
    user: User = Depends(get_current_user),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return privacy_service.export_account_data(db, user, business)


@router.get("/audit-logs")
def audit_logs(
    user: User = Depends(get_current_user),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"items": audit_service.list_audit_logs(db, user_id=user.id, business_id=business.id, limit=50)}


@router.delete("/privacy/account")
def delete_account(
    user: User = Depends(get_current_user),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return privacy_service.soft_delete_account(db, user, business)
