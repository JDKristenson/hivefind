"""kam: the substrate CLI. Subcommands per PRD v1.1 §6.2."""

from __future__ import annotations

import argparse
import secrets
import string
import sys
from datetime import UTC, datetime
from pathlib import Path

from . import doctor as doctor_mod
from . import jobs as jobs_mod
from . import overnight as overnight_mod
from .config import ANCHORS_DIR, BOOTSTRAP_ENV, load_settings
from .db import DB, DBUnavailable
from .run import RunRequest, approve, execute, heartbeat, record_external


def _db(settings) -> DB:
    try:
        return DB(settings)
    except DBUnavailable as e:
        print(f"refused: {e}", file=sys.stderr)
        sys.exit(4)


def cmd_run(a: argparse.Namespace) -> int:
    settings = load_settings()
    req = RunRequest(mission=a.mission, agent=a.agent, task_class=a.task_class, prompt=a.prompt, surface=a.surface,
                     gate=a.gate, parent_run=a.parent, model=a.model, dry_run=a.dry_run,
                     fields_used=set(a.fields_used.split(",")) if a.fields_used else set(),
                     confidentiality=a.confidentiality, subject=a.subject or "", timeout=a.timeout)
    out = execute(req, settings)
    tag = {0: "receipted", 3: "staged", 4: "refused", 5: "failed"}.get(out.exit_code, "?")
    print(f"[{tag}] run_id={out.run_id} state={out.state} :: {out.message}", file=sys.stderr)
    if out.result_text and not a.quiet:
        print(out.result_text)
    return out.exit_code


def cmd_log(a: argparse.Namespace) -> int:
    settings = load_settings()
    rid = record_external(settings, mission=a.mission, agent=a.agent, surface=a.surface, state=a.state, summary=a.summary,
                          target_ref=a.target_ref, task_class=a.task_class, parent_run=a.parent, cost_usd=a.cost)
    print(rid)
    return 0


def cmd_approve(a: argparse.Namespace) -> int:
    settings = load_settings()
    h = approve(settings, a.run_id, a.object_id)
    print(f"receipted {a.run_id} hash {h[:16]}…")
    return 0


def cmd_flag(a: argparse.Namespace, paused: bool) -> int:
    settings = load_settings()
    db = _db(settings)
    name = a.agent or "global"
    db.set_flag(name, paused, a.by or "cli")
    print(f"{'paused' if paused else 'resumed'} {name}")
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    settings = load_settings()
    db = _db(settings)
    v = db.verify()
    print(f"ok={v['ok']} checked={v['checked']} head={v['head_hash']} reason={v['reason']}"
          + (f" first_bad_chain_seq={v['first_bad_chain_seq']}" if v.get("first_bad_chain_seq") else ""))
    if a.anchor and v["ok"]:
        head = db.chain_head()
        now = datetime.now(UTC)
        db.write_anchor(now, head["head_hash"], int(head["event_count"]))
        ANCHORS_DIR.mkdir(parents=True, exist_ok=True)
        p = ANCHORS_DIR / f"{now:%Y-%m-%d}.txt"
        p.write_text(f"{now.isoformat()} head={head['head_hash']} events={head['event_count']}\n")
        print(f"anchor written {p}")
    return 0 if v["ok"] else 2


def cmd_doctor(a: argparse.Namespace) -> int:
    settings = load_settings()
    checks = doctor_mod.run_checks(settings, check_db=not a.no_db)
    print(doctor_mod.format_report(checks))
    return doctor_mod.exit_code(checks)


def cmd_heartbeat(a: argparse.Namespace) -> int:
    settings = load_settings()
    if a.check:
        db = _db(settings)
        jobs = jobs_mod.load_jobs()
        db.sync_jobs([{"job_id": j.job_id, "host": j.host, "cadence": j.cadence, "grace_minutes": j.grace_minutes,
                       "expected_artifact": j.expected_artifact} for j in jobs])
        hb = db.latest_heartbeats()
        rows = jobs_mod.health(jobs, hb, first_seen=db.job_first_seen())
        last_failed = db.latest_failed_by_job()
        by_id = {j.job_id: j for j in jobs}
        for r in rows:
            tag = "MISSING" if r["stale"] else ("not-due" if r["not_due"] else "ok")
            print(f"{tag:7} {r['job_id']} last={r['last']}")
        for r in rows:
            if r["stale"] and jobs_mod.missed_event_due(by_id[r["job_id"]], last_failed.get(r["job_id"])):
                # at most one 'missed' event per job per hour; the Overnight health line is the primary signal
                record_external(settings, mission="TEC-agentic-os", agent=f"job:{r['job_id']}", surface="kam", state="failed",
                                summary=f"missed: {r['job_id']} (cadence {r['cadence']})", target_ref=None, host=settings.host)
        return 0
    rid = heartbeat(settings, a.job_id, settings.host, a.note or "")
    print(rid)
    return 0


def cmd_overnight(a: argparse.Namespace) -> int:
    settings = load_settings()
    p = overnight_mod.write(settings, Path(a.out) if a.out else None)
    print(p)
    return 0


def cmd_mirror(a: argparse.Namespace) -> int:
    settings = load_settings()
    from . import mirror as mirror_mod
    try:
        c, u = mirror_mod.sync(settings)
    except RuntimeError as e:
        print(f"mirror skipped: {e}", file=sys.stderr)
        return 4
    print(f"mirrored: created {c}, updated {u}")
    return 0


