# System Architecture

> Version 3.0 | April 2026

Technical architecture for the Hivefind ecosystem. Notion AI agents are the primary execution layer. n8n and Relay.app fill gaps only where Notion cannot reach an external API natively.

---

## Notion-First Architecture

Notion is not a passive dashboard. Notion AI agents execute work, store state, and surface exceptions. External orchestration (n8n, Relay.app) exists only for API calls Notion cannot make natively.

```
+---------------------------------------------------------------+
|                     NOTION WORKSPACE                          |
|                                                               |
|  +--------------------------+  +---------------------------+  |
|  |    AGENT EXECUTION       |  |    HUMAN INTERFACE        |  |
|  |    (Notion AI Agents)    |  |    (Dashboards, Views)    |  |
|  |                          |  |                           |  |
|  |  Tier 1: Run natively    |  |  Morning briefing         |  |
|  |  Tier 2: Trigger n8n     |  |  Exception queue          |  |
|  |    for API gaps          |  |  Agent status dashboard   |  |
|  |  Tier 3: State + UI      |  |  Strategic decision log   |  |
|  |    only (n8n executes)   |  |  Performance trends       |  |
|  +--------------------------+  +---------------------------+  |
|                  |                                             |
|  +------------------------------------------------------------+
|  |              DATA LAYER (Notion Databases)                 |
|  |                                                            |
|  |  Agent Registry | Activity Log | Exception Queue           |
|  |  Memory Entries | Memory Review Queue | Preferences        |
|  |  Domain DBs (CRM, Inventory, etc.)                         |
|  +------------------------------------------------------------+
|                                                               |
+---------------------------------------------------------------+
         |                              |
         | API gaps only                | API gaps only
         v                              v
+------------------+          +------------------+
|       n8n        |          |    Relay.app     |
|  (Tier 2/3 API   |          |  (macOS-native   |
|   calls, webhooks)|         |   integrations)  |
+------------------+          +------------------+
         |
         v
+------------------+
|  External APIs   |
|  (Shopify, QBO,  |
|   LinkedIn, etc.)|
+------------------+
```

### What Changed from v2.0

| v2.0 (Three-Layer) | v3.0 (Notion-First) |
|---------------------|----------------------|
| n8n = universal orchestration | n8n = gap-filler for APIs Notion cannot reach |
| Notion = passive dashboard + data store | Notion AI agents = primary executors |
| All agent logic in n8n workflows | Tier 1 agents run entirely in Notion |
| Relay.app bridges Notion to n8n | Relay.app handles macOS-native integrations |

---

## Agent Tier Classification

19 agents across 3 tiers. Tier determines where execution happens.

### Tier 1: Notion-Native

No external API dependencies. Runs entirely as Notion AI agents triggered by schedules, DB property changes, or manual invocation.

| Agent | Role | Trigger Pattern |
|-------|------|-----------------|
| Xavier | Chief of Staff / Router | Schedule (6 AM, 6 PM) + DB property change (new exceptions) |
| Clare | Communications Director | Schedule (6:05 AM, 6 PM) + manual |
| Aurelius | Standards & Compliance | Schedule (weekly) + DB property change (new activity) |
| Iris | Personal Brand Manager | Schedule (weekly) + manual |
| Seneca | Strategic Advisor | Manual + DB property change (strategic decisions logged) |
| Hamilton | Financial Strategist | Schedule (monthly) + manual |
| Cicero | Political Intelligence | Schedule (weekly) + manual |
| Evelyn (Memory Curator) | Memory management, review, decay | Schedule (daily) + DB property change (new memory entries) |

### Tier 2: Hybrid

Notion AI agent handles logic and state. n8n or Relay.app called for specific API operations Notion cannot perform natively.

