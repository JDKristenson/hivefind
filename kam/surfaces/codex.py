"""codex exec --json under the ChatGPT login (subscription pool). Parses the JSONL event stream for usage and the final message."""

from __future__ import annotations

import json
import shutil
import subprocess

from .base import SurfaceResult


def parse_jsonl(stdout: str) -> SurfaceResult:
    tin = tout = 0
    saw_usage = False
    last_text = ""
    error = None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        usage = ev.get("usage") or (ev.get("item") or {}).get("usage") if isinstance(ev.get("item"), dict) else ev.get("usage")
        if isinstance(usage, dict) and ("input_tokens" in usage or "output_tokens" in usage):
            saw_usage = True
            tin += int(usage.get("input_tokens") or 0) + int(usage.get("cached_input_tokens") or 0)
            tout += int(usage.get("output_tokens") or 0)
        item = ev.get("item")
        if isinstance(item, dict) and item.get("type") in ("agent_message", "assistant_message", "message"):
            txt = item.get("text") or item.get("content")
            if isinstance(txt, list):
                txt = " ".join(str(c.get("text", "")) if isinstance(c, dict) else str(c) for c in txt)
            if txt:
                last_text = str(txt)
        if ev.get("type") in ("error", "turn.failed"):
            error = str(ev.get("message") or ev.get("error") or ev)
        if ev.get("type") == "turn.completed" and isinstance(ev.get("usage"), dict):
            pass  # already counted above
    if not last_text:
        # fall back to the last non-JSON line, codex prints the final answer plainly in some versions
        plain = [l for l in stdout.splitlines() if l.strip() and not l.strip().startswith("{")]
        last_text = plain[-1].strip() if plain else ""
    return SurfaceResult(
        ok=error is None and bool(last_text), text=last_text,
        tokens_in=tin if saw_usage else None, tokens_out=tout if saw_usage else None,
        cost_usd=None, raw={"stdout_tail": stdout[-2000:]}, error=error,
    )


def run(prompt: str, *, model: str | None = None, timeout: int = 900, cwd: str | None = None) -> SurfaceResult:
    exe = shutil.which("codex")
    if not exe:
        return SurfaceResult(ok=False, error="codex CLI not found on PATH")
    cmd = [exe, "exec", "--json", "--skip-git-repo-check"]
    if model:
        cmd += ["-m", model]
    cmd.append(prompt)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd, check=False)
    except subprocess.TimeoutExpired:
        return SurfaceResult(ok=False, error=f"codex exec timed out after {timeout}s")
    res = parse_jsonl(p.stdout)
    if p.returncode != 0 and not res.ok:
        res.error = res.error or f"codex exec exit {p.returncode}: {p.stderr[-500:]}"
    res.model = model or "codex-default"
    return res
