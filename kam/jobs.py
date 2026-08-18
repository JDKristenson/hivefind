"""Jobs manifest, heartbeats, and the watchdog (PRD v1.1 §6.12). Silence becomes visible by enumerating what should run."""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from .config import JOBS_YAML

DOW = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


@dataclass
class Job:
    job_id: str
    host: str
    cadence: str
    grace_minutes: int = 30
    expected_artifact: str | None = None
    description: str = ""


def load_jobs(path: Path = JOBS_YAML) -> list[Job]:
    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    out: list[Job] = []
    for j in (data or {}).get("jobs", []):
        out.append(Job(job_id=j["job_id"], host=j.get("host", "ec2"), cadence=str(j.get("cadence", "every 60m")),
                       grace_minutes=int(j.get("grace_minutes", 30)), expected_artifact=j.get("expected_artifact"),
                       description=j.get("description", "")))
    return out


def expected_interval(cadence: str) -> timedelta:
    """every 5m | every 2h | daily HH:MM | weekly <dow> HH:MM | hourly."""
    c = cadence.strip().lower()
    if c == "hourly":
        return timedelta(hours=1)
    m = re.match(r"every\s+(\d+)\s*(m|min|minutes?|h|hours?)$", c)
    if m:
        n = int(m.group(1))
        return timedelta(minutes=n) if m.group(2).startswith("m") else timedelta(hours=n)
    if c.startswith("daily"):
        return timedelta(days=1)
    if c.startswith("weekly") or c.split()[0][:3] in DOW:
        return timedelta(days=7)
    return timedelta(hours=1)


def is_stale(job: Job, last: datetime | None, now: datetime | None = None, first_seen: datetime | None = None) -> bool:
    """A job is stale when its last heartbeat is older than cadence + grace. A job that has never run is stale only
    once it has existed (first_seen) longer than cadence + grace; before that it is simply not due yet."""
    now = now or datetime.now(UTC)
    window = expected_interval(job.cadence) + timedelta(minutes=job.grace_minutes)
    if last is None:
        if first_seen is None:
            return True
        return now - first_seen > window
    return now - last > window


def artifact_present(job: Job, since: datetime) -> bool | None:
    """Vendor-side jobs prove themselves by their artifact. file:<glob> checks mtime; others return None (unknown)."""
    if not job.expected_artifact:
        return None
    kind, _, spec = job.expected_artifact.partition(":")
    if kind == "file":
        for p in glob.glob(os.path.expanduser(spec)):
            if datetime.fromtimestamp(os.path.getmtime(p), UTC) >= since:
                return True
        return False
    return None


def health(jobs: list[Job], heartbeats: dict[str, datetime], now: datetime | None = None,
           first_seen: dict[str, datetime] | None = None) -> list[dict[str, Any]]:
    now = now or datetime.now(UTC)
    first_seen = first_seen or {}
    rows = []
    for j in jobs:
        last = heartbeats.get(j.job_id)
        stale = is_stale(j, last, now, first_seen.get(j.job_id))
        not_due = last is None and not stale
        rows.append({"job_id": j.job_id, "host": j.host, "cadence": j.cadence, "last": last, "stale": stale, "not_due": not_due})
    return rows


def missed_event_due(job: Job, last_failed: datetime | None, now: datetime | None = None) -> bool:
    """Write at most one 'missed' event per job per max(cadence+grace, 60 min)."""
    now = now or datetime.now(UTC)
    if last_failed is None:
        return True
    window = max(expected_interval(job.cadence) + timedelta(minutes=job.grace_minutes), timedelta(minutes=60))
    return now - last_failed > window
