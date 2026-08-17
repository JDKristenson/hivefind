"""The Python canonical form must reproduce the SQL hash byte for byte.
Fixture: chain_seq 1 as written by kam.log() on Supabase 2026-08-17 (kam.canonical_event output and row_hash)."""

from datetime import UTC, datetime
from decimal import Decimal

from kam.log import GENESIS, EventRow, canonical, event_hash, uuid7, verify_chain

SQL_CANON_1 = (
    '{"at":"2026-08-17T22:47:39.911555Z","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000",'
    '"run_id":"019913c0-0000-7000-8000-000000000001","seq":1,"state":"intended","summary":"phase0 chain canary A"}'
)
SQL_HASH_1 = "04e18288e2bb59cea239350c49d9de8d5fe82e00d97392981c7537dc017b6638"
SQL_CANON_2 = (
    '{"at":"2026-08-17T22:47:39.937263Z","cost_usd":"0.0001","prev_hash":"04e18288e2bb59cea239350c49d9de8d5fe82e00d97392981c7537dc017b6638",'
    '"run_id":"019913c0-0000-7000-8000-000000000001","seq":2,"state":"receipted","summary":"phase0 chain canary A",'
    '"target_ref":"sql://canary","tokens_in":12,"tokens_out":3}'
)
SQL_HASH_2 = "7b8290914f3045c272c42f19362a75f339fef86856fb05d1217441d15701330b"


def _row1() -> EventRow:
    return EventRow(run_id="019913c0-0000-7000-8000-000000000001", seq=1, state="intended",
                    at=datetime(2026, 8, 17, 22, 47, 39, 911555, tzinfo=UTC), prev_hash=GENESIS, summary="phase0 chain canary A")


def _row2() -> EventRow:
    return EventRow(run_id="019913c0-0000-7000-8000-000000000001", seq=2, state="receipted",
                    at=datetime(2026, 8, 17, 22, 47, 39, 937263, tzinfo=UTC), prev_hash=SQL_HASH_1,
                    target_ref="sql://canary", tokens_in=12, tokens_out=3, cost_usd=Decimal("0.0001"), summary="phase0 chain canary A")


def test_canonical_matches_sql_byte_for_byte():
    assert canonical(_row1()) == SQL_CANON_1
    assert canonical(_row2()) == SQL_CANON_2


def test_hash_matches_sql():
    assert event_hash(_row1()) == SQL_HASH_1
    assert event_hash(_row2()) == SQL_HASH_2


def test_verify_chain_detects_tamper():
    rows = [
        {"chain_seq": 1, "run_id": _row1().run_id, "seq": 1, "state": "intended", "at": _row1().at, "prev_hash": GENESIS,
         "summary": "phase0 chain canary A", "row_hash": SQL_HASH_1},
        {"chain_seq": 2, "run_id": _row2().run_id, "seq": 2, "state": "receipted", "at": _row2().at, "prev_hash": SQL_HASH_1,
         "target_ref": "sql://canary", "tokens_in": 12, "tokens_out": 3, "cost_usd": Decimal("0.0001"),
         "summary": "phase0 chain canary A", "row_hash": SQL_HASH_2},
    ]
    ok, n, head, bad, reason = verify_chain(rows)
    assert ok and n == 2 and head == SQL_HASH_2 and bad is None
    tampered = [dict(rows[0]), dict(rows[1])]
    tampered[1]["summary"] = "TAMPERED"
    ok, n, head, bad, reason = verify_chain(tampered)
    assert not ok and bad == 2 and "row_hash mismatch" in reason


def test_cost_formatting_is_fixed_four_decimals():
    e = EventRow(run_id="r", seq=1, state="receipted", at=datetime(2026, 1, 1, tzinfo=UTC), prev_hash=GENESIS, cost_usd=1.5)
    assert '"cost_usd":"1.5000"' in canonical(e)


def test_uuid7_is_time_ordered_and_versioned():
    a, b = uuid7(), uuid7()
    assert a[14] == "7" and b[14] == "7"
    assert a < b or a[:13] == b[:13]
