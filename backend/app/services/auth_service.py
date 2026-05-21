from uuid import uuid4
from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from sqlalchemy.orm import Session

from app.core.exceptions import bad_request, unauthorized
from app.core.security import create_access_token, hash_password, verify_password
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.schemas.auth import LoginRequest, PasswordResetConfirm, PasswordResetRequest, RegisterRequest
from app.services.audit_service import record_audit


def register(db: Session, payload: RegisterRequest) -> dict:
    if db.query(User).filter(User.email == payload.email).first():
        raise bad_request("Email already exists")
    user = User(
        id=str(uuid4()),
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="business_owner",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    record_audit(db, "register", "user", user_id=user.id)
    return {"message": "Account created successfully", "user_id": user.id}


def login(db: Session, payload: LoginRequest) -> dict:
    user = (
        db.query(User)
        .filter(User.email == payload.email, User.is_active.is_(True), User.deleted_at.is_(None))
        .first()
    )
    if not user or not verify_password(payload.password, user.hashed_password):
        raise unauthorized()
    record_audit(db, "login", "auth", user_id=user.id)
    return {
        "access_token": create_access_token(str(user.id), {"role": user.role}),
        "token_type": "bearer",
        "user_id": user.id,
    }


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def request_password_reset(db: Session, payload: PasswordResetRequest) -> dict:
    user = db.query(User).filter(User.email == payload.email, User.deleted_at.is_(None)).first()
    if not user:
        return {"message": "If that email exists, a reset token has been created"}
    raw_token = secrets.token_urlsafe(32)
    row = PasswordResetToken(
        id=str(uuid4()),
        user_id=user.id,
        token_hash=_token_hash(raw_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )
    db.add(row)
    db.commit()
    record_audit(db, "password_reset_requested", "auth", user_id=user.id)
    response = {"message": "If that email exists, a reset token has been created"}
    # MVP/dev convenience. In production, send this token by email and remove it from the response.
    response["reset_token"] = raw_token
    return response


def confirm_password_reset(db: Session, payload: PasswordResetConfirm) -> dict:
    row = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == _token_hash(payload.token), PasswordResetToken.used_at.is_(None))
        .first()
    )
    now = datetime.now(timezone.utc)
    if not row:
        raise bad_request("Invalid or expired reset token")
    expires_at = row.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < now:
        raise bad_request("Invalid or expired reset token")
    user = db.query(User).filter(User.id == row.user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise bad_request("Invalid reset token")
    user.hashed_password = hash_password(payload.new_password)
    row.used_at = now
    db.commit()
    record_audit(db, "password_reset_confirmed", "auth", user_id=user.id)
    return {"message": "Password reset successfully"}
