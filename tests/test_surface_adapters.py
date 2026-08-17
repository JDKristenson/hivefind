"""Surface adapters parse usage from fixtures. Fixtures come from real canaries (Phase 0) and are replayed offline."""

import json
from pathlib import Path

import pytest

from kam.jobs import Job, expected_interval, health, is_stale
from kam.mirror import build_properties, status_for
from kam.surfaces import claude_p, codex, openrouter

FIX = Path(__file__).parent / "fixtures"


def _load(name: str):
    p = FIX / name
    if not p.exists():
        pytest.skip(f"fixture {name} not captured yet (run the Phase 0 canary)")
    return p.read_text()


def test_claude_p_parses_json_result_shape():
    sample = json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "OK", "session_id": "abc",
                         "total_cost_usd": 0.0123, "usage": {"input_tokens": 10, "output_tokens": 2, "cache_read_input_tokens": 5}})
    r = claude_p.parse_json_result(sample)
    assert r.ok and r.text == "OK" and r.tokens_in == 15 and r.tokens_out == 2 and r.cost_usd == 0.0123
    assert r.target_ref == "claude-session:abc"


def test_claude_p_fixture():
    r = claude_p.parse_json_result(_load("claude-p.json"))
    assert r.ok and "OK" in r.text.upper() and r.tokens_out is not None


def test_codex_parses_jsonl_usage():
    lines = [
        json.dumps({"type": "thread.started", "thread_id": "t1"}),
        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "OK"}}),
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 100, "cached_input_tokens": 20, "output_tokens": 3}}),
    ]
    r = codex.parse_jsonl("\n".join(lines))
    assert r.ok and r.text == "OK" and r.tokens_in == 120 and r.tokens_out == 3 and r.cost_usd is None


def test_codex_fixture():
    r = codex.parse_jsonl(_load("codex-exec.jsonl"))
    assert r.ok and "OK" in r.text.upper()


def test_openrouter_parses_usage_and_cost():
    obj = {"id": "gen-1", "model": "anthropic/claude-haiku-4.5",
           "choices": [{"message": {"role": "assistant", "content": "OK"}}],
           "usage": {"prompt_tokens": 30, "completion_tokens": 1, "cost": 0.000045}}
    r = openrouter.parse_response(obj)
    assert r.ok and r.text == "OK" and r.tokens_in == 30 and r.tokens_out == 1 and r.cost_usd == 0.000045
    assert r.target_ref == "openrouter:gen-1"


def test_openrouter_fixture():
    r = openrouter.parse_response(json.loads(_load("openrouter.json")))
    assert r.ok and "OK" in r.text.upper() and r.tokens_in


def test_status_mapping_matches_prd_7_4():
    assert status_for("intended", None) == "Running"
    assert status_for("staged_for_approval", "external_send") == "Drafted"
    assert status_for("receipted", "external_send") == "Published"
    assert status_for("receipted", None) == "Reviewed"
    assert status_for("failed", None) == "Failed"
    assert status_for("cancelled", None) == "Cancelled"
    assert status_for("heartbeat", None) is None


def test_build_properties_only_uses_known_schema():
    schema = {"Run": {"type": "title"}, "Status": {"type": "status"}, "KAM run id": {"type": "rich_text"}, "Surface": {"type": "select"}}
    from datetime import UTC, datetime
    run = {"run_id": "0199-abcdefgh", "agent": "jd", "task_class": "classify", "state": "receipted", "gate": None,
           "surface": "openrouter", "summary": "OK", "created_at": datetime(2026, 8, 17, tzinfo=UTC)}
    props = build_properties(schema, run)
    assert set(props) == {"Run", "Status", "KAM run id", "Surface"}
    assert props["Status"] == {"status": {"name": "Reviewed"}}


def test_jobs_staleness():
    from datetime import UTC, datetime, timedelta
    j = Job(job_id="x", host="ec2", cadence="every 5m", grace_minutes=10)
    now = datetime(2026, 8, 17, 12, 0, tzinfo=UTC)
    assert expected_interval("every 5m") == timedelta(minutes=5)
    assert expected_interval("daily 06:15") == timedelta(days=1)
    assert expected_interval("weekly mon 07:30") == timedelta(days=7)
    assert is_stale(j, None, now)
    assert not is_stale(j, now - timedelta(minutes=12), now)
    assert is_stale(j, now - timedelta(minutes=16), now)
    rows = health([j], {}, now)
    assert rows[0]["stale"] is True
