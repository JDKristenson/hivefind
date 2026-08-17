"""`kam doctor` (PRD v1.1 §6.2): shell hazards, secrets on disk, .env.op hygiene, bootstrap warning, surfaces on this host, DB reachability."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import BOOTSTRAP_ENV, CLAUDE_P_UNSET, ENV_OP, PACKAGE_DIR, REPO_DIR, SURFACE_HOSTS, Settings
from .db import DB, DBUnavailable

SECRET_PATTERNS = (
    re.compile(r"sk-or-v1-[A-Za-z0-9]{20,}"),                # OpenRouter
    re.compile(r"sk-ant-[A-Za-z0-9-]{20,}"),                 # Anthropic
    re.compile(r"ntn_[A-Za-z0-9]{20,}|secret_[A-Za-z0-9]{30,}"),  # Notion
    re.compile(r"postgres(ql)?://[A-Za-z0-9_.-]+:[A-Za-z0-9%._~-]{8,}@[A-Za-z0-9.-]+"),  # DSN with a real password
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}"),  # JWT
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    level: str = "error"  # error | warn | info


def _scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for root in paths:
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix in (".pyc",) or ".git" in p.parts or "__pycache__" in p.parts:
                continue
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                continue
            for pat in SECRET_PATTERNS:
                if pat.search(text):
                    hits.append(f"{p.relative_to(REPO_DIR)} matches {pat.pattern[:24]}…")
                    break
    return hits


def run_checks(settings: Settings, *, check_db: bool = True) -> list[Check]:
    out: list[Check] = []
    # shell hazards
    present = [k for k in CLAUDE_P_UNSET if os.environ.get(k)]
    out.append(Check("shell env", not any(k == "ANTHROPIC_API_KEY" for k in present),
                     ("ANTHROPIC_API_KEY is set in this shell: claude -p would bill the API, not Max" if "ANTHROPIC_API_KEY" in present
                      else "no ANTHROPIC_API_KEY in shell") + (f"; nested-session vars present: {[k for k in present if k != 'ANTHROPIC_API_KEY']} (kam run claude-p refuses here)" if any(k != "ANTHROPIC_API_KEY" for k in present) else ""),
                     "warn" if present and "ANTHROPIC_API_KEY" not in present else "error"))
    # secrets in scope
    hits = _scan_secrets([PACKAGE_DIR, REPO_DIR / "scripts"] if (REPO_DIR / "scripts").exists() else [PACKAGE_DIR])
    out.append(Check("secrets on disk (kam/, scripts/)", not hits, "; ".join(hits) if hits else "none found"))
    # .env.op hygiene
    if ENV_OP.exists():
        bad = [l for l in ENV_OP.read_text().splitlines() if "=" in l and not l.strip().startswith("#") and "op://" not in l]
        out.append(Check(".env.op references only", not bad, "; ".join(bad)[:200] if bad else "all values are op:// references"))
    else:
        out.append(Check(".env.op present", False, "kam/.env.op missing", "warn"))
    # bootstrap
    out.append(Check("bootstrap secrets file", not BOOTSTRAP_ENV.exists(),
                     f"{BOOTSTRAP_ENV} exists (Phase 0 bootstrap); move its values into 1Password and delete it" if BOOTSTRAP_ENV.exists() else "absent",
                     "warn"))
    if BOOTSTRAP_ENV.exists():
        mode = oct(BOOTSTRAP_ENV.stat().st_mode & 0o777)
        out.append(Check("bootstrap file mode", mode == "0o600", f"mode {mode}", "error" if mode != "0o600" else "info"))
    # secret source
    out.append(Check("secret source", settings.source in ("op", "bootstrap", "process"), f"source={settings.source}", "info"))
    # surfaces on this host
    served = sorted(s for s, hosts in SURFACE_HOSTS.items() if settings.host in hosts)
    out.append(Check("host", True, f"{settings.host}: serves {served}", "info"))
    for exe, surf in (("claude", "claude-p"), ("codex", "codex-exec"), ("agy", "agy"), ("op", "1password"), ("uv", "uv")):
        out.append(Check(f"binary {exe}", shutil.which(exe) is not None or (exe == "agy" and Path.home().joinpath('.local/bin/agy').exists()),
                         shutil.which(exe) or ("~/.local/bin/agy" if exe == "agy" and Path.home().joinpath('.local/bin/agy').exists() else "not found"), "warn"))
    if shutil.which("op"):
        try:
            r = subprocess.run(["op", "whoami"], capture_output=True, text=True, timeout=8, check=False)
            out.append(Check("1Password session", r.returncode == 0, "signed in" if r.returncode == 0 else "not signed in (op signin) and no OP_SERVICE_ACCOUNT_TOKEN", "warn"))
        except (OSError, subprocess.TimeoutExpired):
            out.append(Check("1Password session", False, "op did not respond", "warn"))
    # git
    try:
        r = subprocess.run(["git", "-C", str(REPO_DIR), "rev-parse", "--verify", "origin/main"], capture_output=True, text=True, timeout=8, check=False)
        out.append(Check("origin/main", r.returncode == 0, "present" if r.returncode == 0 else "missing", "warn"))
    except (OSError, subprocess.TimeoutExpired):
        out.append(Check("origin/main", False, "git unavailable", "warn"))
    # db
    if check_db:
        try:
            db = DB(settings)
            v = db.verify()
            out.append(Check("database", True, f"kam.verify ok={v['ok']} checked={v['checked']} head={str(v['head_hash'])[:12]}…", "info" if v["ok"] else "error"))
            out.append(Check("kill switch readable", True, "kam.flags read ok; global paused=" + str(db.is_paused()), "info"))
        except DBUnavailable as e:
            out.append(Check("database", False, f"unreachable: {str(e)[:120]}"))
    return out


def format_report(checks: list[Check]) -> str:
    lines = []
    for c in checks:
        mark = "OK  " if c.ok else ("WARN" if c.level == "warn" else "FAIL")
        if c.ok and c.level == "warn":
            mark = "OK  "
        lines.append(f"{mark} {c.name}: {c.detail}")
    return "\n".join(lines)


def exit_code(checks: list[Check]) -> int:
    return 1 if any((not c.ok) and c.level == "error" for c in checks) else 0
