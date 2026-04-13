"""Structured request logging middleware for the HiveFind embed service."""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import date, datetime, timezone
from pathlib import Path

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")


def _ensure_log_dir() -> None:
    """Create the log directory if it doesn't exist."""
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)


def _log_file_path() -> str:
    """Return today's log file path: access-YYYY-MM-DD.jsonl."""
    today = date.today().isoformat()
    return os.path.join(LOG_DIR, f"access-{today}.jsonl")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request as a JSON line to a daily log file."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.monotonic()
        response = await call_next(request)
        latency_ms = round((time.monotonic() - start) * 1000, 2)

        ip = request.client.host if request.client else "unknown"

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": ip,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "latency_ms": latency_ms,
        }

        try:
            _ensure_log_dir()
            with open(_log_file_path(), "a") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError:
            logger.warning("Failed to write access log entry: %s", entry)

        return response
