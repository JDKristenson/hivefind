"""Shared fixtures for hivefind-embed tests."""

from __future__ import annotations

import os
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

TEST_API_KEY = "test-hivefind-api-key-2026"


@pytest.fixture(autouse=True)
def _set_api_key() -> Generator[None, None, None]:
    """Set EMBED_SERVICE_API_KEY for all tests by default."""
    with patch.dict(os.environ, {"EMBED_SERVICE_API_KEY": TEST_API_KEY}):
        yield


@pytest.fixture()
def mock_embedder() -> Generator[MagicMock, None, None]:
    """Mock GeminiEmbedder that returns deterministic 3072-dim vectors."""
    with patch("src.main.embedder") as mock:
        mock.embed_text.return_value = [0.1] * 3072
        mock.embed_file.return_value = [0.2] * 3072
        mock.embed_multimodal.return_value = [0.3] * 3072
        yield mock


@pytest.fixture()
def mock_pinecone() -> Generator[MagicMock, None, None]:
    """Mock HivefindPinecone client."""
    with patch("src.main.pinecone_client") as mock:
        mock.upsert_vector.return_value = "test-memory-id"
        mock.query_vectors.return_value = [
            {
                "id": "mem-001",
                "score": 0.95,
                "metadata": {
                    "type": "outcome",
                    "agent": "Evelyn",
                    "domain": "personal",
                    "modality": "text",
                },
            },
            {
                "id": "mem-002",
                "score": 0.82,
                "metadata": {
                    "type": "pattern",
                    "agent": "Clare",
                    "domain": "personal",
                    "modality": "text",
                },
            },
        ]
        yield mock


@pytest.fixture()
def client(mock_embedder: MagicMock, mock_pinecone: MagicMock) -> TestClient:
    """FastAPI test client with mocked dependencies and API key header."""
    from src.main import app

    client = TestClient(app, raise_server_exceptions=False)
    client.headers["X-API-Key"] = TEST_API_KEY
    return client


def make_ingest_payload(**overrides: Any) -> dict[str, Any]:
    """Build a valid IngestRequest payload with optional overrides."""
    base: dict[str, Any] = {
        "agent": "Evelyn",
        "task_id": "test-task-001",
        "task_type": "memory_ingestion",
        "outcome": "success",
        "decision_made": "Stored user preference for morning flights",
        "rationale": "User booked morning flights 12 of last 15 times",
        "result_summary": "Preference recorded with 0.85 confidence",
        "lessons": ["Morning flight preference is strong"],
        "confidence": 0.85,
        "tags": ["travel", "preference"],
        "related_entities": ["Marco"],
        "human_feedback": None,
        "privacy_level": "open",
        "domain": "personal",
    }
    base.update(overrides)
    return base
