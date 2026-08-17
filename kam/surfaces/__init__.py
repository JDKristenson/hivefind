"""Surface adapters. Each exposes run(prompt, **kw) -> SurfaceResult. Deferred surfaces raise a clear message."""

from __future__ import annotations

from collections.abc import Callable

from ..config import Settings
from . import agy, claude_p, codex, openrouter
from .base import SurfaceResult

DEFERRED = {
    "manus": "Manus adapter lands in Phase 3 (API + webhook receipt).",
    "hermes": "Hermes dispatch from EC2 lands in Phase 3 (Telegram/CLI relay).",
    "cf-browser": "Cloudflare Browser Run pilot is Phase 3.",
    "notion-ai": "Notion Custom Agents are invoked in Notion, not by kam run; record them with `kam log --surface notion-ai`.",
    "pplx-computer": "Perplexity Computer tasks are scheduled in Perplexity; record them with `kam log --surface pplx-computer`.",
    "n8n": "n8n workflows are triggered by webhook/schedule; record them with `kam log --surface n8n`.",
}


def dispatch(surface: str, prompt: str, settings: Settings, *, model: str | None = None, system: str | None = None,
             timeout: int | None = None, cwd: str | None = None) -> SurfaceResult:
    if surface == "claude-p":
        return claude_p.run(prompt if not system else f"{system}\n\n{prompt}", model=model, timeout=timeout or 900, cwd=cwd)
    if surface == "codex-exec":
        return codex.run(prompt if not system else f"{system}\n\n{prompt}", model=model, timeout=timeout or 900, cwd=cwd)
    if surface == "agy":
        return agy.run(prompt if not system else f"{system}\n\n{prompt}", model=model, timeout=timeout or 600, cwd=cwd)
    if surface == "openrouter":
        return openrouter.run(prompt, api_key=settings.require("OPENROUTER_API_KEY"), model=model, system=system, timeout=timeout or 120)
    if surface in DEFERRED:
        return SurfaceResult(ok=False, error=DEFERRED[surface])
    return SurfaceResult(ok=False, error=f"unknown surface '{surface}'")


ADAPTERS: dict[str, Callable] = {"claude-p": claude_p.run, "codex-exec": codex.run, "agy": agy.run, "openrouter": openrouter.run}
