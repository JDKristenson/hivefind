"""OpenRouter (metered). Auxiliary work: titles, classification, compression. Usage and cost come back in the response."""

from __future__ import annotations

import httpx

from .base import SurfaceResult

DEFAULT_MODEL = "anthropic/claude-haiku-4.5"
URL = "https://openrouter.ai/api/v1/chat/completions"


def parse_response(obj: dict) -> SurfaceResult:
    choices = obj.get("choices") or []
    text = ""
    if choices:
        msg = choices[0].get("message") or {}
        text = msg.get("content") or ""
        if isinstance(text, list):
            text = " ".join(str(c.get("text", "")) if isinstance(c, dict) else str(c) for c in text)
    usage = obj.get("usage") or {}
    cost = usage.get("cost")
    return SurfaceResult(
        ok=bool(text) and not obj.get("error"),
        text=str(text).strip(), model=obj.get("model"),
        tokens_in=usage.get("prompt_tokens"), tokens_out=usage.get("completion_tokens"),
        cost_usd=float(cost) if cost is not None else None,
        target_ref=f"openrouter:{obj.get('id')}" if obj.get("id") else None,
        raw={k: obj.get(k) for k in ("id", "model", "usage", "error")},
        error=str(obj.get("error")) if obj.get("error") else None,
    )


def run(prompt: str, *, api_key: str, model: str | None = None, system: str | None = None, timeout: int = 120) -> SurfaceResult:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = {"model": model or DEFAULT_MODEL, "messages": messages, "usage": {"include": True}}
    headers = {"Authorization": f"Bearer {api_key}", "HTTP-Referer": "https://github.com/JDKristenson/hivefind", "X-Title": "KAM"}
    try:
        r = httpx.post(URL, json=body, headers=headers, timeout=timeout)
    except httpx.HTTPError as e:
        return SurfaceResult(ok=False, error=f"openrouter http error: {e}")
    try:
        obj = r.json()
    except ValueError:
        return SurfaceResult(ok=False, error=f"openrouter non-JSON response {r.status_code}: {r.text[:300]}")
    res = parse_response(obj)
    if r.status_code >= 400 and res.error is None:
        res.ok = False
        res.error = f"openrouter HTTP {r.status_code}"
    return res
