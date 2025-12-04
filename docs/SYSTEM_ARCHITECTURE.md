# System Architecture

Technical architecture for the AI Crew ecosystem, defining the three-layer model and how components interact.

---

## Three-Layer Architecture

The AI Crew operates on a three-layer model with clear boundaries:

```
┌─────────────────────────────────────────────────────────────────┐
│                      HUMAN INTERFACE                            │
│                         (Notion)                                │
│                                                                 │
│  Your cockpit for monitoring, decisions, and exceptions         │
│  - Agent status pages                                           │
│  - Performance dashboards                                       │
│  - Exception queue for review                                   │
│  - Strategic decision log                                       │
│                                                                 │
│  YOU interact here. Agents display here.                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Relay.app / Notion API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│                         (n8n)                                   │
│                                                                 │
│  Where agents execute, coordinate, and hand off                 │
│  - Xavier routes incoming work                                  │
│  - Triggers fire agent workflows                                │
│  - Agent logic executes                                         │
│  - Cross-agent handoffs happen                                  │
│  - Errors caught and escalated                                  │
│                                                                 │
│  AGENTS interact here. Xavier coordinates here.                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Direct writes
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                │
│                    (Notion Databases)                           │
│                                                                 │
│  Persistent storage, audit trail, historical record             │
│  - Agent Registry (master roster)                               │
│  - Activity Log (what agents did)                               │
│  - Exception Queue (issues for review)                          │
│  - Domain-specific databases (CRM, inventory, etc.)             │
│                                                                 │
│  AGENTS write here. You read here.                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer Definitions

### Human Interface Layer

**Purpose:** Your window into the system.

**Primary Tool:** Notion

**What Lives Here:**
- Dashboards showing agent health and status
- Exception queue requiring your decisions
- Briefings compiled by Clare
- Strategic logs and decisions
- Performance trends and analytics

**Who Interacts:**
- You (JD) - primary consumer
- Clare - compiles briefings for display
- Occasionally other agents - surface urgent items

**Design Principles:**
- Optimized for human comprehension
- Visual, scannable, actionable
- Updated in real-time but consumed at check-in cadence
- Exception-driven (you see what needs attention)

---

### Orchestration Layer

**Purpose:** Where work gets done.

**Primary Tool:** n8n

**What Lives Here:**
- Agent workflow definitions
- Trigger logic (schedules, webhooks, events)
- Routing decisions (Xavier's domain)
- Integration connections to external APIs
- Error handling and retry logic

**Who Interacts:**
- Xavier - routes and monitors
- All agents - execute their workflows
- You - only for debugging/configuration

**Design Principles:**
- Automation-first (minimal human touch)
- Resilient (retries, fallbacks, error capture)
- Observable (everything logged)
- Modular (each agent = discrete workflow)

---

### Data Layer

**Purpose:** Single source of truth and audit trail.

**Primary Tool:** Notion Databases

**What Lives Here:**
- Agent Registry (who exists, their status)
- Activity Log (what happened, when)
- Exception Queue (what needs attention)
- Exception Types (configurable categories)
- Domain databases (CRM contacts, inventory, etc.)

**Who Interacts:**
- Agents - write constantly
- You - read at check-ins
- Xavier - monitors for anomalies
- External systems - via API

**Design Principles:**
- Append-mostly (don't delete history)
- Structured (consistent schemas)
- Linked (relationships between tables)
- Queryable (supports filters, views, rollups)

---

## Information Flow

### Morning Check-In Flow

```
[n8n: Scheduled 6 AM trigger]
         │
         ▼
[Xavier: Health check all agents]
         │
         ├── Online/Offline status → Activity Log
         ├── Errors detected → Exception Queue
         └── Summary → Clare
                         │
                         ▼
              [Clare: Compile briefing]
                         │
                         ▼
              [Notion: Morning Briefing Page]
                         │
                         ▼
                    [You read it]
```

### Exception Flow

```
[Agent encounters issue beyond authority]
         │
         ▼
[Agent: Log to Exception Queue]
         │
         ├── Type, Severity, Details
         ├── Suggested escalation path
         └── Status = Open
                │
                ▼
[Xavier: Detects new exception]
         │
         ├── Routes to correct handler
         │   (Franklin, Warren, Aurelius, or JD)
         │
         └── Updates Escalated To field
                │
                ▼
[Notion: Exception appears in your queue]
         │
         ▼
[You: Review and resolve]
         │
         ▼
[Resolution logged, Status = Resolved]
```

### Agent Execution Flow

```
[Trigger fires (schedule/webhook/event)]
         │
         ▼
[n8n: Agent workflow starts]
         │
         ├── Log start → Activity Log
         │
         ├── Execute logic
         │   ├── API calls to external systems
         │   ├── Data reads from Notion
         │   └── AI processing (Claude)
         │
         ├── Handle result
         │   ├── Success → Log completion
         │   ├── Needs handoff → Trigger next agent
         │   └── Error → Log error, create exception
         │
         └── Log end → Activity Log
```

---

## Database Schema

### Agent Registry

The master roster of all agents.

| Field | Type | Description |
|-------|------|-------------|
| Name | Text (Title) | Agent name (e.g., "Xavier") |
| Title | Text | Role title (e.g., "Chief of Staff") |
| Domain | Select | Coordination, Personal, Haze Gray, Puzzlehouse |
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

---

## Health Monitoring

### Uptime Calculation

```
Uptime % = (Successful Runs / Total Expected Runs) × 100
```

Measured over rolling 30-day window.

**Target:** 99% uptime for all agents

### Health Score Formula

```
Health Score = (Uptime Weight × Uptime %)
             + (Error Weight × Error Factor)
             + (Response Weight × Response Factor)

