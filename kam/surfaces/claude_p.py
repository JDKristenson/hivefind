"""claude -p under the Max login. Child env is CONSTRUCTED with the four hazardous variables removed
(ANTHROPIC_API_KEY switches Claude Code off the subscription; CLAUDECODE / CLAUDE_CODE_* cause the nested-session hang).
Never invoke from inside a Claude Code session; the wrapper refuses if CLAUDECODE is set and KAM_ALLOW_NESTED is not.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

from ..config import CLAUDE_P_UNSET
from .base import SurfaceResult

DEFAULT_MODEL = "claude-fable-5"


def child_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base is None else base)
    for k in CLAUDE_P_UNSET:
        env.pop(k, None)
    return env


def parse_json_result(stdout: str) -> SurfaceResult:
    """`claude -p --output-format json` prints one JSON object (result, total_cost_usd, usage, session_id, is_error)."""
    stdout = stdout.strip()
    try:
        obj = json.loads(stdout)
    except json.JSONDecodeError:
        # some versions print stream lines; take the last JSON object that has 'result'
        obj = None
        for line in reversed(stdout.splitlines()):
            try:
                cand = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(cand, dict) and ("result" in cand or "total_cost_usd" in cand):
                obj = cand
                break
        if obj is None:
            return SurfaceResult(ok=False, error="claude -p returned no JSON", raw={"stdout": stdout[-2000:]})
    usage = obj.get("usage") or {}
    tin = usage.get("input_tokens")
    tout = usage.get("output_tokens")
    if tin is not None:
        tin = int(tin) + int(usage.get("cache_read_input_tokens") or 0) + int(usage.get("cache_creation_input_tokens") or 0)
    cost = obj.get("total_cost_usd")
    return SurfaceResult(
        ok=not obj.get("is_error", False),
        text=str(obj.get("result", "")),
        model=(obj.get("model") or (usage.get("model") if isinstance(usage, dict) else None)),
        tokens_in=tin, tokens_out=int(tout) if tout is not None else None,
        cost_usd=float(cost) if cost is not None else None,
        target_ref=f"claude-session:{obj.get('session_id')}" if obj.get("session_id") else None,
        raw=obj, error=(str(obj.get("result")) if obj.get("is_error") else None),
    )


def run(prompt: str, *, model: str | None = None, timeout: int = 900, cwd: str | None = None) -> SurfaceResult:
    if os.environ.get("CLAUDECODE") and not os.environ.get("KAM_ALLOW_NESTED"):
        return SurfaceResult(ok=False, error="refusing to run claude -p from inside a Claude Code session (nested invocation hangs); run from a plain terminal or launchd")
    exe = shutil.which("claude")
    if not exe:
        return SurfaceResult(ok=False, error="claude CLI not found on PATH")
    cmd = [exe, "-p", "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    cmd.append(prompt)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=child_env(), cwd=cwd, check=False, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return SurfaceResult(ok=False, error=f"claude -p timed out after {timeout}s")
    fx = os.environ.get("KAM_FIXTURE_DIR")
    if fx and p.stdout.strip():
        try:
            from pathlib import Path
            Path(fx).mkdir(parents=True, exist_ok=True)
            Path(fx, "claude-p.json").write_text(p.stdout)
        except OSError:
            pass
    if p.returncode != 0 and not p.stdout.strip():
        return SurfaceResult(ok=False, error=f"claude -p exit {p.returncode}: {p.stderr[-500:]}")
    res = parse_json_result(p.stdout)
    if res.model is None:
        res.model = model or DEFAULT_MODEL
    return res