def cmd_ledger(a: argparse.Namespace) -> int:
    from datetime import timedelta

    from .config import REPORTS_DIR
    settings = load_settings()
    db = _db(settings)
    now = datetime.now(UTC)
    rows = db.spend_by_pool(now - timedelta(days=7))
    lines = [f"# KAM ledger, week ending {now:%Y-%m-%d} (host {settings.host})", ""]
    for r in rows:
        cost = "unmetered by vendor" if r["cost_usd"] is None else f"${float(r['cost_usd']):.4f} (API list-price estimate for subscription pools)"
        lines.append(f"- {r['pool']}: {r['runs']} run(s), tokens in/out {r['tokens_in'] or 0}/{r['tokens_out'] or 0}, {cost}")
    text = "\n".join(lines) + "\n"
    out_dir = Path(a.out) if a.out else (REPORTS_DIR if settings.host == "mac" else Path.home() / "kam" / "reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"ledger-{now:%Y-%m-%d}.md"
    p.write_text(text)
    print(text)
    print(p)
    return 0


def cmd_jobs(a: argparse.Namespace) -> int:
    for j in jobs_mod.load_jobs():
        print(f"{j.job_id:22} {j.host:5} {j.cadence:16} grace {j.grace_minutes}m  {j.description}")
    return 0


def cmd_rotate(a: argparse.Namespace) -> int:
    settings = load_settings()
    db = _db(settings)
    alphabet = string.ascii_letters + string.digits
    new = "".join(secrets.choice(alphabet) for _ in range(32))
    db.rotate_password(new)
    if BOOTSTRAP_ENV.exists() and settings.source == "bootstrap":
        text = BOOTSTRAP_ENV.read_text()
        import re
        text = re.sub(r"(KAM_DB_DSN=postgresql://[^:]+:)[A-Za-z0-9]+(@)", r"\g<1>" + new + r"\2", text)
        BOOTSTRAP_ENV.write_text(text)
        print("rotated kam_writer password and updated the bootstrap file (move it into 1Password)")
    else:
        print("rotated kam_writer password; update the 1Password item KAM_DB_DSN now (old DSN is dead)")
    return 0


def main(argv: list[str] | None = None) -> int:
    import os
    if os.environ.get("KAM_TRACE_AFTER"):  # diagnostics for hung scheduled jobs: dump the stack to stderr after N seconds and exit
        import faulthandler
        faulthandler.dump_traceback_later(int(os.environ["KAM_TRACE_AFTER"]), exit=True)
    ap = argparse.ArgumentParser(prog="kam", description="KAM: HiveFind execution substrate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="dispatch a job to a surface, with gate and fence checks")
    r.add_argument("--mission", required=True); r.add_argument("--agent", required=True); r.add_argument("--task-class", required=True)
    r.add_argument("--surface"); r.add_argument("--gate"); r.add_argument("--parent"); r.add_argument("--model")
    r.add_argument("--subject", default=""); r.add_argument("--fields-used", help="comma list of Cadence fields the prompt was built from")
    r.add_argument("--confidentiality"); r.add_argument("--timeout", type=int); r.add_argument("--dry-run", action="store_true")
    r.add_argument("--quiet", action="store_true"); r.add_argument("prompt")
    r.set_defaults(fn=cmd_run)

    lg = sub.add_parser("log", help="record a run that happened on a surface kam cannot drive")
    lg.add_argument("--mission", required=True); lg.add_argument("--agent", required=True); lg.add_argument("--surface", required=True)
    lg.add_argument("--state", default="receipted"); lg.add_argument("--target-ref"); lg.add_argument("--task-class", default="glue")
    lg.add_argument("--parent"); lg.add_argument("--cost", type=float); lg.add_argument("summary")
    lg.set_defaults(fn=cmd_log)

    apv = sub.add_parser("approve", help="attest a staged run was approved and executed in the host tool")
    apv.add_argument("run_id"); apv.add_argument("--object-id"); apv.set_defaults(fn=cmd_approve)

    pz = sub.add_parser("pause"); pz.add_argument("--agent"); pz.add_argument("--by"); pz.set_defaults(fn=lambda a: cmd_flag(a, True))
    rs = sub.add_parser("resume"); rs.add_argument("--agent"); rs.add_argument("--by"); rs.set_defaults(fn=lambda a: cmd_flag(a, False))

    v = sub.add_parser("verify"); v.add_argument("--anchor", action="store_true", help="also write today's anchor (DB + kam/anchors)"); v.set_defaults(fn=cmd_verify)
    d = sub.add_parser("doctor"); d.add_argument("--no-db", action="store_true"); d.set_defaults(fn=cmd_doctor)
    hb = sub.add_parser("heartbeat"); hb.add_argument("job_id", nargs="?"); hb.add_argument("--check", action="store_true"); hb.add_argument("--note"); hb.set_defaults(fn=cmd_heartbeat)
    ov = sub.add_parser("overnight"); ov.add_argument("--out"); ov.set_defaults(fn=cmd_overnight)
    mi = sub.add_parser("mirror"); mi.set_defaults(fn=cmd_mirror)
    jb = sub.add_parser("jobs"); jb.set_defaults(fn=cmd_jobs)
    le = sub.add_parser("ledger"); le.add_argument("--out"); le.set_defaults(fn=cmd_ledger)
    ro = sub.add_parser("rotate-db-password"); ro.set_defaults(fn=cmd_rotate)

    a = ap.parse_args(argv)
    if a.cmd == "heartbeat" and not a.check and not a.job_id:
        ap.error("heartbeat needs a job_id or --check")
    return int(a.fn(a))


if __name__ == "__main__":
    sys.exit(main())
