"""Tests for rate limiting middleware."""

from __future__ import annotations

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from tests.conftest import TEST_API_KEY


class TestRateLimiting:
    """Rate limiting on protected endpoints."""

    def test_requests_under_limit_succeed(self, client: TestClient) -> None:
        for _ in range(5):
            resp = client.post("/embed/text", json={"text": "hello"})
            assert resp.status_code == 200

    def test_requests_over_limit_return_429(self, client: TestClient) -> None:
        # Default limit: 60/minute. Exceed it.
        statuses = []
        for _ in range(65):
            resp = client.post(
                "/embed/text",
                json={"text": "hello"},
            )
            statuses.append(resp.status_code)

        assert 429 in statuses, "Expected at least one 429 response"

    def test_health_not_rate_limited(self, client: TestClient) -> None:
        for _ in range(70):
            resp = client.get("/health")
            assert resp.status_code == 200

    def test_429_response_body_has_error(self, client: TestClient) -> None:
        for _ in range(65):
            resp = client.post("/embed/text", json={"text": "hello"})
            if resp.status_code == 429:
                assert "rate limit" in resp.text.lower() or "Rate limit" in resp.text
                break