Where:
- Uptime Weight = 0.5
- Error Weight = 0.3
- Response Weight = 0.2
- Error Factor = 100 - (Error Count × 5), min 0
- Response Factor = 100 if avg response < threshold, scaled down otherwise
```

### Alert Thresholds

| Condition | Action |
|-----------|--------|
| Agent offline > 5 minutes | Xavier alert |
| Health Score < 90 | Warning in dashboard |
| Health Score < 80 | Exception created |
| Health Score < 70 | Escalate to JD |
| Error Count > 5 in 24 hours | Immediate review |
| Uptime < 95% | Performance review triggered |

---

## n8n Workflow Conventions

### Naming Convention

```
[Domain]_[Agent]_[Function]

Examples:
- Personal_Evelyn_EmailTriage
- Coordination_Xavier_HealthCheck
- Puzzlehouse_Franklin_InventorySync
```

### Standard Workflow Structure

Every agent workflow follows this pattern:

```
1. TRIGGER
   └── Schedule, Webhook, or Event

2. START LOG
   └── Write to Activity Log: Started

3. MAIN LOGIC
   └── Agent-specific processing

4. ERROR HANDLER (parallel branch)
   └── Catch errors → Create Exception → Alert Xavier

5. END LOG
   └── Write to Activity Log: Completed

6. HANDOFF (if applicable)
   └── Trigger next agent's workflow
```

### Error Handling

All workflows must:
1. Catch errors with try/catch or error workflow
2. Log error details to Activity Log
3. Create Exception Queue item for significant errors
4. Notify Xavier for routing decisions
5. Retry transient failures (3 attempts, exponential backoff)

---

## Integration Map

### External Systems

| System | Used By | Purpose | Connection |
|--------|---------|---------|------------|
| Google Workspace | Evelyn | Calendar, Email | OAuth API |
| Shopify | Franklin, Clara, Ada | E-commerce | API Key |
| Clay | Eleanor | CRM | API |
| QuickBooks | Warren, Hetty | Finance | OAuth API |
| LinkedIn | Helena, Dale | Content, Leads | API |
| Social Platforms | Ada | Content posting | Various APIs |
| Health APIs | Galen | Biometrics | Various |
| Travel APIs | Marco | Bookings | Various |
| ElevenLabs | Clare | Voice | API Key |
| Claude | All | AI Processing | API Key |

### Internal Connections

| From | To | Method | Purpose |
|------|-----|--------|---------|
| n8n | Notion | API | Write logs, exceptions, data |
| Notion | n8n | Webhook | Trigger on database changes |
| Relay.app | Both | Native | Sync and automation |

---

## Operating Rhythm

### Daily Cadence

| Time | Activity | System |
|------|----------|--------|
| 6:00 AM | Xavier health check | n8n scheduled |
| 6:05 AM | Clare compiles briefing | n8n triggered |
| 6:30 AM | Morning briefing ready | Notion page |
| ~7:00 AM | JD morning check-in | Notion dashboard |
| Throughout | Agents execute as triggered | n8n |
| Throughout | Exceptions queue as raised | Notion |
| ~6:00 PM | Clare compiles day summary | n8n triggered |
| ~7:00 PM | JD evening check-in | Notion dashboard |

### Weekly Cadence

| Day | Activity |
|-----|----------|
| Monday | Xavier produces week-ahead preview |
| Friday | Xavier + Clare produce week summary |
| Sunday | Automated performance report generated |

### Monthly Cadence

| Activity | Owner |
|----------|-------|
| Agent performance review | Xavier + Aurelius |
| Exception pattern analysis | Xavier |
| System health report | Xavier |
| Recommendations to JD | Coordination Layer |

---

## Resilience Design

### Single Points of Failure

| Component | Risk | Mitigation |
|-----------|------|------------|
| n8n instance | All orchestration stops | Self-hosted backup; alerting |
| Notion API | Cannot read/write data | Queue writes; cache reads |
| Claude API | AI processing fails | Fallback to simpler logic |
| Internet connectivity | All external APIs fail | Local queue; retry on reconnect |

### Failure Modes

| Scenario | Detection | Response |
|----------|-----------|----------|
| Agent workflow hangs | Xavier timeout check | Kill and retry; create exception |
| External API down | Error in workflow | Retry 3x; create exception; continue |
| Notion write fails | n8n error handler | Queue locally; retry; alert |
| Multiple agents fail | Xavier pattern detection | Escalate immediately to JD |

### Data Protection

- Activity Log: Append-only, never delete
- Exception Queue: Resolved items archived, not deleted
- Agent Registry: Changes logged with timestamps
- All databases: Daily backup via Notion export

---

## Future Considerations

### Scaling

Current architecture supports 18 agents. For significant expansion:
- Consider dedicated databases per domain
- Implement queue system for high-volume agents
- Add caching layer for frequently-accessed data

### Observability

Planned enhancements:
- Grafana dashboard for real-time monitoring
- Structured logging for log aggregation
- Trace IDs for cross-agent request tracking

### AI Enhancement

As Claude capabilities expand:
- Agents may gain more autonomous decision authority
- Natural language interfaces for exception resolution
- Predictive health monitoring

---

*This architecture balances automation with human oversight. Agents work autonomously; you manage by exception.*
