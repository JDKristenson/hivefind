"""Database access. Every write goes through kam.log() in Postgres; this module never assembles hashes itself."""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

import psycopg
from psycopg.rows import dict_row

from .config import Settings


class DBUnavailable(RuntimeError):
    pass


@dataclass
class LogResult:
    seq: int
    chain_seq: int
    row_hash: str
    inserted: bool


class DB:
    def __init__(self, settings: Settings) -> None:
        if not settings.db_dsn:
            raise DBUnavailable("KAM_DB_DSN is not set; run `kam doctor`")
        self._dsn = settings.db_dsn

    @contextmanager
    def conn(self) -> Iterator[psycopg.Connection]:
        try:
            with psycopg.connect(self._dsn, connect_timeout=15, row_factory=dict_row) as c:
                yield c
        except psycopg.OperationalError as e:  # pragma: no cover - network
            raise DBUnavailable(str(e)) from e

    # --- flags (kill switch; fail closed is the caller's job: any exception == paused) ---
    def is_paused(self, agent: str | None = None) -> bool:
        with self.conn() as c:
            rows = c.execute("select name, paused from kam.flags where name = 'global' or name = %s", (agent or "",)).fetchall()
        return any(r["paused"] for r in rows)

    def set_flag(self, name: str, paused: bool, by: str) -> None:
        with self.conn() as c:
            c.execute("select kam.set_flag(%s, %s, %s)", (name, paused, by))
            c.commit()

    # --- the one writer ---
    def log(
        self, run_id: str, state: str, *, summary: str | None = None, target_ref: str | None = None,
        tokens_in: int | None = None, tokens_out: int | None = None, cost_usd: Decimal | float | None = None,
        run: dict[str, Any] | None = None, seq: int | None = None, at: datetime | None = None,
    ) -> LogResult:
        with self.conn() as c:
            row = c.execute(
                "select * from kam.log(%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)",
                (run_id, state, summary, target_ref, tokens_in, tokens_out,
                 None if cost_usd is None else Decimal(str(cost_usd)),
                 json.dumps(run) if run else None, seq, at),
            ).fetchone()
            c.commit()
        assert row is not None
        return LogResult(int(row["seq"]), int(row["chain_seq"]), row["row_hash"], bool(row["inserted"]))

    # --- reads ---
    def verify(self) -> dict[str, Any]:
        with self.conn() as c:
            row = c.execute("select * from kam.verify()").fetchone()
        assert row is not None
        return dict(row)

    def events(self, since: datetime | None = None) -> list[dict[str, Any]]:
        with self.conn() as c:
            if since:
                return c.execute("select * from kam.run_events where at >= %s order by chain_seq", (since,)).fetchall()
            return c.execute("select * from kam.run_events order by chain_seq").fetchall()

    def chain_head(self) -> dict[str, Any]:
        with self.conn() as c:
            row = c.execute("select head_hash, event_count, updated_at from kam.chain_head where id = 1").fetchone()
        assert row is not None
        return dict(row)

    def write_anchor(self, day: datetime, head_hash: str, event_count: int) -> None:
        with self.conn() as c:
            c.execute(
                "insert into kam.anchors(day, head_hash, event_count) values (%s, %s, %s) "
                "on conflict (day) do update set head_hash = excluded.head_hash, event_count = excluded.event_count, written_at = now()",
                (day.date(), head_hash, event_count),
            )
            c.commit()

    def latest_anchor(self) -> dict[str, Any] | None:
        with self.conn() as c:
            return c.execute("select * from kam.anchors order by day desc limit 1").fetchone()

    def runs_with_latest(self, since: datetime | None = None) -> list[dict[str, Any]]:
        """Runs joined to their latest event, newest first."""
        since = since or datetime.now(UTC) - timedelta(days=1)
        sql = """
        with latest as (
          select distinct on (run_id) run_id, seq, state, at, target_ref, tokens_in, tokens_out, cost_usd, summary
          from kam.run_events order by run_id, seq desc)
        select r.*, l.seq as last_seq, l.state, l.at as last_at, l.target_ref, l.tokens_in, l.tokens_out, l.cost_usd, l.summary
        from kam.runs r join latest l using (run_id)
        where r.created_at >= %s or l.at >= %s
        order by l.at desc
        """
        with self.conn() as c:
            return c.execute(sql, (since, since)).fetchall()

    def spend_by_pool(self, since: datetime) -> list[dict[str, Any]]:
        sql = """
        select r.pool, count(distinct r.run_id) as runs,
               sum(e.cost_usd) as cost_usd, sum(e.tokens_in) as tokens_in, sum(e.tokens_out) as tokens_out,
               count(*) filter (where e.cost_usd is null and e.state in ('receipted','executed')) as unmetered_events
        from kam.run_events e join kam.runs r using (run_id)
        where e.at >= %s group by r.pool order by r.pool
        """
        with self.conn() as c:
            return c.execute(sql, (since,)).fetchall()

    def job_first_seen(self) -> dict[str, datetime]:
        with self.conn() as c:
            rows = c.execute("select job_id, first_seen from kam.jobs").fetchall()
        return {r["job_id"]: r["first_seen"] for r in rows}

    def latest_failed_by_job(self) -> dict[str, datetime]:
        sql = """
        select r.agent, max(e.at) as at from kam.run_events e join kam.runs r using (run_id)
        where e.state = 'failed' and r.agent like 'job:%%' and e.summary like 'missed:%%' group by r.agent
        """
        with self.conn() as c:
            rows = c.execute(sql).fetchall()
        return {r["agent"].removeprefix("job:"): r["at"] for r in rows}

    def latest_heartbeats(self) -> dict[str, datetime]:
        sql = """
        select r.agent, max(e.at) as at from kam.run_events e join kam.runs r using (run_id)
        where e.state = 'heartbeat' and r.agent like 'job:%%' group by r.agent
        """
        with self.conn() as c:
            rows = c.execute(sql).fetchall()
        return {r["agent"].removeprefix("job:"): r["at"] for r in rows}

    def unmirrored_runs(self) -> list[dict[str, Any]]:
        sql = """
        with latest as (
          select distinct on (run_id) run_id, seq, state, at, target_ref, summary, cost_usd
          from kam.run_events order by run_id, seq desc)
        select r.*, l.state, l.at as last_at, l.target_ref, l.summary, l.cost_usd
        from kam.runs r join latest l using (run_id)
        where r.mirrored_at is null or l.at > r.mirrored_at
        order by l.at limit 200
        """
        with self.conn() as c:
            return c.execute(sql).fetchall()

    def mark_mirrored(self, run_id: str, notion_page_id: str) -> None:
        with self.conn() as c:
            c.execute("update kam.runs set mirrored_at = now(), notion_page_id = %s where run_id = %s", (notion_page_id, run_id))
            c.commit()

    def sync_jobs(self, jobs: list[dict[str, Any]]) -> None:
        with self.conn() as c:
            for j in jobs:
                c.execute(
                    "insert into kam.jobs(job_id, host, cadence, grace_minutes, expected_artifact) values (%s,%s,%s,%s,%s) "
                    "on conflict (job_id) do update set host=excluded.host, cadence=excluded.cadence, "
                    "grace_minutes=excluded.grace_minutes, expected_artifact=excluded.expected_artifact, updated_at=now()",
                    (j["job_id"], j["host"], j["cadence"], int(j.get("grace_minutes", 30)), j.get("expected_artifact")),
                )
            c.commit()

    def rotate_password(self, new_password: str) -> None:
        """A role may change its own password; no admin credential and no chat transit needed."""
        with self.conn() as c:
            c.execute(psycopg.sql.SQL("alter role kam_writer with password {}").format(psycopg.sql.Literal(new_password)))
            c.commit()
