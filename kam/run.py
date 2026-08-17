"""`kam run`: the dispatch verb (PRD v1.1 §6.2). Exit codes: 0 receipted, 3 staged, 4 refused, 5 surface error."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime

from . import gates, missions
from .config import SURFACE_HOSTS, SURFACE_POOL, Settings
from .db import DB, DBUnavailable
from .log import uuid7
from .registry import Registry
from .staging import stage
from .surfaces import dispatch

EXIT_OK, EXIT_STAGED, EXIT_REFUSED, EXIT_SURFACE = 0, 3, 4, 5


@dataclass
class RunRequest:
    mission: str
    agent: str
    task_class: str
    prompt: str
    surface: str | None = None
    gate: str | None = None
    parent_run: str | None = None
    model: str | None = None
    dry_run: bool = False
    fields_used: set[str] = field(default_factory=set)
    confidentiality: str | None = None
    subject: str = ""
    timeout: int | None = None


@dataclass
class RunOutcome:
    exit_code: int
    run_id: str | None
    state: str
    message: str
    result_text: str = ""
    target_ref: str | None = None


def _refuse(msg: str) -> RunOutcome:
    return RunOutcome(EXIT_REFUSED, None, "refused", msg)


def execute(req: RunRequest, settings: Settings, *, registry: Registry | None = None, db: DB | None = None,
            out=sys.stderr) -> RunOutcome:
    registry = registry or Registry.load()
    host = settings.host

    # 1. flags, fail closed
    try:
        db = db or DB(settings)
        if db.is_paused(req.agent):
            return _refuse(f"paused (kam.flags): global or agent '{req.agent}'")
    except DBUnavailable as e:
        return _refuse(f"kill switch unreadable, refusing (fail closed): {e}")

    # 2. registry
    try:
        agent = registry.get(req.agent)
    except KeyError as e:
        return _refuse(str(e))
    if agent.paused:
        return _refuse(f"agent '{agent.name}' is paused in the registry")
    surface = req.surface or agent.default_surface
    if not agent.allows(surface):
        return _refuse(f"surface '{surface}' is not in {agent.name}.allowed_surfaces {agent.allowed_surfaces}")

    # 3. mission fence
    mission = missions.resolve(req.mission)
    ok, why = missions.surface_allowed_for(mission, surface)
    if not ok:
        return _refuse(why)

    # 4. host check
    hosts = SURFACE_HOSTS.get(surface)
    if hosts is None:
        return _refuse(f"unknown surface '{surface}'")
    if host not in hosts:
        return _refuse(f"surface {surface} is served by host {sorted(hosts)}; this host is {host}")

    # 5. confidential-move rule
    prov_ok, prov_why = gates.prompt_provenance_ok(req.fields_used, req.confidentiality)
    gate = req.gate
    if not prov_ok:
        gate = "confidential_move"
    decision = gates.decide(gate, agent.gates)

    # injection check on the inbound prompt
    inj = gates.find_injection(req.prompt)

    run_id = uuid7()
    run_meta = {
        "mission": mission.id, "agent": agent.name, "surface": surface, "host": host,
        "pool": SURFACE_POOL.get(surface, "unknown"), "model": req.model, "task_class": req.task_class,
        "gate": decision.gate, "parent_run": req.parent_run,
    }
    if req.dry_run:
        return RunOutcome(EXIT_OK, None, "dry-run", f"would run on {surface} as {agent.name}; gate={decision.gate} stage={decision.stage}; {prov_why}")

    # 6. intent
    db.log(run_id, "intended", summary=f"{req.task_class}: {req.subject or req.prompt[:80]}", run=run_meta)
    if inj:
        db.log(run_id, "failed", summary=f"injection pattern: {inj[:60]}")
        return RunOutcome(EXIT_SURFACE, run_id, "failed", f"injection pattern found in prompt: {inj!r}; run refused and logged")
    db.log(run_id, "executing", summary=decision.reason)

    # 7. gate: prepare then stage
    if decision.stage:
        prep = dispatch(surface, req.prompt, settings, model=req.model, system=gates.SYSTEM_PREAMBLE, timeout=req.timeout)
        if not prep.ok:
            db.log(run_id, "failed", summary=f"preparation failed on {surface}: {prep.error}", tokens_in=prep.tokens_in,
                   tokens_out=prep.tokens_out, cost_usd=prep.cost_usd)
            return RunOutcome(EXIT_SURFACE, run_id, "failed", prep.error or "preparation failed")
        ref, note = stage(agent.stage_to, agent=agent.name, subject=req.subject or req.task_class, body=prep.text, run_id=run_id)
        db.log(run_id, "staged_for_approval", summary=f"{decision.gate}: {note}", target_ref=ref or None,
               tokens_in=prep.tokens_in, tokens_out=prep.tokens_out, cost_usd=prep.cost_usd)
        return RunOutcome(EXIT_STAGED, run_id, "staged_for_approval", f"staged: {note}", prep.text, ref)

    # 8. execute
    res = dispatch(surface, req.prompt, settings, model=req.model, system=gates.SYSTEM_PREAMBLE, timeout=req.timeout)
    if not res.ok:
        db.log(run_id, "failed", summary=f"{surface}: {res.error}", target_ref=res.target_ref,
               tokens_in=res.tokens_in, tokens_out=res.tokens_out, cost_usd=res.cost_usd)
        return RunOutcome(EXIT_SURFACE, run_id, "failed", res.error or "surface error", res.text, res.target_ref)
    # 9. receipt
    db.log(run_id, "receipted", summary=(res.text or "")[:200].replace("\n", " "), target_ref=res.target_ref,
           tokens_in=res.tokens_in, tokens_out=res.tokens_out, cost_usd=res.cost_usd)
    return RunOutcome(EXIT_OK, run_id, "receipted", f"receipted on {surface} ({res.model})", res.text, res.target_ref)


def record_external(settings: Settings, *, mission: str, agent: str, surface: str, state: str, summary: str,
                    target_ref: str | None, task_class: str = "glue", host: str = "vendor",
                    parent_run: str | None = None, cost_usd: float | None = None) -> str:
    """`kam log`: record a run that happened on a surface kam cannot drive (Perplexity, Notion AI, n8n)."""
    db = DB(settings)
    run_id = uuid7()
    meta = {"mission": mission, "agent": agent, "surface": surface, "host": host, "pool": SURFACE_POOL.get(surface, "unknown"),
            "task_class": task_class, "parent_run": parent_run}
    db.log(run_id, "intended", summary=summary, run=meta)
    db.log(run_id, state, summary=summary, target_ref=target_ref, cost_usd=cost_usd)
    return run_id


def approve(settings: Settings, run_id: str, object_id: str | None) -> str:
    db = DB(settings)
    db.log(run_id, "approved", summary=f"JD attestation{': ' + object_id if object_id else ''}")
    db.log(run_id, "executed", summary="executed in host tool (attested)")
    r = db.log(run_id, "receipted", summary="receipt by attestation (kam approve)", target_ref=object_id)
    return r.row_hash


def heartbeat(settings: Settings, job_id: str, host: str, note: str = "") -> str:
    db = DB(settings)
    run_id = uuid7()
    meta = {"mission": "TEC-agentic-os", "agent": f"job:{job_id}", "surface": "kam", "host": host, "pool": "none", "task_class": "glue"}
    db.log(run_id, "heartbeat", summary=note or f"heartbeat {job_id}", run=meta, at=datetime.now(UTC))
    return run_id
