"""FastAPI application for HiveFind embedding service."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncGenerator, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.auth import ApiKeyMiddleware
from src.embedder import DEFAULT_DIMENSIONS, SUPPORTED_MIME_TYPES, GeminiEmbedder
from src.ratelimit import limiter
from src.models import (
    EmbedResponse,
    EmbedTextRequest,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    MemoryMatch,
)
from src.pinecone_client import HivefindPinecone

logger = logging.getLogger(__name__)

embedder: Optional[GeminiEmbedder] = None
pinecone_client: Optional[HivefindPinecone] = None


def _load_env() -> None:
    """Load .env from project root or service directory."""
    project_root_env = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", ".env"
    )
    if os.path.exists(project_root_env):
        load_dotenv(project_root_env)
    else:
        load_dotenv()


def _require_env(key: str) -> str:
    """Get a required environment variable or raise."""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize clients on startup."""
    global embedder, pinecone_client

    _load_env()

    gemini_key = _require_env("GEMINI_API_KEY")
    pinecone_key = _require_env("PINECONE_API_KEY")
    index_name = os.environ.get("PINECONE_INDEX_NAME_V2", "hivefind-memory-v2")
    index_host = os.environ.get("PINECONE_HOST_V2")

    embedder = GeminiEmbedder(api_key=gemini_key)
    pinecone_client = HivefindPinecone(
        api_key=pinecone_key,
        index_name=index_name,
        host=index_host,
    )

    logger.info("HiveFind embed service started (index=%s)", index_name)
    yield
    logger.info("HiveFind embed service shutting down")


app = FastAPI(
    title="HiveFind Embed Service",
    description="Gemini Embedding 2 wrapper for HiveFind memory layer",
    version="0.2.0",
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(ApiKeyMiddleware)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for Xavier monitoring."""
    return HealthResponse()


@app.post("/embed/text", response_model=EmbedResponse)
@limiter.limit("60/minute")
async def embed_text(request: Request, body: EmbedTextRequest) -> EmbedResponse:
    """Embed a plain text string and return the vector."""
    try:
        vector = embedder.embed_text(
            text=body.text,
            dimensions=body.dimensions,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}") from e

    return EmbedResponse(
        vector=vector,
        dimensions=len(vector),
        modality="text",
    )


@app.post("/embed/file", response_model=EmbedResponse)
@limiter.limit("60/minute")
async def embed_file(
    request: Request,
    file: UploadFile = File(...),
    caption: Optional[str] = Form(default=None),
    dimensions: int = Form(default=DEFAULT_DIMENSIONS),
) -> EmbedResponse:
    """Embed a file (image, audio, video, or PDF)."""
    mime_type = file.content_type or ""
    if mime_type not in SUPPORTED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {mime_type}. Supported: {sorted(SUPPORTED_MIME_TYPES)}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        vector = embedder.embed_file(
            file_bytes=file_bytes,
            mime_type=mime_type,
            caption=caption,
            dimensions=dimensions,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}") from e

    modality = mime_type.split("/")[0]
    if mime_type == "application/pdf":
        modality = "pdf"

    return EmbedResponse(
        vector=vector,
        dimensions=len(vector),
        modality=modality,
    )


@app.post("/embed/multimodal", response_model=EmbedResponse)
@limiter.limit("60/minute")
async def embed_multimodal(
    request: Request,
    text: Optional[str] = Form(default=None),
    files: list[UploadFile] = File(default=[]),
    dimensions: int = Form(default=DEFAULT_DIMENSIONS),
) -> EmbedResponse:
    """Embed interleaved text and files in a single request."""
    if not text and not files:
        raise HTTPException(
            status_code=400,
            detail="Must provide at least text or one file.",
        )

    file_data: list[tuple[bytes, str]] = []
    for f in files:
        mime_type = f.content_type or ""
        if mime_type not in SUPPORTED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {mime_type}",
            )
        data = await f.read()
        if data:
            file_data.append((data, mime_type))

    try:
        vector = embedder.embed_multimodal(
            text=text,
            files=file_data,
            dimensions=dimensions,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}") from e

    modality = "multimodal" if (text and file_data) else ("text" if text else "file")

    return EmbedResponse(
        vector=vector,
        dimensions=len(vector),
        modality=modality,
    )


@app.post("/ingest", response_model=IngestResponse)
@limiter.limit("60/minute")
async def ingest_memory(request: Request, body: IngestRequest) -> IngestResponse:
    """Full memory ingestion: embed text payload and upsert to Pinecone.

    This replaces the OpenAI embed + Pinecone upsert chain in
    Evelyn_01_MemoryIngestion.
    """
    embed_text_parts = [
        f"Agent: {body.agent}",
        f"Task: {body.task_type}",
        f"Decision: {body.decision_made}",
        f"Rationale: {body.rationale}",
        f"Result: {body.result_summary}",
    ]
    if body.lessons:
        embed_text_parts.append(f"Lessons: {'; '.join(body.lessons)}")
    if body.tags:
        embed_text_parts.append(f"Tags: {', '.join(body.tags)}")

    combined_text = "\n".join(embed_text_parts)

    try:
        vector = embedder.embed_text(text=combined_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}") from e

    metadata = {
        "type": "outcome",
        "agent": body.agent,
        "domain": body.domain,
        "task_type": body.task_type,
        "outcome": body.outcome,
        "confidence": body.confidence,
        "privacy_level": body.privacy_level,
        "tags": body.tags,
        "entity_refs": body.related_entities,
        "modality": "text",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decision": body.decision_made,
        "rationale": body.rationale,
        "result_summary": body.result_summary,
        "lessons": body.lessons,
    }
    if body.human_feedback:
        metadata["human_feedback"] = body.human_feedback

    memory_id = pinecone_client.upsert_vector(
        vector=vector,
        metadata=metadata,
        vector_id=body.task_id,
    )

    return IngestResponse(
        memory_id=memory_id,
        dimensions=len(vector),
        modality="text",
    )


@app.post("/query", response_model=QueryResponse)
@limiter.limit("60/minute")
async def query_memories(request: Request, body: QueryRequest) -> QueryResponse:
    """Query memory: embed query text and search Pinecone.

    This replaces the OpenAI embed + Pinecone query chain in
    Evelyn_02_MemoryQuery.
    """
    try:
        query_vector = embedder.embed_text(text=body.query_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {e}") from e

    filters: dict[str, object] = {}
    if body.agent:
        filters["agent"] = body.agent
    if body.domain:
        filters["domain"] = body.domain
    if body.modality_filter:
        filters["modality"] = body.modality_filter

    matches = pinecone_client.query_vectors(
        vector=query_vector,
        top_k=body.top_k,
        filters=filters if filters else None,
    )

    return QueryResponse(
        matches=[MemoryMatch(**m) for m in matches],
        query_dimensions=len(query_vector),
    )


if __name__ == "__main__":
    import uvicorn

    _load_env()
    port = int(os.environ.get("EMBED_SERVICE_PORT", "8766"))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
