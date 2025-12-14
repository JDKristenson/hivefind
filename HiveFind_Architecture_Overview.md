# HiveFind: Multi-Agent Automation System

**Repository:** https://github.com/JDKristenson/hivefind
**Author:** JD Kristenson
**Date:** December 2025

---

## Vision Summary

HiveFind is a personal automation system built around the concept of specialized AI "agents," each responsible for a distinct domain of work and life management. Rather than building a monolithic automation platform, HiveFind distributes responsibilities across purpose-built agents that communicate through shared infrastructure (Notion databases, Slack channels, webhooks).

The system philosophy mirrors organizational design: just as a well-run company has specialists who own their domains while collaborating through defined interfaces, HiveFind agents own their areas of expertise while sharing data through standardized protocols.

**Core Principles:**
1. **Single Responsibility:** Each agent owns one domain completely
2. **Loose Coupling:** Agents communicate through shared data stores, not direct dependencies
3. **Human-in-the-Loop:** Agents advise and automate; humans decide and override
4. **Graceful Degradation:** If one agent fails, others continue operating
5. **Collective Learning:** Agents accumulate wisdom over time and share knowledge across domains

---

## Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      HUMAN INTERFACE LAYER                       │
│  Slack (commands, alerts)  │  Vestaboard  │  reMarkable  │ DMs  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                         │
│                         n8n Workflows                            │
│         (Triggers, Logic, Transformations, Routing)              │
└─────────────────────────────────────────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
┌────────────────────────────────┐  ┌────────────────────────────────┐
│          DATA LAYER            │  │        MEMORY LAYER            │
│  Notion (structured data)      │  │  Pinecone (experiential)       │
│  Google Calendar  │  APIs      │  │  Notion (explicit knowledge)   │
└────────────────────────────────┘  │  Evelyn (curator agent)        │
                │                   └────────────────────────────────┘
                ▼                                 │
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
│  Whoop │ OpenWeather │ Sunsama │ Monday.com │ Email │ etc.      │
└─────────────────────────────────────────────────────────────────┘
```

### Memory Layer Detail

The Memory Layer enables collective learning across all agents. See `docs/MEMORY_ARCHITECTURE.md` for full specification.

**Two-Tier Design:**
- **Explicit Knowledge (Notion):** Human-curated preferences, business rules, relationship context
- **Experiential Memory (Pinecone):** Semantic storage of task outcomes, patterns, corrections

**Memory Curator (Evelyn):**
- Validates and tags incoming memories from all agents
- Serves relevant context to agents before they make decisions
- Consolidates patterns weekly; promotes validated insights to explicit knowledge
- Processes human corrections as high-value learning signals

**Agent Integration Pattern:**
```
Before Decision: Agent queries Evelyn for relevant knowledge
After Task: Agent submits memory payload (outcome, lessons, confidence)
On Correction: Evelyn captures human override and extracts lesson
```

### Agent Relationship Map

```
                              ┌──────────────┐
                              │   HAMILTON   │
                              │  (Schedule)  │
                              │      📅      │
                              └──────┬───────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
       ┌──────────┐           ┌──────────┐           ┌──────────┐
       │  CLARE   │           │  WARREN  │           │  GALEN   │
       │ (Tasks)  │◄─────────►│(Finance) │           │ (Health) │
       │    📋    │           │    💰    │           │    🏃    │
       └────┬─────┘           └──────────┘           └────┬─────┘
            │                                              │
            │         ┌──────────────────────┐            │
            │         │                      │            │
            ▼         ▼                      ▼            ▼
       ┌──────────┐                              ┌──────────┐
       │  MARTHA  │                              │  MARCO   │
       │  (Home)  │                              │ (Travel) │
       │    🏠    │                              │    ✈️    │
       └──────────┘                              └──────────┘

                    BUSINESS AGENTS (Haze Gray)
       ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ ELEANOR  │  │  HELENA  │  │  PORTIA  │  │  THEA    │
       │  (CRM)   │  │ (Leads)  │  │(Projects)│  │(Learning)│
       │    👥    │  │    🎯    │  │    📊    │  │    📚    │
       └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### Data Flow Patterns

