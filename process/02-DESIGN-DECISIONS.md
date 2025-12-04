# Design Decisions

Key architectural choices and the reasoning behind them.

---

## Decision 1: Agents as Roles, Not Automations

**Choice:** Design each agent as a complete job role with identity, personality, decision authority, and success metrics; not as a set of automations.

**Alternatives considered:**
- Workflow-first approach (build automations, group them later)
- Feature-based design (one agent per feature)
- Tool-based design (one agent per integration)

**Why this approach:**
- Forces clarity about *what* before *how*
- Makes handoffs and boundaries explicit
- Personality and voice create consistency
- Success metrics make agents accountable
- Job description format is intuitive for explaining to others

**Tradeoff:** More upfront work. Each spec takes 2-4 hours vs. just building an automation.

**Verdict:** Worth it. The spec-writing forces thinking that prevents expensive rework later.

---

## Decision 2: Named Personas with Historical Anchors

**Choice:** Every agent has a human name tied to a historical figure whose attributes match the role.

**Alternatives considered:**
- Functional names (FinanceBot, EmailAgent)
- Abstract names (Agent-1, Agent-2)
- No names (just job titles)

**Why this approach:**
- Memorable and intuitive (Warren = finance is obvious)
- Personality anchor for voice consistency
- Makes the system explainable ("Warren handles my finances, like his namesake")
- More engaging than functional names
- Demonstrates thoughtfulness to clients

**Tradeoff:** Takes time to find good matches. Some are stretches.

**Verdict:** High value. Names are one of the most commented-on aspects when demoing.

---

## Decision 3: Three-Layer Coordination

**Choice:** Separate coordination into three distinct roles: Xavier (operations), Aurelius (values/accountability), Clare (communications).

**Alternatives considered:**
- Single coordinator agent
- No coordinator (agents self-organize)
- Human serves as coordinator

**Why this approach:**
- Separation of concerns (ops vs. values vs. comms are different functions)
- Prevents any single agent from becoming bloated
- Clear escalation paths based on issue type
- Mirrors real executive structure (COO, ethics officer, comms director)

**Tradeoff:** More agents to build and maintain. More complex routing logic.

**Verdict:** Essential at scale. With 15+ domain agents, coordination can't be ad hoc.

---

## Decision 4: Supervisor Relationships

**Choice:** Some agents report to other agents, not directly to the human. Warren oversees Hetty (tax). Franklin oversees Clara (customer service).

**Alternatives considered:**
- Flat structure (all agents report to human)
- Full hierarchy (multiple layers)
- Domain-based grouping only (no direct reporting)

**Why this approach:**
- Reduces human bottleneck (Hetty doesn't need to escalate every tax question)
- Creates clear domain ownership (Warren owns all finance, including tax)
- Mirrors how organizations actually work
- Scales better as agents multiply

**Tradeoff:** Requires building agents in order (supervisors before reports). More complex information flows.

**Verdict:** Necessary for any domain with subspecialties (finance/tax, store ops/customer service).

---

## Decision 5: Trigger → Action → Output Format

**Choice:** Every responsibility defined as: WHEN [trigger] → WHAT [action] → WHERE [output destination].

**Alternatives considered:**
- Narrative descriptions ("handles email triage")
- Feature lists ("can classify emails")
- Use-case format ("As a user, I want...")

**Why this approach:**
- Directly translatable to automation logic
- Forces specificity (what exactly triggers this? where does output go?)
- Makes gaps obvious (if you can't specify the trigger, you can't automate it)
- Consistent format across all agents

**Tradeoff:** More rigid. Some responsibilities don't fit neatly.

**Verdict:** Essential. This format is what makes specs actionable vs. aspirational.

---

## Decision 6: Explicit Decision Authority

**Choice:** Every spec defines three categories: autonomous actions (no approval needed), escalate to human, and hard boundaries (never do).

**Alternatives considered:**
- Default to human approval for everything
- Default to autonomous with exception list
- Case-by-case judgment

**Why this approach:**
- Forces thinking about trust boundaries upfront
- Prevents scope creep and dangerous autonomy
- Makes agent behavior predictable
- Documents the "rules of engagement" for debugging

**Tradeoff:** Requires careful thought. Under-trusting creates bottlenecks; over-trusting creates risks.

**Verdict:** Critical. This section gets the most revision during spec development.

---

## Decision 7: Domain Clustering

**Choice:** Group agents by shared context: Personal (9), Haze Gray (4), Puzzlehouse (3), plus Coordination (3).

**Alternatives considered:**
- Function-based (all comms together, all finance together)
- Flat list (no grouping)
- Client-facing vs. internal

**Why this approach:**
- Agents in same domain share data (Puzzlehouse agents share Shopify access)
- Reduces cross-domain dependencies
- Maps to how the principal (JD) thinks about life/work domains
- Clear boundaries for what data each agent cluster accesses

**Tradeoff:** Some functions span domains (Clare does communications for all). Requires careful boundary management.

**Verdict:** Right balance. Domain context matters more than functional similarity.

---

## Decision 8: Notion as Central Hub

**Choice:** Use Notion as the central repository for all agent data, logs, and dashboards.

**Alternatives considered:**
- Purpose-built database (Airtable, custom)
- Multiple tools per domain
- File-based system

**Why this approach:**
- Already using Notion; no new tool to learn
- Flexible schema (can adapt as agents evolve)
- Human-readable (can browse logs manually)
- Good API for integrations
- Relational databases for connected data

**Tradeoff:** Not optimized for high-volume logging. May need to supplement later.

**Verdict:** Right for current scale. Reassess if logging volume becomes an issue.

---

## Decision 9: n8n for Orchestration

**Choice:** Use n8n (self-hosted) as the primary workflow automation platform.

**Alternatives considered:**
- Zapier (easier but less flexible)
- Make.com (similar to n8n)
- Custom code (maximum flexibility)
- Relay.app (more AI-native)

**Why this approach:**
- Self-hosted = no per-workflow pricing at scale
- Visual workflow builder for iteration
- Good community and documentation
- Can run custom code when needed
- Open source; no vendor lock-in

**Tradeoff:** More setup than SaaS options. Self-hosting requires maintenance.

**Verdict:** Best balance of flexibility, cost, and capability for this use case.

---

## Decision 10: Spec Before Build

**Choice:** Complete all agent specs before building any automations.

**Alternatives considered:**
- Build as you go (spec one, build one, repeat)
- Prototype first, spec later
- Minimal spec, iterate based on usage

**Why this approach:**
- Reveals cross-agent dependencies early
- Prevents building something that doesn't fit the architecture
- Specs are cheaper to revise than workflows
- Creates complete documentation from day one
- Forces system-level thinking

**Tradeoff:** Longer time to first working automation. Possible over-engineering.

**Verdict:** Worth it for a system this interconnected. For simpler projects, build-as-you-go might be fine.

---

## Decisions I'd Reconsider

### Maybe: More Aggressive Automation

Some specs include tasks that could be fully autonomous but are flagged for human review. After building and observing, might push more toward autonomous operation.

### Maybe: Simpler Coordination

Three coordination agents might be overkill. Could potentially combine Xavier and Clare, with Aurelius as the only separate coordinator.

### Maybe: Start Smaller

18 agents is ambitious. Could have started with 5-6 core agents and expanded. But the design phase was valuable regardless of build sequence.

---

*These decisions emerged from iteration, not upfront planning. The first architecture sketch looked very different.*