| Agent | Role | Notion Handles | n8n/Relay Handles |
|-------|------|----------------|-------------------|
| Evelyn (EA) | Email triage, calendar, scheduling | Triage logic, priority assignment, briefing compilation | Google Workspace API (Gmail read/send, Calendar read/write) |
| Eleanor | CRM / Relationship Manager | Contact scoring, relationship mapping, follow-up scheduling | Clay API, enrichment APIs |
| Warren | CFO / Financial Ops | Budget tracking, variance analysis, reporting | QuickBooks OAuth API |
| Hetty | Bookkeeper | Transaction categorization, reconciliation | QuickBooks OAuth API |
| Galen | Health & Wellness | Trend analysis, recommendations, check-in scheduling | Health/biometric APIs |
| Martha | Home & Household | Task scheduling, inventory tracking, vendor management | Home service APIs |
| Marco | Travel & Logistics | Itinerary compilation, preference matching | Travel booking APIs |
| Helena | LinkedIn & Networking | Content drafting, connection strategy, outreach scheduling | LinkedIn API |
| Dale | Sales & BD | Pipeline management, prospect scoring, outreach planning | LinkedIn API, enrichment APIs |

### Tier 3: n8n-Primary

API-heavy workflows where n8n executes most logic. Notion provides state storage, UI, and human review surfaces.

| Agent | Role | n8n Executes | Notion Provides |
|-------|------|-------------|-----------------|
| Ada | Social Media Manager | Multi-platform posting, scheduling, analytics pull | Content calendar, approval queue, performance dashboard |
| Franklin | Inventory & E-commerce | Shopify sync, stock alerts, order processing | Inventory DB, exception queue, reorder triggers |
| Clara | Customer Experience | Order status checks, review responses, support triage | Customer DB, response templates, escalation queue |

---

## Information Flow

### Morning Check-In Flow

```
[Notion: Scheduled trigger, 6:00 AM]
         |
         v
[Xavier (Notion agent): Query Agent Registry for health data]
         |
         +-- Check Last Run timestamps against expected schedules
         +-- Check Error Count (30d) thresholds
         +-- Flag offline/degraded agents
         |
         +-- Write results --> Activity Log
         +-- Create exceptions --> Exception Queue (if needed)
         +-- Update summary property --> Xavier's Briefing Handoff DB
         |
         v
[Notion: Scheduled trigger, 6:05 AM]
         |
         v
[Clare (Notion agent): Read Xavier's output + Activity Log + Exception Queue]
         |
         +-- Compile morning briefing
         +-- Write --> Morning Briefing page
         |
         v
[JD reads briefing in Notion, ~7:00 AM]
```

No n8n involvement. Entire flow runs inside Notion.

### Exception Flow

```
[Any agent encounters issue beyond authority]
         |
         v
[Agent: Create entry in Exception Queue]
         |
         +-- Type, Severity, Details
         +-- Suggested escalation path
         +-- Status = Open
         |
         v
[Xavier (Notion agent): DB trigger on new Exception Queue entry]
         |
         +-- Evaluate severity + type
         +-- Route to handler (Franklin, Warren, Aurelius, or JD)
         +-- Update "Escalated To" field
         |
         v
[Notion: Exception appears in JD's filtered view]
         |
         v
[JD: Review and resolve]
         |
         v
[Resolution logged, Status = Resolved]
```

### Tier 1 Agent Execution Flow

```
[Notion: Trigger fires (schedule / DB property change / manual)]
         |
         v
[Notion AI Agent: Execute instructions]
         |
         +-- Read from source databases
         +-- Apply logic (filtering, scoring, drafting)
         +-- Write results to target databases
         |
         +-- On success --> Write to Activity Log (Status: Completed)
         +-- On error --> Write to Activity Log (Status: Error)
         |                + Create Exception Queue entry
         v
[Done]
```

### Tier 2 Agent Execution Flow

```
[Notion: Trigger fires]
         |
         v
[Notion AI Agent: Execute Notion-side logic]
         |
         +-- Read/write Notion databases
         +-- Determine what external API call is needed
         |
         v
[Notion agent triggers n8n webhook with payload]
         |
         v
[n8n: Execute API call (e.g., Gmail send, QuickBooks query)]
         |
         +-- Return result to Notion via API write
         |
         v
[Notion AI Agent: Process API result, write final state]
         |
         +-- Activity Log entry
         +-- Exception if API call failed
```

