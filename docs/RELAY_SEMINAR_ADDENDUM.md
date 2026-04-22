# Relay.app Seminar Addendum

**Source**: Rundown seminar on Relay.app, 2026-04-22
**Purpose**: Fold two seminar frameworks into the Hivefind build plan so Phase 4+ automations pick the right pattern and the right tool the first time.
**Scope**: Complements `BUILD_PLAN.md`. Does not replace any existing phase.

---

## Framework 1: Growth Operator Agent Matrix

Five agent roles across any work domain. Every Hivefind agent task decomposes into one or more of these.

| Role | What it does | Hivefind analog |
|------|--------------|-----------------|
| Monitor | Watches a signal, fires on a threshold | Activity Log triggers, Exception Queue creation |
| Researcher | Gathers and enriches data | Iris, Evelyn (Memory) query side, Helena account research |
| Generator | Produces a draft or artifact | Dale, Cicero, Clare, Evelyn (EA) composer |
| Optimizer | Analyzes patterns and recommends | Warren projections, Aurelius values check, Galen correlations |
| Orchestrator | Routes work and stitches tools | Xavier (primary), Hamilton cross-function, cross-platform pipelines |

### Domain coverage check

The seminar matrix covers seven domains. Hivefind's current 19-agent roster covers all seven, with gaps only in depth, not breadth.

| Seminar domain | Hivefind coverage | Gap |
|----------------|-------------------|-----|
| Intelligence & Research | Iris, Evelyn (Memory) | No external competitor tracker for Haze Gray |
| Social Media & Community | Ada (Puzzlehouse only) | No personal brand social monitor for JD |
| Organic Content & SEO | Dale | SEO-specific signal tracking absent |
| Lead Operations | Helena | Enrichment + scoring not yet wired |
| Sales Enablement | Cicero, Hamilton | Win/loss pattern analysis not built |
| Performance Analysis | Warren (finance), Franklin (store) | No unified marketing ROAS view |
| Operations & Coordination | Xavier, Aurelius | Full coverage |

**Action**: Treat the four gaps above as candidate agent additions or sub-capabilities. File under "future agents" in `AGENT_ROSTER.md`. Do not expand the roster now; finish Phase 1-3 first.

---

## Framework 2: Three Common AI Agent Patterns

Every Relay.app workflow and every Hivefind automation maps to one of three shapes.

### Recurring

Scheduled cadence. Find, synthesize, send.

**Examples in Hivefind**:
- Clare's Daily Briefing (8 PM ET digest)
- Aurelius weekly values-conflict scan
- Warren monthly P&L summary
- Dale weekly content calendar review

**Tool fit**: n8n cron triggers are fine. Relay.app wins when the send step needs human approval before it goes out (newsletter drafts, financial reports to JD).

### Preparation

Event-triggered lookup and brief.

**Examples in Hivefind**:
- Evelyn (EA) pre-meeting prep (calendar event upcoming, pull attendee history, summarize, deliver brief)
- Helena pre-call research (meeting booked, enrich account, draft talking points)
- Marco pre-trip itinerary compile (flight booked, pull logistics, produce single-page brief)
- Cicero proposal prep (opportunity advances to proposal stage, pull prior wins, draft outline)

**Tool fit**: **This is Relay.app's strongest pattern.** Calendar-triggered workflows with AI steps and a human approval gate before delivery. Default all four above to Relay.app, not n8n.

### Data Transfer

Event occurs, AI processes, write to another system.

**Examples in Hivefind**:
- EmailToNotion v3 (email arrives, classify, write to Inbox DB) - already in n8n, keep
- Hetty expense categorization (transaction lands, categorize, write to Financial Transactions)
- Clara ticket routing (Shopify ticket, triage, route to Franklin or autorespond)
- Iris document ingestion (file dropped in vault, tag, file, index)

**Tool fit**: n8n is the right home. These are silent, high-frequency, no human review. Relay.app's human-in-the-loop is overhead here.

---

## Decision rules added to the build plan

**Rule 1 - Pattern before tool.** Before building any new automation past Phase 3, classify it as Recurring, Preparation, or Data Transfer. Write the pattern name in the workflow comment header.

**Rule 2 - Relay.app owns Preparation.** Calendar-triggered prep workflows with a human approval step go to Relay.app. This is a new entry in the Technology Stack table in `README.md`.

**Rule 3 - n8n owns Data Transfer.** High-frequency silent workflows stay in n8n. Do not migrate working n8n Data Transfer flows to Relay.app.

**Rule 4 - Recurring splits by approval gate.** If the output goes straight to JD without review, n8n. If it needs human review before send, Relay.app.

**Rule 5 - Every agent spec gets a role tag.** Add a line to the spec template: `Primary Roles: [Monitor, Researcher, Generator, Optimizer, Orchestrator]`. This forces the spec author to name what the agent actually does in operator terms.

---

## Phase-by-phase impact

| Phase | Change |
|-------|--------|
| 0 | No change. Notion foundation stays. |
| 1 (Coordination) | Xavier gets explicit `Orchestrator` role tag; Clare gets `Generator + Optimizer`; Aurelius gets `Monitor + Optimizer`. |
| 2 (Knowledge + memory) | Iris and Evelyn (Memory) tagged `Researcher + Generator`. |
| 3 (Notion-native) | Seneca `Generator`, Hamilton `Monitor + Orchestrator`, Cicero `Generator + Optimizer`. |
| 4 (Google hybrids) | **Evelyn (EA) pre-meeting prep flow and Martha household prep flow move from n8n to Relay.app.** Calendar-triggered Preparation pattern with human approval. |
| 5-8 | Apply Rule 1 at spec time. Default Preparation-pattern agents to Relay.app (Helena pre-call, Marco pre-trip), Data Transfer agents to n8n (Hetty, Clara), Recurring with review to Relay.app. |

---

## What to do this week

1. Add the five role tags to `templates/AGENT_SPEC_TEMPLATE.md`.
2. Add the Pattern line (Recurring / Preparation / Data Transfer) to `templates/AGENT_SPEC_TEMPLATE.md`.
3. Update `README.md` Technology Stack to split orchestration by pattern: Notion AI (primary), n8n (Data Transfer + silent Recurring), Relay.app (Preparation + reviewed Recurring).
4. Log the four gap domains in `AGENT_ROSTER.md` under a new "Future capabilities" section.
5. Do not start a Relay.app account until Phase 4 build begins. Seminar intel only at this point.

---

*Related*: `BUILD_PLAN.md` (phases), `README.md` (stack), `AGENT_ROSTER.md` (roster), `CONVENTIONS.md` (spec format).
