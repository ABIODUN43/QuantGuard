import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import (
    analysis,
    alerts,
    auth,
    business,
    economic,
    forecast,
    recommendations,
    reports,
    scenarios,
    settings as settings_routes,
    upload,
    users,
)
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import https_enforcement_middleware, rate_limit_middleware
from app.db.init_db import seed_demo_data

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    Path(settings.report_storage_dir).mkdir(parents=True, exist_ok=True)
    app = FastAPI(
        title="QuantGuard AI API",
        version="0.1.0",
        description="Financial early warning and risk intelligence API for SMEs.",
        openapi_tags=[
            {"name": "auth", "description": "JWT account registration and login."},
            {"name": "analysis", "description": "Quantitative risk scoring and stress probability."},
            {"name": "forecast", "description": "Cashflow and liquidity forecasts."},
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if settings.environment.lower() == "production" and settings.secret_key == "dev-secret-change-me":
        raise RuntimeError("QG_SECRET_KEY must be set in production")

    app.include_router(auth.router, prefix=settings.api_prefix)
    app.include_router(users.router, prefix=settings.api_prefix)
    app.include_router(business.router, prefix=settings.api_prefix)
    app.include_router(upload.router, prefix=settings.api_prefix)
    app.include_router(analysis.router, prefix=settings.api_prefix)
    app.include_router(alerts.router, prefix=settings.api_prefix)
    app.include_router(forecast.router, prefix=settings.api_prefix)
    app.include_router(recommendations.router, prefix=settings.api_prefix)
    app.include_router(scenarios.router, prefix=settings.api_prefix)
    app.include_router(reports.router, prefix=settings.api_prefix)
    app.include_router(economic.router, prefix=settings.api_prefix)
    app.include_router(settings_routes.router, prefix=settings.api_prefix)
    app.mount("/reports", StaticFiles(directory=settings.report_storage_dir), name="reports")

    @app.on_event("startup")
    def on_startup() -> None:
        seed_demo_data()
        logger.info("QuantGuard API startup complete")

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.status_code, "message": exc.detail}},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": {"code": 422, "message": "Validation failed", "details": exc.errors()}},
        )

    @app.middleware("http")
    async def enforce_https(request: Request, call_next):
        return await https_enforcement_middleware(request, call_next)

    @app.middleware("http")
    async def rate_limit(request: Request, call_next):
        return await rate_limit_middleware(request, call_next)

    @app.middleware("http")
    async def request_logging(request: Request, call_next):
        logger.info("%s %s", request.method, request.url.path)
        response = await call_next(request)
        logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
        return response

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "healthy", "service": "quantguard-ai-api"}

    return app


app = create_app()
