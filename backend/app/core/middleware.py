from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.config import settings


_rate_windows: dict[str, deque[float]] = defaultdict(deque)


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def https_enforcement_middleware(request: Request, call_next):
    if settings.enforce_https or settings.environment.lower() == "production":
        proto = request.headers.get("x-forwarded-proto", request.url.scheme)
        if proto != "https" and request.url.hostname not in {"127.0.0.1", "localhost"}:
            https_url = request.url.replace(scheme="https")
            return RedirectResponse(str(https_url), status_code=307)
    return await call_next(request)


async def rate_limit_middleware(request: Request, call_next):
    limit = max(1, settings.rate_limit_per_minute)
    now = time.time()
    window = _rate_windows[_client_key(request)]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= limit:
        return JSONResponse(
            status_code=429,
            content={"error": {"code": 429, "message": "Rate limit exceeded. Try again shortly."}},
        )
    window.append(now)
    return await call_next(request)
