from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessOnboardRequest


def onboard_business(db: Session, user, payload: BusinessOnboardRequest) -> dict:
    business = db.query(Business).filter(Business.user_id == user.id, Business.deleted_at.is_(None)).first()
    if not business:
        business = Business(id=str(uuid4()), user_id=user.id)
        db.add(business)
    for key, value in payload.model_dump().items():
        setattr(business, key, value)
    db.commit()
    db.refresh(business)
    return {"message": "Business profile created", "business_id": business.id}


def current_business(db: Session, user) -> Business | None:
    return db.query(Business).filter(Business.user_id == user.id, Business.deleted_at.is_(None)).first()
