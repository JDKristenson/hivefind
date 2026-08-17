"""Antigravity CLI (`agy --print`) under the Google sign-in. Text output only; no JSON, no usage (verified 2026-08-17)."""

from __future__ import annotations

import shutil
import subprocess

from .base import SurfaceResult


def run(prompt: str, *, model: str | None = None, timeout: int = 600, cwd: str | None = None) -> SurfaceResult:
    exe = shutil.which("agy") or "/Users/JDKristenson/.local/bin/agy"
    if not shutil.which(exe) and not exe.startswith("/"):
        return SurfaceResult(ok=False, error="agy CLI not found")
    cmd = [exe, "--print", prompt, "--print-timeout", f"{max(60, timeout - 30)}s"]
    if model:
        cmd += ["--model", model]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd, stdin=subprocess.DEVNULL, check=False)
    except subprocess.TimeoutExpired:
        return SurfaceResult(ok=False, error=f"agy timed out after {timeout}s")
    except OSError as e:
        return SurfaceResult(ok=False, error=f"agy launch failed: {e}")
    text = p.stdout.strip()
    if p.returncode != 0 and not text:
        return SurfaceResult(ok=False, error=f"agy exit {p.returncode}: {p.stderr[-500:]}")
    return SurfaceResult(ok=bool(text), text=text, model=model or "agy-default",
                         tokens_in=None, tokens_out=None, cost_usd=None, raw={"stderr_tail": p.stderr[-500:]})
