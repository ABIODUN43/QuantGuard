from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "full_name": "Daniel Okafor",
                        "email": "daniel@example.com",
                        "password": "securepassword",
                    }
                }
            }
        }
    },
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    return auth_service.register(db, payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {"email": "daniel@example.com", "password": "securepassword"}
                }
            }
        }
    },
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    return auth_service.login(db, payload)


@router.post("/password-reset/request")
def password_reset_request(payload: PasswordResetRequest, db: Session = Depends(get_db)) -> dict:
    return auth_service.request_password_reset(db, payload)


@router.post("/password-reset/confirm")
def password_reset_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)) -> dict:
    return auth_service.confirm_password_reset(db, payload)
