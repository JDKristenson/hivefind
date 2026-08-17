"""Staging targets for gated actions (PRD v1.1 §6.9). v1: local-drafts (20 DECK/OUTBOX). Notion Ready to Send and
Gmail drafts arrive with the Notion token (Phase 1/2). The wrapper never sends anything."""

from __future__ import annotations

import re
from datetime import datetime

from .config import LANDINGS, OUTBOX_DIR


def _slug(s: str, n: int = 40) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:n] or "draft"


def stage_local_draft(agent: str, subject: str, body: str, run_id: str, now: datetime | None = None) -> str:
    """Write the draft as a single file into 20 DECK/OUTBOX (files, never folders) and log the landing. Returns the path."""
    now = now or datetime.now().astimezone()
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    name = f"{now:%Y-%m-%d} kam - draft-{_slug(agent)}-{_slug(subject)}.md"
    path = OUTBOX_DIR / name
    path.write_text(
        f"# DRAFT (staged by KAM, not sent)\n\n"
        f"- agent: {agent}\n- run_id: {run_id}\n- staged_at: {now:%Y-%m-%d %H:%M}\n- subject: {subject}\n\n---\n\n{body}\n"
    )
    try:
        with LANDINGS.open("a") as f:
            f.write(f"{now:%Y-%m-%d %H:%M} | kam | 20 DECK/OUTBOX/{name} | ACT: review draft, send by hand, then kam approve {run_id}\n")
    except OSError:
        pass
    return str(path)


def stage(target: str, *, agent: str, subject: str, body: str, run_id: str) -> tuple[str, str]:
    """Returns (target_ref, note)."""
    if target in ("local-drafts", "mail-drafts", "outbox"):
        p = stage_local_draft(agent, subject, body, run_id)
        return f"file://{p}", "staged to 20 DECK/OUTBOX (mail drafts via n8n arrive in Phase 2)"
    if target == "notion-ready-to-send":
        return "", "notion-ready-to-send needs NOTION_TOKEN and the Ready to Send DB id (Phase 1); nothing staged"
    return "", f"unknown staging target '{target}'"