**Pattern 1: Scheduled Intelligence**
```
Schedule Trigger → Query Data Sources → Apply Logic → Generate Output → Deliver to Human
```
Example: Galen queries Oura Ring at 6 AM, calculates recovery impact, adjusts Hamilton's task load, alerts via Slack.

**Pattern 2: Event-Driven Response**
```
External Event → Webhook Receives → Route by Type → Process → Update State → Notify
```
Example: New lead form submission triggers Helena, who scores the lead, creates CRM entry via Eleanor, schedules follow-up via Hamilton.

**Pattern 3: Human-Initiated Query**
```
Slack Command → Parse Request → Query Relevant Agent(s) → Format Response → Reply
```
Example: `/galen` command queries Whoop API, formats recovery data, returns to Slack DM.

**Pattern 4: Cross-Agent Coordination**
```
Agent A Detects Condition → Writes to Shared State → Agent B Reads State → Takes Action
```
Example: Galen detects low recovery, writes to Activity Log with flag, Hamilton reads flag and reduces scheduled tasks by 35%.

---

## Agent Directory

| Agent | Domain | Primary Data Source | Key Outputs |
|-------|--------|---------------------|-------------|
| **Evelyn** | Memory/Knowledge | Pinecone, Notion Memory DBs | Context briefs, pattern reports, correction processing |
| **Hamilton** | Calendar/Schedule | Google Calendar, Sunsama | Schedule optimization, conflict resolution |
| **Clare** | Task Management | Notion Tasks DB | Priority coaching, completion tracking |
| **Warren** | Finance | Budget DB, Transactions | Spending alerts, runway calculations |
| **Galen** | Health/Wellness | Oura Ring API | Recovery briefings, load adjustment signals |
| **Martha** | Household | Household DB | Chore reminders, home status (Vestaboard) |
| **Marco** | Travel | Travel DB, Calendar | Trip briefings, meeting dossiers (reMarkable) |
| **Eleanor** | CRM | Contacts DB | Relationship management, follow-up reminders |
| **Helena** | Lead Generation | Leads DB | Lead scoring, pipeline management |
| **Portia** | Project Management | Engagements DB | Status tracking, milestone alerts |
| **Thea** | Learning/Development | Lessons DB | Daily micro-lessons, skill tracking |

---

## Infrastructure Components

### n8n Workflow Engine
- **Role:** Orchestration, scheduling, API integration
- **Deployment:** Self-hosted or n8n Cloud
- **Workflows:** 23 active workflows across all agents

### Notion
- **Role:** Structured data storage, human-readable interface
- **Databases:** Tasks, Contacts, Leads, Engagements, Travel, Household, Activity Log
- **Pattern:** Each agent reads/writes to specific databases

### Slack
- **Role:** Human interface, alerts, commands
- **Channels:** #health, #finance, #operations, #leads, #home
- **Pattern:** Domain-specific channels + DM for critical alerts

### Google Calendar
- **Role:** Schedule of record, bridge to Sunsama
- **Pattern:** Hamilton writes, other agents read

### Vestaboard
- **Role:** Ambient household display
- **Pattern:** Martha writes status updates (weather, tasks, presence)

### reMarkable
- **Role:** Offline document consumption
- **Pattern:** Marco generates PDFs, uploads via Google Drive sync

### Oura Ring
- **Role:** Biometric data source
- **Pattern:** Galen reads sleep, readiness, HRV data via Oura API

---

## Production Risk Assessment

### High Risk Areas (Likely Failure Points)

**1. API Rate Limits and Quotas**
- **Risk:** Oura, Google Calendar, Notion all have rate limits
- **Failure Mode:** Workflows fail silently when limits hit
- **Mitigation:** Add explicit rate limit handling, implement backoff, monitor API quota usage
- **Current State:** Not implemented; will break at scale

