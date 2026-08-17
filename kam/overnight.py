"""`kam overnight`: render the Overnight report (PRD v1.1 §6.4). One query, rendered by whichever host is up; /POD reads the newest."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import REPORTS_DIR, Settings
from .db import DB
from .jobs import health, load_jobs

ET = ZoneInfo("America/New_York")


def _fmt(dt: datetime | None) -> str:
    return dt.astimezone(ET).strftime("%m-%d %H:%M") if dt else "never"


def render(settings: Settings, now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    db = DB(settings)
    since = now - timedelta(days=1)
    runs = db.runs_with_latest(since)
    spend = db.spend_by_pool(now - timedelta(days=7))
    anchor = db.latest_anchor()
    head = db.chain_head()
    hb = db.latest_heartbeats()
    jobs = load_jobs()
    hrows = health(jobs, hb, now)

    by_agent: dict[str, list] = {}
    staged: list = []
    stuck: list = []
    for r in runs:
        if r["agent"].startswith("job:"):
            continue
        by_agent.setdefault(r["agent"], []).append(r)
        if r["state"] == "staged_for_approval":
            staged.append(r)
            if now - r["last_at"] > timedelta(hours=24):
                stuck.append(r)

    L: list[str] = []
    L.append(f"# KAM Overnight, {now.astimezone(ET):%A %Y-%m-%d %H:%M} ET (host {settings.host})")
    L.append("")
    L.append("## Runs, last 24h")
    if not by_agent:
        L.append("- none")
    for agent, rs in sorted(by_agent.items()):
        states = {}
        for r in rs:
            states[r["state"]] = states.get(r["state"], 0) + 1
        L.append(f"- {agent}: {len(rs)} run(s), " + ", ".join(f"{k} {v}" for k, v in sorted(states.items())))
        for r in rs[:5]:
            ref = f" -> {r['target_ref']}" if r.get("target_ref") else ""
            L.append(f"    - {_fmt(r['last_at'])} {r['surface']} [{r['state']}] {str(r.get('summary') or '')[:90]}{ref}")
    L.append("")
    L.append("## Awaiting your approval")
    if not staged:
        L.append("- none")
    for r in staged:
        L.append(f"- {r['agent']} {r['run_id']} staged {_fmt(r['last_at'])}: {str(r.get('summary') or '')[:80]} -> {r.get('target_ref') or '(no ref)'}")
    if stuck:
        L.append("")
        L.append("## Stuck > 24h in staged_for_approval")
        for r in stuck:
            L.append(f"- {r['agent']} {r['run_id']} since {_fmt(r['last_at'])}")
    L.append("")
    L.append("## Spend by pool, last 7 days")
    if not spend:
        L.append("- none")
    for s in spend:
        cost = "unmetered by vendor" if s["cost_usd"] is None else f"${float(s['cost_usd']):.4f}"
        L.append(f"- {s['pool']}: {s['runs']} run(s), tokens in/out {s['tokens_in'] or 0}/{s['tokens_out'] or 0}, {cost}"
                 + (f", {s['unmetered_events']} unmetered event(s)" if s["unmetered_events"] else ""))
    L.append("")
    L.append("## Chain")
    L.append(f"- head {head['head_hash'][:16]}… over {head['event_count']} events (updated {_fmt(head['updated_at'])})")
    if anchor:
        L.append(f"- last anchor {anchor['day']}: {anchor['head_hash'][:16]}… at {anchor['event_count']} events")
    else:
        L.append("- no anchor written yet")
    L.append("")
    L.append("## Job health (manifest vs heartbeats)")
    if not hrows:
        L.append("- no jobs in kam/jobs.yaml")
    for h in hrows:
        flag = "MISSING" if h["stale"] else "ok"
        L.append(f"- {flag:7} {h['job_id']} ({h['host']}, {h['cadence']}) last {_fmt(h['last'])}")
    L.append("")
    return "\n".join(L)


def write(settings: Settings, out_dir: Path | None = None, now: datetime | None = None) -> Path:
    now = now or datetime.now(UTC)
    out_dir = out_dir or REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    text = render(settings, now)
    p = out_dir / f"overnight-{now.astimezone(ET):%Y-%m-%d}.md"
    p.write_text(text)
    return p