### Tier 3 Agent Execution Flow

```
[n8n: Trigger fires (schedule / webhook / event)]
         |
         v
[n8n: Execute workflow]
         |
         +-- API calls to external systems
         +-- AI processing (Claude API)
         +-- Write results --> Notion databases via API
         |
         +-- Log start/end --> Activity Log
         +-- Errors --> Exception Queue
         +-- Handoffs --> Trigger next workflow
```

---

## Notion Agent Configuration Patterns

How Tier 1 agents are configured inside Notion.

### Trigger Types

| Trigger | When to Use | Example |
|---------|-------------|---------|
| Schedule | Recurring cadence (daily, weekly, monthly) | Xavier health check at 6 AM |
| DB property change | React to new/updated records | Xavier routes new exceptions on creation |
| Manual | On-demand by JD | Seneca strategic analysis |

### Agent Instruction Structure

Each Notion AI agent receives structured instructions defining:

```
IDENTITY
  Name, role, authority level, reporting chain

DATABASES (read)
  Which databases to query and what filters to apply

DATABASES (write)
  Which databases to update and what fields to set

LOGIC
  Decision rules, scoring criteria, routing logic
  Written as explicit if/then conditions, not prose

OUTPUT FORMAT
  Expected structure of results (which fields, what values)

ESCALATION RULES
  When to create an Exception Queue entry
  When to flag for Xavier vs. handle independently

HANDOFF RULES
  When to pass work to another agent (and which one)
  What data to include in the handoff
```

### Example: Xavier Health Check Configuration

```
IDENTITY
  Xavier, Chief of Staff, Authority Level 2-Coordination
  Reports to: JD. Supervises: All domain agents.

DATABASES (read)
  - Agent Registry: All records where Status = Active
  - Activity Log: Last 24 hours, filter by Status = Error

DATABASES (write)
  - Activity Log: Create new entry (Action Type: Health Check)
  - Exception Queue: Create entry if thresholds breached

LOGIC
  For each active agent:
    IF Last Run > expected interval + 5 min: flag as Offline
    IF Error Count (30d) > 5: flag as Degraded
    IF Health Score < 80: create Exception (Severity: Medium)
    IF Health Score < 70: create Exception (Severity: High, Escalated To: JD)

OUTPUT FORMAT
  Activity Log entry with:
    Action Summary: "Health check: X healthy, Y degraded, Z offline"
    Details: Per-agent breakdown

HANDOFF RULES
  After health check completes, set Xavier Briefing Handoff property
  to signal Clare to compile morning briefing.
```

---

## Database Schema

### Agent Registry

Master roster of all agents. Added: Platform column for tier tracking.

| Field | Type | Description |
|-------|------|-------------|
| Name | Text (Title) | Agent name (e.g., "Xavier") |
| Title | Text | Role title (e.g., "Chief of Staff") |
| Domain | Select | Coordination, Personal, Haze Gray, Puzzlehouse |
| Platform | Select | Notion-Native, Hybrid, n8n-Primary |
| Named For | Text | Historical namesake |
| Status | Select | Active, Inactive, Maintenance |
| Authority Level | Select | 1-Principal, 2-Coordination, 3-Supervisor, 4-Domain Agent |
| Reports To | Relation | Links to supervisor in Agent Registry |
| Supervises | Relation | Links to direct reports |
| Depends On | Multi-select/Text | Systems and agents this agent requires |
| Depended On By | Multi-select/Text | Agents that require this agent |
| Last Run | Date | Most recent execution timestamp |
| Last Error | Date | Most recent error timestamp |
| Error Count (30d) | Number | Errors in rolling 30-day window |
| Uptime % | Number | Calculated availability percentage |
| Health Score | Number | Composite score 0-100 |
| Spec Link | URL | Link to agent specification file |

### Activity Log

Real-time record of agent actions.

