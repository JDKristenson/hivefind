"""API key authentication middleware for the HiveFind embed service."""

from __future__ import annotations

import hmac
import os

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

EXEMPT_PATHS = {"/health", "/docs", "/openapi.json"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Validate X-API-Key header on all non-exempt endpoints.

    If EMBED_SERVICE_API_KEY is not set, protected endpoints return 503.
    Uses constant-time comparison to prevent timing attacks.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        expected_key = os.environ.get("EMBED_SERVICE_API_KEY")
        if not expected_key:
            return JSONResponse(
                status_code=503,
                content={"detail": "API key not configured. Service unavailable."},
            )

        provided_key = request.headers.get("X-API-Key", "")
        if not provided_key or not hmac.compare_digest(provided_key, expected_key):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key."},
            )

        return await call_next(request)
