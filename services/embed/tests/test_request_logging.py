"""Tests for request logging middleware."""

from __future__ import annotations

import json
import os
import tempfile
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import TEST_API_KEY


@pytest.fixture(autouse=True)
def _reset_rate_limiter() -> None:
    """Reset slowapi rate limiter state so prior tests don't cause 429s."""
    from src.ratelimit import limiter

    limiter.reset()


class TestRequestLogging:
    """Structured request logging to services/embed/logs/."""

    def test_successful_request_logged(self, client: TestClient, tmp_path: object) -> None:
        """Authenticated request logs IP, path, method, status, latency."""
        log_dir = str(tmp_path)
        with patch("src.request_logger.LOG_DIR", log_dir):
            resp = client.post("/embed/text", json={"text": "hello"})
            assert resp.status_code == 200

            log_files = os.listdir(log_dir)
            assert len(log_files) >= 1

            log_file = os.path.join(log_dir, sorted(log_files)[-1])
            with open(log_file) as f:
                lines = f.readlines()

            # Find the log line for our request
            entries = [json.loads(line) for line in lines if line.strip()]
            embed_entries = [e for e in entries if e["path"] == "/embed/text"]
            assert len(embed_entries) >= 1

            entry = embed_entries[-1]
            assert entry["method"] == "POST"
            assert entry["status"] == 200
            assert entry["path"] == "/embed/text"
            assert "ip" in entry
            assert "latency_ms" in entry
            assert isinstance(entry["latency_ms"], (int, float))
            assert entry["latency_ms"] >= 0

    def test_rejected_request_logged(self, client: TestClient, tmp_path: object) -> None:
        """401 from missing API key still gets logged."""
        log_dir = str(tmp_path)
        with patch("src.request_logger.LOG_DIR", log_dir):
            # Remove the API key header for this request
            resp = client.post(
                "/embed/text",
                json={"text": "hello"},
                headers={"X-API-Key": ""},
            )
            assert resp.status_code == 401

            log_files = os.listdir(log_dir)
            assert len(log_files) >= 1

            log_file = os.path.join(log_dir, sorted(log_files)[-1])
            with open(log_file) as f:
                lines = f.readlines()

            entries = [json.loads(line) for line in lines if line.strip()]
            rejected = [e for e in entries if e["status"] == 401]
            assert len(rejected) >= 1
            assert rejected[-1]["path"] == "/embed/text"

    def test_health_endpoint_logged(self, client: TestClient, tmp_path: object) -> None:
        """Health checks are logged too (for monitoring completeness)."""
        log_dir = str(tmp_path)
        with patch("src.request_logger.LOG_DIR", log_dir):
            resp = client.get("/health")
            assert resp.status_code == 200

            log_files = os.listdir(log_dir)
            assert len(log_files) >= 1

            log_file = os.path.join(log_dir, sorted(log_files)[-1])
            with open(log_file) as f:
                lines = f.readlines()

            entries = [json.loads(line) for line in lines if line.strip()]
            health_entries = [e for e in entries if e["path"] == "/health"]
            assert len(health_entries) >= 1

    def test_log_entry_has_timestamp(self, client: TestClient, tmp_path: object) -> None:
        """Each log entry includes an ISO timestamp."""
        log_dir = str(tmp_path)
        with patch("src.request_logger.LOG_DIR", log_dir):
            client.get("/health")

            log_files = os.listdir(log_dir)
            log_file = os.path.join(log_dir, sorted(log_files)[-1])
            with open(log_file) as f:
                lines = f.readlines()

            entries = [json.loads(line) for line in lines if line.strip()]
            assert len(entries) >= 1
            assert "timestamp" in entries[-1]
            # ISO format check: should contain "T" separator
            assert "T" in entries[-1]["timestamp"]

    def test_log_file_uses_date_naming(self, client: TestClient, tmp_path: object) -> None:
        """Log files are named by date for easy rotation."""
        log_dir = str(tmp_path)
        with patch("src.request_logger.LOG_DIR", log_dir):
            client.get("/health")

            log_files = os.listdir(log_dir)
            assert len(log_files) == 1
            # Format: access-YYYY-MM-DD.jsonl
            assert log_files[0].startswith("access-")
            assert log_files[0].endswith(".jsonl")