| Field | Type | Description |
|-------|------|-------------|
| Timestamp | Date | When action occurred |
| Agent | Relation | Links to Agent Registry |
| Status | Select | Online, Offline, Error, Maintenance |
| Action Type | Select | Health Check, Sync, Triage, Handoff, etc. |
| Action Summary | Text | Brief description |
| Details | Text | Full details (expandable) |
| Related Agent | Relation | If action involved another agent |
| Triggered By | Text | What initiated this action |
| Duration (sec) | Number | How long action took |
| Last Error Time | Date | If this action had an error |
| Error Message | Text | Error details if applicable |

### Exception Queue

Issues requiring human attention.

| Field | Type | Description |
|-------|------|-------------|
| ID | Text (Title) | Unique identifier (EX-001, EX-002, etc.) |
| Timestamp | Date | When exception occurred |
| Agent | Relation | Which agent raised it |
| Exception Type | Relation | Links to Exception Types |
| Severity | Select | Critical, High, Medium, Low |
| Summary | Text | One-line description |
| Details | Text | Full context |
| Escalated To | Relation | Who should handle this |
| Status | Select | Open, Pending Review, In Progress, Resolved, Closed |
| Resolution | Text | How it was resolved |
| Resolved By | Relation | Agent or person who resolved |
| Resolved At | Date | Resolution timestamp |

### Exception Types

Configuration table for exception categories.

| Field | Type | Description |
|-------|------|-------------|
| Exception Type | Text (Title) | Category name |
| Description | Text | What this type means |
| Default Severity | Select | Typical severity level |
| Default Escalation | Text | Who usually handles this |
| Applies To Agents | Multi-select | Which agents can raise this type |

### Memory Entries

Long-term memory storage for Evelyn (Memory Curator).

| Field | Type | Description |
|-------|------|-------------|
| ID | Text (Title) | Unique memory identifier |
| Content | Text | The memory content |
| Source | Select | Conversation, Email, Calendar, Manual, Agent |
| Source Agent | Relation | Which agent created this memory |
| Created | Date | When memory was captured |
| Last Accessed | Date | Most recent retrieval |
| Access Count | Number | Times this memory has been retrieved |
| Decay Score | Number | 0-100, decreases over time without access |
| Tags | Multi-select | Categorization tags |
| Related Memories | Relation | Links to associated Memory Entries |
| Status | Select | Active, Review, Archived, Deleted |

### Memory Review Queue

Memories flagged for human review or consolidation.

| Field | Type | Description |
|-------|------|-------------|
| Memory | Relation | Links to Memory Entries |
| Review Reason | Select | Low Decay Score, Conflict, Consolidation Candidate, Stale |
| Suggested Action | Select | Keep, Archive, Merge, Delete |
| Reviewed | Checkbox | Whether JD has reviewed |
| Resolution | Text | What was decided |

### Explicit Preferences

JD's stated preferences, separate from inferred memories.

| Field | Type | Description |
|-------|------|-------------|
| Category | Select | Communication, Scheduling, Travel, Finance, Health, Work |
| Preference | Text (Title) | The preference statement |
| Source | Text | Where/when JD stated this |
| Confidence | Select | Explicit (JD said it), Inferred (pattern-based), Provisional |
| Active | Checkbox | Whether this preference is current |
| Overrides | Relation | Links to preferences this one supersedes |

---

## Integration Map

### Notion Native Integrations

Notion connects natively to these services. No n8n needed.

| Service | Capability | Used By |
|---------|------------|---------|
| Google Workspace | Calendar events, Drive files | Evelyn (EA), Clare |
| Slack | Notifications, channel posts | Xavier (alerts), Clare (briefings) |
| Notion AI | Summarization, drafting, Q&A over DB content | All Tier 1 agents |
| Notion Semantic Search | Native search across pages and databases | Evelyn (Memory Curator) |

### External APIs via n8n

APIs that require n8n as middleware.

