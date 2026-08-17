"""Hash-chain primitives that mirror the SQL in kam.canonical_event / kam.event_hash exactly.

Canonical form (PRD v1.1 §6.1): keys sorted, no whitespace, JSON string escaping, integers bare,
`at` as UTC RFC 3339 with microseconds and Z, `cost_usd` as a fixed four-decimal string, NULLs omitted.
The SQL side is the writer of record; this module exists so `kam verify` can recompute the chain
client-side and so tests can prove both implementations agree byte for byte.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

GENESIS = "0" * 64
STATES = (
    "intended", "executing", "staged_for_approval", "approved", "executed",
    "receipted", "failed", "cancelled", "heartbeat",
)


def uuid7() -> str:
    """UUIDv7 (time-ordered) generated in Python; Postgres 17 has no native uuidv7()."""
    ms = int(time.time() * 1000)
    rand = os.urandom(10)
    b = ms.to_bytes(6, "big") + rand
    ba = bytearray(b)
    ba[6] = (ba[6] & 0x0F) | 0x70  # version 7
    ba[8] = (ba[8] & 0x3F) | 0x80  # variant
    return str(uuid.UUID(bytes=bytes(ba)))


def fmt_at(at: datetime) -> str:
    if at.tzinfo is None:
        raise ValueError("at must be timezone-aware")
    return at.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def fmt_cost(cost: Decimal | float | str | None) -> str | None:
    if cost is None:
        return None
    return f"{Decimal(str(cost)):.4f}"


@dataclass(frozen=True)
class EventRow:
    run_id: str
    seq: int
    state: str
    at: datetime
    prev_hash: str
    target_ref: str | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: Decimal | float | str | None = None
    summary: str | None = None


def canonical(e: EventRow) -> str:
    obj: dict[str, object] = {
        "at": fmt_at(e.at),
        "prev_hash": e.prev_hash,
        "run_id": e.run_id,
        "seq": int(e.seq),
        "state": e.state,
    }
    if e.cost_usd is not None:
        obj["cost_usd"] = fmt_cost(e.cost_usd)
    if e.summary is not None:
        obj["summary"] = e.summary
    if e.target_ref is not None:
        obj["target_ref"] = e.target_ref
    if e.tokens_in is not None:
        obj["tokens_in"] = int(e.tokens_in)
    if e.tokens_out is not None:
        obj["tokens_out"] = int(e.tokens_out)
    # sort_keys + compact separators + ensure_ascii=False == Postgres to_json escaping for these types
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def event_hash(e: EventRow) -> str:
    return hashlib.sha256(canonical(e).encode("utf-8")).hexdigest()


def verify_chain(rows: list[dict]) -> tuple[bool, int, str, int | None, str]:
    """rows ordered by chain_seq. Returns (ok, checked, head_hash, first_bad_chain_seq, reason)."""
    prev = GENESIS
    n = 0
    for r in rows:
        n += 1
        if int(r["chain_seq"]) != n:
            return False, n, prev, int(r["chain_seq"]), "chain_seq gap"
        if r["prev_hash"] != prev:
            return False, n, prev, int(r["chain_seq"]), "prev_hash mismatch"
        e = EventRow(
            run_id=r["run_id"], seq=int(r["seq"]), state=r["state"], at=r["at"], prev_hash=r["prev_hash"],
            target_ref=r.get("target_ref"), tokens_in=r.get("tokens_in"), tokens_out=r.get("tokens_out"),
            cost_usd=r.get("cost_usd"), summary=r.get("summary"),
        )
        calc = event_hash(e)
        if calc != r["row_hash"]:
            return False, n, prev, int(r["chain_seq"]), "row_hash mismatch (row altered)"
        prev = r["row_hash"]
    return True, n, prev, None, "ok"
