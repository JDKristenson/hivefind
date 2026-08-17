"""`kam mirror`: upsert runs into the existing HiveFind 🛰️ Agent Runs data source (PRD v1.1 §6.3, §7.4).
Needs NOTION_TOKEN (an internal integration shared with the Agent Runs DB). Schema-tolerant: maps by property name and type."""

from __future__ import annotations

import time
from typing import Any

import httpx

from .config import Settings
from .db import DB

AGENT_RUNS_DATA_SOURCE = "4210943f-6d78-4c1d-83a6-0ec1cecec668"
NOTION_VERSION = "2025-09-03"
API = "https://api.notion.com/v1"

STATUS_MAP = {
    "intended": "Running", "executing": "Running", "staged_for_approval": "Drafted",
    "approved": "Published", "executed": "Published", "failed": "Failed", "cancelled": "Cancelled",
}


def status_for(state: str, gate: str | None) -> str | None:
    if state == "receipted":
        return "Published" if gate else "Reviewed"
    if state == "heartbeat":
        return None
    return STATUS_MAP.get(state, "Running")


class Notion:
    def __init__(self, token: str) -> None:
        self.h = {"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION, "Content-Type": "application/json"}
        self._last = 0.0

    def _throttle(self) -> None:  # <= 3 requests per second
        gap = time.monotonic() - self._last
        if gap < 0.34:
            time.sleep(0.34 - gap)
        self._last = time.monotonic()

    def get(self, path: str) -> dict:
        self._throttle()
        r = httpx.get(f"{API}{path}", headers=self.h, timeout=30)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, body: dict) -> dict:
        self._throttle()
        r = httpx.post(f"{API}{path}", headers=self.h, json=body, timeout=30)
        r.raise_for_status()
        return r.json()

    def patch(self, path: str, body: dict) -> dict:
        self._throttle()
        r = httpx.patch(f"{API}{path}", headers=self.h, json=body, timeout=30)
        r.raise_for_status()
        return r.json()


def build_properties(schema: dict[str, dict], run: dict[str, Any]) -> dict[str, Any]:
    """Map a run row onto whatever properties the data source has. Unknown names are skipped."""
    props: dict[str, Any] = {}
    title_name = next((n for n, p in schema.items() if p.get("type") == "title"), None)
    if title_name:
        props[title_name] = {"title": [{"text": {"content": f"{run['agent']} · {run['task_class']} · {run['run_id'][-8:]}"}}]}
    st = status_for(run["state"], run.get("gate"))
    if "Status" in schema and st:
        t = schema["Status"].get("type")
        props["Status"] = {t: {"name": st}} if t in ("status", "select") else props.get("Status", {})
    if "KAM run id" in schema:
        props["KAM run id"] = {"rich_text": [{"text": {"content": run["run_id"]}}]}
    if "Surface" in schema and schema["Surface"].get("type") == "select":
        props["Surface"] = {"select": {"name": run["surface"]}}
    if "Output Summary" in schema and schema["Output Summary"].get("type") == "rich_text":
        props["Output Summary"] = {"rich_text": [{"text": {"content": str(run.get("summary") or "")[:1900]}}]}
    if "Run Date" in schema and schema["Run Date"].get("type") == "date":
        props["Run Date"] = {"date": {"start": run["created_at"].isoformat()}}
    if "Trigger Source" in schema and schema["Trigger Source"].get("type") == "select":
        props["Trigger Source"] = {"select": {"name": "KAM"}}
    if "Run Type" in schema and schema["Run Type"].get("type") == "select":
        props["Run Type"] = {"select": {"name": run["task_class"]}}
    return props


def sync(settings: Settings, limit: int = 200) -> tuple[int, int]:
    """Returns (created, updated)."""
    token = settings.require("NOTION_TOKEN")
    n = Notion(token)
    db = DB(settings)
    ds = n.get(f"/data_sources/{AGENT_RUNS_DATA_SOURCE}")
    schema = ds.get("properties", {})
    created = updated = 0
    for run in db.unmirrored_runs()[:limit]:
        if run["agent"].startswith("job:"):
            db.mark_mirrored(run["run_id"], "skipped:job")
            continue
        props = build_properties(schema, run)
        if run.get("notion_page_id") and not run["notion_page_id"].startswith("skipped"):
            n.patch(f"/pages/{run['notion_page_id']}", {"properties": props})
            db.mark_mirrored(run["run_id"], run["notion_page_id"])
            updated += 1
        else:
            page = n.post("/pages", {"parent": {"type": "data_source_id", "data_source_id": AGENT_RUNS_DATA_SOURCE}, "properties": props})
            db.mark_mirrored(run["run_id"], page["id"])
            created += 1
    return created, updated