| System | Used By | Purpose | Connection |
|--------|---------|---------|------------|
| Shopify | Franklin, Clara, Ada | E-commerce ops | API Key |
| Clay | Eleanor | CRM enrichment | API |
| QuickBooks | Warren, Hetty | Accounting | OAuth API |
| LinkedIn | Helena, Dale | Content, outreach | API |
| Social Platforms | Ada | Multi-platform posting | Various APIs |
| Health APIs | Galen | Biometrics | Various |
| Travel APIs | Marco | Bookings | Various |
| ElevenLabs | Clare | Voice synthesis | API Key |
| Claude API | All (via n8n Code nodes) | AI processing | API Key |

### Vector Search

| Option | Status | Purpose |
|--------|--------|---------|
| Notion Semantic Search | Primary | Native search across workspace content |
| Pinecone (hivefind-memory-v2) | Optional fallback | High-dimensional vector search (3072d, Gemini embeddings) if Notion search proves insufficient for memory retrieval |

### Internal Connections

| From | To | Method | Purpose |
|------|-----|--------|---------|
| Notion AI Agent | Notion DBs | Native | Read/write during agent execution |
| Notion AI Agent | n8n | Webhook trigger | Request external API calls |
| n8n | Notion | API | Write results back from API calls |
| Relay.app | Notion | Native | macOS-native automations |
| n8n | External APIs | Various | API calls Notion cannot make |

---

## Health Monitoring

### Notion-Native Monitoring

Tier 1 agents are monitored entirely within Notion.

| Monitor | Method | Frequency |
|---------|--------|-----------|
| Agent heartbeat | Xavier checks Last Run timestamps against expected schedules | Every 6 hours |
| Error rate | Xavier queries Activity Log for Error status entries | Every 6 hours |
| Health score | Notion formula property on Agent Registry (auto-calculated) | Real-time |
| Exception backlog | Notion filtered view: Status = Open, sorted by age | Real-time |

### Uptime Calculation

```
Uptime % = (Successful Runs / Total Expected Runs) x 100
```

Measured over rolling 30-day window. Target: 99% for all agents.

### Health Score Formula

```
Health Score = (0.5 x Uptime %)
             + (0.3 x Error Factor)
             + (0.2 x Response Factor)

Where:
  Error Factor = 100 - (Error Count x 5), min 0
  Response Factor = 100 if avg response < threshold, scaled down otherwise
```

Implemented as a Notion formula property on Agent Registry. Updates automatically.

### Alert Thresholds

| Condition | Action |
|-----------|--------|
| Agent Last Run > expected interval + 5 min | Xavier flags in Activity Log |
| Health Score < 90 | Warning indicator on Agent Registry dashboard |
| Health Score < 80 | Xavier creates Exception (Severity: Medium) |
| Health Score < 70 | Xavier creates Exception (Severity: High, Escalated To: JD) |
| Error Count > 5 in 24 hours | Xavier creates Exception (Severity: Critical) |
| Uptime < 95% | Performance review triggered (Aurelius notified) |

---

## n8n Workflow Conventions

Applies only to Tier 2 API-gap workflows and Tier 3 primary workflows.

### Naming Convention

```
[Tier]_[Agent]_[Function]

Examples:
  T2_Evelyn_GmailFetch
  T2_Warren_QuickBooksSync
  T3_Franklin_ShopifyInventorySync
  T3_Ada_SocialPost
```

### Standard Workflow Structure

```
1. TRIGGER
   Webhook from Notion agent (Tier 2) or Schedule/Event (Tier 3)

2. START LOG
   Write to Activity Log via Notion API: Started

3. MAIN LOGIC
   API calls to external systems
   AI processing if needed (Claude API)

4. WRITE BACK
   Write results to Notion databases via API

5. ERROR HANDLER (parallel branch)
   Catch errors --> Create Exception Queue entry --> Alert Xavier

6. END LOG
   Write to Activity Log via Notion API: Completed
```

### Error Handling

All n8n workflows must:

1. Catch errors with try/catch or error workflow
2. Log error details to Activity Log (Notion API write)
3. Create Exception Queue item for significant errors
4. Retry transient failures (3 attempts, exponential backoff)
5. Return a structured error payload to the calling Notion agent (Tier 2)

---

## Operating Rhythm

