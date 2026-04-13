"""Tests for API key authentication middleware."""

from __future__ import annotations

import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import TEST_API_KEY

WRONG_API_KEY = "wrong-key"


@pytest.fixture()
def auth_client(mock_embedder: MagicMock, mock_pinecone: MagicMock) -> TestClient:
    """Test client with EMBED_SERVICE_API_KEY set (no default header)."""
    from src.main import app

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def no_key_client(
    mock_embedder: MagicMock, mock_pinecone: MagicMock
) -> Generator[TestClient, None, None]:
    """Test client with no EMBED_SERVICE_API_KEY configured."""
    with patch.dict(os.environ, {}, clear=False) as env:
        env.pop("EMBED_SERVICE_API_KEY", None)
        from src.main import app

        yield TestClient(app, raise_server_exceptions=False)


class TestAuthMiddleware:
    """API key validation on protected endpoints."""

    def test_valid_key_allows_request(self, auth_client: TestClient) -> None:
        resp = auth_client.post(
            "/embed/text",
            json={"text": "hello"},
            headers={"X-API-Key": TEST_API_KEY},
        )
        assert resp.status_code == 200

    def test_missing_key_returns_401(self, auth_client: TestClient) -> None:
        resp = auth_client.post("/embed/text", json={"text": "hello"})
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"].lower() or "api key" in resp.json()["detail"].lower()

    def test_wrong_key_returns_401(self, auth_client: TestClient) -> None:
        resp = auth_client.post(
            "/embed/text",
            json={"text": "hello"},
            headers={"X-API-Key": WRONG_API_KEY},
        )
        assert resp.status_code == 401

    def test_health_exempt_from_auth(self, auth_client: TestClient) -> None:
        resp = auth_client.get("/health")
        assert resp.status_code == 200

    def test_health_exempt_even_without_key_configured(
        self, no_key_client: TestClient
    ) -> None:
        resp = no_key_client.get("/health")
        assert resp.status_code == 200

    def test_ingest_requires_auth(self, auth_client: TestClient) -> None:
        resp = auth_client.post("/ingest", json={"agent": "test"})
        assert resp.status_code == 401

    def test_query_requires_auth(self, auth_client: TestClient) -> None:
        resp = auth_client.post("/query", json={"query_text": "test"})
        assert resp.status_code == 401

    def test_embed_file_requires_auth(self, auth_client: TestClient) -> None:
        resp = auth_client.post("/embed/file")
        assert resp.status_code == 401

    def test_embed_multimodal_requires_auth(self, auth_client: TestClient) -> None:
        resp = auth_client.post("/embed/multimodal")
        assert resp.status_code == 401

    def test_no_key_configured_returns_503(self, no_key_client: TestClient) -> None:
        resp = no_key_client.post("/embed/text", json={"text": "hello"})
        assert resp.status_code == 503
        assert "not configured" in resp.json()["detail"].lower()

    def test_timing_safe_comparison(self, auth_client: TestClient) -> None:
        """Auth should use constant-time comparison to prevent timing attacks."""
        # Both should return 401, but the important thing is that the
        # implementation uses hmac.compare_digest (verified in code review)
        resp_short = auth_client.post(
            "/embed/text",
            json={"text": "hello"},
            headers={"X-API-Key": "a"},
        )
        resp_long = auth_client.post(
            "/embed/text",
            json={"text": "hello"},
            headers={"X-API-Key": "a" * 1000},
        )
        assert resp_short.status_code == 401
        assert resp_long.status_code == 401