**2. Credential Expiration**
- **Risk:** OAuth tokens expire (Google), API keys rotate
- **Failure Mode:** Entire agent goes offline without notification
- **Mitigation:** Implement credential health checks, alert on auth failures
- **Current State:** Partial; some workflows log failures but no proactive monitoring

**3. Notion Schema Drift**
- **Risk:** Manual changes to Notion databases break workflows
- **Failure Mode:** Workflows error on missing properties, wrong types
- **Mitigation:** Schema validation layer, database snapshots, change detection
- **Current State:** Not implemented; fragile to human edits

**4. Single Point of Failure: n8n**
- **Risk:** n8n server downtime stops all automation
- **Failure Mode:** Complete system outage
- **Mitigation:** High-availability deployment, health monitoring, failover
- **Current State:** Single instance; no redundancy

### Medium Risk Areas

**5. Data Consistency Across Agents**
- **Risk:** Agents read stale data, write conflicts
- **Failure Mode:** Contradictory actions, duplicate entries
- **Mitigation:** Implement locking, use Notion's built-in conflict resolution
- **Current State:** Eventual consistency assumed; rare conflicts

**6. Alert Fatigue**
- **Risk:** Too many Slack notifications desensitize user
- **Failure Mode:** Critical alerts ignored among noise
- **Mitigation:** Alert severity levels, digest mode, quiet hours
- **Current State:** Basic routing implemented; no severity tuning

**7. External Service Dependencies**
- **Risk:** Third-party APIs change or deprecate
- **Failure Mode:** Workflows break without warning
- **Mitigation:** Version pinning, API monitoring, abstraction layers
- **Current State:** Direct API calls; no abstraction

### Low Risk Areas (But Worth Noting)

**8. Timezone Handling**
- **Risk:** Schedule triggers fire at wrong times during travel
- **Failure Mode:** Morning briefing arrives at 3 AM
- **Mitigation:** Dynamic timezone detection, travel-aware scheduling
- **Current State:** Hardcoded to US East; manual adjustment needed

**9. Cost Accumulation**
- **Risk:** API calls, n8n executions accumulate costs
- **Failure Mode:** Unexpected bills
- **Mitigation:** Usage monitoring, budget alerts
- **Current State:** Low volume; not yet a concern

### Recommended Improvements for Production

1. **Observability:** Add centralized logging, execution metrics, error tracking
2. **Testing:** Implement workflow unit tests, integration tests
3. **Documentation:** Maintain runbooks for each agent failure mode
4. **Alerting:** Meta-alert system that monitors agent health
5. **Backup:** Regular Notion database exports, workflow JSON backups

---

## Representative Agent: Galen (Health/Wellness)

### Agent Profile

| Attribute | Value |
|-----------|-------|
| **Name** | Galen |
| **Emoji** | 🏃 |
| **Domain** | Health and wellness management |
| **Named After** | Galen of Pergamon, ancient Greek physician |
| **Primary Data Source** | Oura Ring API |
| **Secondary Sources** | Activity Log (Notion), Calendar (Google) |
| **Output Channels** | Slack DM, Slack #health, Hamilton (schedule adjustment) |

### Job Description

**Title:** Health Intelligence Agent

**Reports To:** Human (JD Kristenson)

**Collaborates With:** Hamilton (schedule), Clare (task load), Martha (household routines)

**Mission Statement:**
Monitor physiological data to optimize daily performance. Translate biometric signals into actionable recommendations. Protect human energy by proactively adjusting commitments based on recovery status.

### Responsibilities

**1. Daily Recovery Briefing (6:00 AM)**
- Query Oura Ring API for previous night's sleep and readiness data
- Calculate readiness score, HRV, resting heart rate, sleep performance
- Generate natural language summary of physiological state
- Deliver briefing to Slack DM with emoji-coded status (🟢🟡🔴)
- Log briefing to Activity Log

**2. Recovery-Based Schedule Adjustment**
- When recovery score falls below thresholds, signal Hamilton to reduce load:
  - Recovery < 33%: Reduce task load by 50%
  - Recovery 33-50%: Reduce task load by 35%
  - Recovery 50-66%: Reduce task load by 20%