### Daily Cadence

| Time | Activity | Runs In |
|------|----------|---------|
| 6:00 AM | Xavier health check | Notion (Tier 1) |
| 6:05 AM | Clare compiles briefing | Notion (Tier 1) |
| 6:30 AM | Morning briefing ready | Notion page |
| ~7:00 AM | JD morning check-in | Notion dashboard |
| Throughout | Tier 1 agents execute on DB triggers | Notion |
| Throughout | Tier 2/3 agents execute on schedule/webhook | Notion + n8n |
| Throughout | Exceptions queue as raised | Notion |
| ~6:00 PM | Clare compiles day summary | Notion (Tier 1) |
| ~7:00 PM | JD evening check-in | Notion dashboard |

### Weekly Cadence

| Day | Activity | Runs In |
|-----|----------|---------|
| Monday | Xavier produces week-ahead preview | Notion |
| Friday | Xavier + Clare produce week summary | Notion |
| Sunday | Automated performance report generated | Notion (formula rollups) |

### Monthly Cadence

| Activity | Owner | Runs In |
|----------|-------|---------|
| Agent performance review | Xavier + Aurelius | Notion |
| Exception pattern analysis | Xavier | Notion |
| System health report | Xavier | Notion |
| Recommendations to JD | Coordination agents | Notion |

---

## Resilience Design

### Single Points of Failure

| Component | Impact | Mitigation |
|-----------|--------|------------|
| Notion platform | All agent execution stops (Tier 1 + data layer) | Notion has 99.9% SLA; no self-hosted fallback. Accept this risk. |
| Notion API | Tier 2/3 cannot write results back | n8n queues writes locally; retries on reconnect |
| n8n instance | Tier 2 API gaps and Tier 3 workflows stop. Tier 1 agents unaffected. | Self-hosted backup; alerting. Reduced blast radius vs. v2.0. |
| Claude API | AI processing fails in n8n workflows | Fallback to simpler rule-based logic |
| Internet connectivity | All external API calls fail | Tier 1 agents still run (Notion workspace cached locally). Tier 2/3 queue and retry. |
| Pinecone | Vector memory fallback unavailable | Notion semantic search is primary. Pinecone is optional. No impact on core ops. |

### Failure Modes

| Scenario | Detection | Response |
|----------|-----------|----------|
| Tier 1 agent fails to run | Xavier health check: Last Run stale | Xavier creates exception; manual re-trigger |
| Tier 2 n8n webhook fails | n8n error handler returns error payload | Notion agent logs exception; retries once; escalates |
| Tier 3 workflow hangs | Xavier timeout check on Activity Log | Kill and retry; create exception |
| External API down | n8n error handler | Retry 3x; create exception; continue without external data |
| Notion write fails (from n8n) | n8n error handler | Queue locally; retry; alert |
| Multiple agents fail | Xavier pattern detection across Activity Log | Escalate immediately to JD |

### Data Protection

- Activity Log: Append-only, never delete
- Exception Queue: Resolved items archived, not deleted
- Agent Registry: Changes logged with timestamps
- Memory Entries: Decay scoring, not deletion. Archived memories retained.
- All databases: Daily backup via Notion export

---

## Future Considerations

### Tier Migration Path

As Notion AI agent capabilities expand:

- Tier 2 agents move to Tier 1 when Notion adds native integrations (e.g., QuickBooks, Shopify)
- Tier 3 agents move to Tier 2 as agent logic shifts into Notion and n8n handles only the API call

### Observability

- Notion dashboard views serve as the primary monitoring surface
- n8n execution logs cover Tier 2/3 API calls
- Cross-agent request tracing via Activity Log relations (Triggered By + Related Agent fields)

### Memory System Evolution

- Notion semantic search replaces Pinecone for most retrieval
- Memory decay and consolidation run as Tier 1 Notion agents (Evelyn Memory Curator)
- If retrieval quality degrades, Pinecone fallback activates with Gemini 3072d embeddings

---

*Notion agents run the show. n8n fills API gaps. You manage by exception.*
