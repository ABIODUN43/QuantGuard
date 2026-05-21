from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import forbidden, unauthorized
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.business import Business
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise unauthorized("Missing bearer token")
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[ALGORITHM])
        user_id = str(UUID(payload["sub"]))
    except (JWTError, KeyError, ValueError) as exc:
        raise unauthorized("Invalid token") from exc
    user = (
        db.query(User)
        .filter(User.id == user_id, User.is_active.is_(True), User.deleted_at.is_(None))
        .first()
    )
    if not user:
        raise unauthorized("User not found")
    return user


def get_current_business(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Business:
    business = (
        db.query(Business)
        .filter(Business.user_id == user.id, Business.deleted_at.is_(None))
        .first()
    )
    if not business:
        from app.core.exceptions import not_found

        raise not_found("Business profile not found")
    return business


def require_roles(*roles: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise forbidden("Insufficient role permissions")
        return user

    return dependency