- Write adjustment signal to shared state for Hamilton to consume
- Notify human of automatic adjustment via Slack

**3. Weekly Health Trends (Sunday 8:00 PM)**
- Aggregate 7 days of Oura data
- Calculate weekly averages: recovery, HRV, sleep, strain
- Identify trends (improving, stable, declining)
- Compare to previous week
- Generate recommendations for upcoming week
- Post summary to #health channel

**4. On-Demand Status Query**
- Respond to `/galen` Slack command
- Return current recovery, last night's sleep, today's strain
- Include recommendation based on current state

### Workflows

| Workflow | Trigger | Frequency |
|----------|---------|-----------|
| `Galen_01_DailyRecoveryBriefing` | Schedule | Daily 6 AM |
| `Galen_02_RecoveryIntervention` | Webhook | Event-driven |
| `Galen_03_StrainTracking` | Schedule | Hourly |
| `Galen_04_RecoveryToHamilton` | Schedule | Daily 6:15 AM |
| `Galen_05_WeeklyTrends` | Schedule | Sunday 8 PM |

### Data Schema

**Oura Ring API Response (Relevant Fields):**
```json
{
  "daily_readiness": {
    "score": 67,
    "contributors": {
      "hrv_balance": 45,
      "resting_heart_rate": 52,
      "sleep_balance": 85
    }
  },
  "daily_sleep": {
    "score": 82,
    "total_sleep_duration": 25200,
    "rem_sleep_duration": 5700,
    "deep_sleep_duration": 5100,
    "efficiency": 88
  }
}
```

**Activity Log Entry:**
```json
{
  "Name": "Galen Daily Briefing - 2025-12-08",
  "Agent": "Galen",
  "Type": "Health Update",
  "Status": "Complete",
  "Summary": "Recovery: 67% (green). HRV: 45ms. Sleep: 7h. Recommendation: Normal capacity."
}
```

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Briefing delivery rate | 99% | Briefings delivered / days |
| Data freshness | < 30 min | Time from Oura sync to briefing |
| Adjustment accuracy | 80%+ | Days where adjustment matched subjective energy |
| Alert relevance | < 5% false positives | Unnecessary low-recovery alerts |

### Known Limitations

1. **Oura Dependency:** Entire agent fails if Oura API is unavailable or user doesn't wear ring
2. **Lag Time:** Oura data syncs when app is opened; morning briefing uses previous night's final sync
3. **Single Metric Focus:** Recovery score is primary signal; doesn't incorporate other health data (nutrition, stress, illness)
4. **Static Thresholds:** Currently uses fixed thresholds; will adapt to individual baseline via Memory Layer integration with Evelyn

### Future Enhancements

1. **Adaptive Thresholds:** Learn personal recovery patterns, adjust recommendations to individual baseline
2. **Multi-Source Integration:** Incorporate Apple Health, nutrition tracking, subjective wellness logs
3. **Predictive Modeling:** Forecast tomorrow's recovery based on today's strain and sleep onset
4. **Social Awareness:** Factor in calendar (high-stakes meetings) when making recommendations

---

## Conclusion

HiveFind demonstrates how personal automation can be organized around domain-specialized agents communicating through shared infrastructure. The system prioritizes human oversight while automating routine intelligence gathering and routing.

The architecture is intentionally simple; n8n workflows, Notion databases, and Slack channels are mature, well-documented tools that don't require custom infrastructure. This simplicity is both a strength (rapid iteration, low maintenance) and a limitation (lacks sophisticated coordination, no machine learning).

For production hardening, the primary investments should be in observability (knowing when things break), resilience (graceful degradation when dependencies fail), and testing (confidence that changes don't break existing functionality).

The agent model has proven valuable for organizing automation conceptually. Even without AI/ML components, framing workflows as "agents with jobs" makes the system more intuitive to extend, debug, and explain.

---

*Document generated for course submission. System actively in development.*
