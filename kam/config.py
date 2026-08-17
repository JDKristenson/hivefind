"""Configuration and secrets loading for KAM.

Order of precedence (PRD v1.1 §6.2, §12.3):
  1. process environment
  2. `op run --env-file kam/.env.op` (1Password references; only when a session or service-account token exists)
  3. ~/.config/kam/env.local  (Phase 0 bootstrap; `kam doctor` warns while it exists)
Secrets are never written anywhere by this module.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

HOME = Path.home()
DESKTOP = HOME / "Desktop"
PROJECTS_YAML = DESKTOP / "00 CIC" / "2 PROJECTS.yaml"
REPORTS_DIR = DESKTOP / "90 ENGINE ROOM" / "reports" / "kam"
OUTBOX_DIR = DESKTOP / "20 DECK" / "OUTBOX"
LANDINGS = DESKTOP / "20 DECK" / "LANDINGS.md"
BOOTSTRAP_ENV = HOME / ".config" / "kam" / "env.local"
PACKAGE_DIR = Path(__file__).resolve().parent
REPO_DIR = PACKAGE_DIR.parent
ENV_OP = PACKAGE_DIR / ".env.op"
REGISTRY_YAML = PACKAGE_DIR / "registry.yaml"
JOBS_YAML = PACKAGE_DIR / "jobs.yaml"
ANCHORS_DIR = PACKAGE_DIR / "anchors"

# Surfaces that never send content off-machine (mission fence, §6.2 step 3).
LOCAL_SURFACES = frozenset({"claude-p", "codex-exec", "agy", "hermes"})
# Which host serves which surface (§3.2).
SURFACE_HOSTS: dict[str, frozenset[str]] = {
    "claude-p": frozenset({"mac"}),
    "codex-exec": frozenset({"mac", "ec2"}),
    "agy": frozenset({"mac"}),
    "notion-ai": frozenset({"vendor"}),
    "pplx-computer": frozenset({"vendor"}),
    "manus": frozenset({"mac", "ec2"}),
    "hermes": frozenset({"ec2"}),
    "openrouter": frozenset({"mac", "ec2"}),
    "cf-browser": frozenset({"mac", "ec2"}),
    "n8n": frozenset({"vendor"}),
    "kam": frozenset({"mac", "ec2"}),
}
SURFACE_POOL: dict[str, str] = {
    "claude-p": "claude-max",
    "codex-exec": "chatgpt",
    "agy": "google-ultra",
    "notion-ai": "notion",
    "pplx-computer": "perplexity-max",
    "manus": "manus",
    "hermes": "anthropic-api",
    "openrouter": "openrouter",
    "cf-browser": "cloudflare",
    "n8n": "n8n",
    "kam": "none",
}

# Environment variables that must never reach a `claude -p` child (nested-session hang, subscription switch).
CLAUDE_P_UNSET = ("ANTHROPIC_API_KEY", "CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID")


def detect_host() -> str:
    """mac | ec2 | other. Override with KAM_HOST."""
    forced = os.environ.get("KAM_HOST")
    if forced:
        return forced
    if platform.system() == "Darwin":
        return "mac"
    if Path("/home/ec2-user").exists() or Path("/sys/hypervisor/uuid").exists():
        return "ec2"
    return "other"


def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _op_available() -> bool:
    if os.environ.get("KAM_SKIP_OP"):  # launchd/systemd jobs: never probe 1Password (no session, can hang on XPC)
        return False
    if not shutil.which("op") or not ENV_OP.exists():
        return False
    if os.environ.get("OP_SERVICE_ACCOUNT_TOKEN"):
        return True
    try:
        r = subprocess.run(["op", "whoami"], capture_output=True, text=True, timeout=10, check=False,
                           stdin=subprocess.DEVNULL, start_new_session=True)
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _load_via_op() -> dict[str, str]:
    """Resolve op:// references in .env.op through `op run`, returning only the resolved KAM_/NOTION_/OPENROUTER_ keys."""
    try:
        r = subprocess.run(
            ["op", "run", "--no-masking", "--env-file", str(ENV_OP), "--", "env"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {}
    if r.returncode != 0:
        return {}
    wanted = _parse_env_file(ENV_OP).keys()
    out: dict[str, str] = {}
    for line in r.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if k in wanted:
                out[k] = v
    return out


@dataclass
class Settings:
    host: str
    env: dict[str, str] = field(default_factory=dict)
    source: str = "process"  # process | op | bootstrap | none
    bootstrap_present: bool = False

    @property
    def db_dsn(self) -> str | None:
        return self.env.get("KAM_DB_DSN")

    @property
    def openrouter_key(self) -> str | None:
        return self.env.get("OPENROUTER_API_KEY")

    @property
    def notion_token(self) -> str | None:
        return self.env.get("NOTION_TOKEN")

    def require(self, key: str) -> str:
        v = self.env.get(key)
        if not v:
            raise RuntimeError(f"missing secret {key}; run `kam doctor`")
        return v


def load_settings() -> Settings:
    env: dict[str, str] = {}
    source = "none"
    if _op_available():
        env.update(_load_via_op())
        if env:
            source = "op"
    bootstrap = _parse_env_file(BOOTSTRAP_ENV)
    if bootstrap:
        for k, v in bootstrap.items():
            env.setdefault(k, v)
        if source == "none":
            source = "bootstrap"
    for k in ("KAM_DB_DSN", "OPENROUTER_API_KEY", "NOTION_TOKEN", "KAM_HOST", "MANUS_API_KEY", "CF_ACCOUNT_ID", "CF_API_TOKEN"):
        if os.environ.get(k):
            env[k] = os.environ[k]
            source = "process" if source == "none" else source
    return Settings(host=detect_host(), env=env, source=source, bootstrap_present=BOOTSTRAP_ENV.exists())
