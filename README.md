# HiveFind

JD Kristenson's personal agent fleet (19 personas, Notion-first control plane) and, from Phase 0 (2026-08-17), **KAM**, the execution
substrate: one dispatch verb (`kam run`), one hash-chained run log in Supabase (`kam` schema), one human approval gate, and one identity
kit per agent. Spec: `10 BRIDGE/TEC/TEC agentic-os/3 out/2026-08-17 claude-code - kam-prd-v1.1.md`.

## Layout

| Path | What |
|---|---|
| `kam/` | substrate package + CLI (`kam run`, `log`, `approve`, `pause`/`resume`, `verify --anchor`, `doctor`, `heartbeat --check`, `overnight`, `mirror`, `jobs`, `rotate-db-password`) |
| `kam/registry.yaml` | agent registry, authority in Phases 0-1 (Notion 🤖 Agent Registry from Phase 2) |
| `kam/jobs.yaml` | every scheduled job; the watchdog compares it to heartbeats |
| `kam/.env.op` | 1Password references only, resolved by `op run` |
| `kam/anchors/` | daily chain-head anchors (committed) |
| `docs/`, `notion/`, `specs/`, `org/`, `process/`, `templates/`, `updates/` | pre-existing HiveFind documents |
| `tests/` | offline tests; fixtures replay real canaries so no test spends subscription quota |

## Install

| Host | Command |
|---|---|
| Mac | `uv tool install --editable .` (Python 3.13 via uv) |
| EC2 | `git pull && uv tool install --editable . --python 3.13` under `ec2-user`; timers in `infra/ec2/systemd/` |

Secrets: `op run --env-file kam/.env.op -- kam ...` once 1Password is signed in; until then `~/.config/kam/env.local` (0600) is the
Phase 0 bootstrap and `kam doctor` warns while it exists. Never export `ANTHROPIC_API_KEY` in a shell that runs `claude -p`.

## Exit codes (`kam run`)

| Code | Meaning |
|---|---|
| 0 | receipted |
| 3 | staged for approval (gate) |
| 4 | refused (pause flag, allowlist, mission fence, host, or unreadable kill switch) |
| 5 | surface error (event `failed`) |
