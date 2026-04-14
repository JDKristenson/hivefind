# Hivefind Architecture

Version 3.0 | April 2026

## Overview

This document defines the organizational structure, coordination layers, and design principles for JD's AI agent ecosystem -- a coordinated team of 19 agents handling personal operations, Haze Gray Consulting, and Puzzlehouse.com. All orchestration runs through Notion AI Agents as the primary platform, with n8n and Relay.app filling gaps for APIs Notion cannot reach natively.

---

## Agent Roster -- Canonical Reference

### 19 Agents Across 4 Domains

| Agent | Named For | Historical Significance | Title | Domain |
|-------|-----------|------------------------|-------|--------|
| **COORDINATION LAYER** |||||
| Xavier | Charles Xavier (Professor X) | Fictional founder of the X-Men; telepathic leader who coordinates a team of individuals with extraordinary abilities | Chief of Staff | Agent fleet operations |
| Clare | Clare Boothe Luce | Playwright, journalist, U.S. Congresswoman, and Ambassador to Italy; first American woman appointed to a major ambassadorship | Communications Officer | Briefings, coaching |
| Aurelius | Marcus Aurelius | Roman Emperor (161-180 AD) and Stoic philosopher; authored *Meditations* while leading military campaigns | Keeper of the Charter | Accountability |
| **PERSONAL STAFF** |||||
| Evelyn (EA) | Evelyn Lincoln | Personal secretary to President John F. Kennedy for 12 years; known for unwavering discretion and meticulous organization | Executive Assistant | Email, calendar |
| Evelyn (Memory) | Evelyn Lincoln | Same namesake as Evelyn (EA); the split reflects Lincoln's dual mastery of both gatekeeping and institutional memory | Memory Curator | Curate, consolidate, and serve the collective memory of all agents |
| Eleanor | Eleanor Roosevelt | First Lady, diplomat, and activist; maintained relationships across politics, labor, civil rights, and arts throughout her life | Relationship Steward | CRM, network |
| Warren | Warren Buffett | Chairman of Berkshire Hathaway; built fortune through patient value investing and long-term compounding | Chief Financial Steward | Finance |
| Hetty | Hetty Green | "The Witch of Wall Street"; amassed fortune of $100M+ (early 1900s) through shrewd investing and legendary frugality | Tax Strategist | Tax optimization |
| Galen | Galen of Pergamon | Greek physician (129-216 AD) whose theories dominated Western medicine for 1,500 years; personal physician to Roman emperors | Chief Health Officer | Biometrics, health |
| Martha | Martha (Biblical) + Martha Stewart | Biblical Martha: hospitable and practical, spoke directly to Jesus about priorities. Martha Stewart: built lifestyle empire on home and entertaining | Keeper of the Realm | Home, family |
| Marco | Marco Polo | Venetian explorer (1254-1324) who traveled the Silk Road to China and documented the unknown for European audiences | Chief Travel Officer | Travel logistics |
| Seneca | Seneca the Younger | Roman Stoic philosopher (4 BC-65 AD); advisor to Emperor Nero; wrote extensively on time, focus, and the shortness of life | Chief Learning Officer | Curriculum, focus |
| Iris | Iris (Greek goddess) | Divine messenger who traveled between Olympus and Earth; personification of the rainbow connecting heaven to mortal world | Chief Knowledge Officer | Knowledge management |
| **HAZE GRAY CONSULTING** |||||
| Helena | Helena Rubinstein | Founded global cosmetics empire; pioneered modern beauty industry through systematic market identification and scientific marketing | Business Development Manager | Lead generation |
| Cicero | Marcus Tullius Cicero | Roman statesman and orator (106-43 BC); considered greatest orator in Roman history; his speeches remain models of persuasion | Chief Persuasion Officer | Proposals, pitches |
| Dale | Dale Carnegie | Author of *How to Win Friends and Influence People* (1936); pioneered self-improvement and interpersonal communication training | Content Strategist | LinkedIn, newsletter |
| Hamilton | Alexander Hamilton | First U.S. Secretary of the Treasury; established American financial system; prolific writer of the Federalist Papers | Engagement Manager | Client delivery |
| **PUZZLEHOUSE.COM** |||||
| Ada | Ada Lovelace | World's first computer programmer (1815-1852); wrote algorithm for Charles Babbage's Analytical Engine; daughter of Lord Byron | Social Media Director | Social content |
| Franklin | Benjamin Franklin | Founding Father, inventor, diplomat; known for *Poor Richard's Almanack* and practical wisdom on thrift and industry | Store Operations Manager | E-commerce ops |
| Clara | Clara Barton | Founder of the American Red Cross (1881); served as nurse in Civil War; known as "Angel of the Battlefield" | Customer Service Representative | Support, complaints |

---

## Org Chart

```
                                    JD
                                     |
                 +-------------------+-------------------+
                 |                   |                   |
              XAVIER              AURELIUS            CLARE
           Chief of Staff      Keeper of Charter   Communications
           (Operations)        (Accountability)      (Briefings)
                 |                   ^                   ^
    +------------+------------+      |                   |
    |            |            |      |                   |
 PERSONAL    HAZE GRAY    PUZZLE     |                   |
  STAFF       CONSULT      HOUSE     |                   |
    |            |            |      |                   |
    +-Evelyn(EA) +-Helena     +-Ada  | receives          | receives
    +-Evelyn(Mem)+-Cicero     +-Franklin  escalations    | agent
    +-Eleanor    +-Dale       +-Clara     from all       | reports
    +-Warren-+   +-Hamilton              agents          |
    |   +-Hetty                                          |
    +-Galen                                              |
    +-Martha                                             |
    +-Marco                                              |
    +-Seneca                                             |
    +-Iris
```

Evelyn (EA) and Evelyn (Memory) share the Evelyn Lincoln lineage but operate as distinct agents. EA owns gatekeeping (email, calendar, scheduling). Memory owns the collective knowledge layer (retrieval, consolidation, preference tracking).

---

## Agent Registry by Domain

### Coordination Layer (3)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Xavier | Chief of Staff | Keep the trains on time invisibly; surface only what requires command decision | Specced |
| Clare | Communications Officer | Start and close the day with clarity; coach communications delivery | Specced |
| Aurelius | Keeper of the Charter | Capture and reflect JD's principles; maintain accountability | Specced |

### Personal Staff (10)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Evelyn (EA) | Executive Assistant | Protect JD's time; triage email, manage calendar, prep meetings | Specced |
| Evelyn (Memory) | Memory Curator | Curate, consolidate, and serve the collective memory of all agents | Specced |
| Eleanor | Relationship Steward | Transform scattered contacts into cultivated relationships | Specced |
| Warren | Chief Financial Steward | Compound wealth patiently; guard against slow leaks | Specced |
| Hetty | Tax Strategist | Capture every dollar, categorize correctly, claim every deduction | Specced |
| Galen | Chief Health Officer | Surface physical truth beneath the calendar; connect data to patterns | Specced |
| Martha | Keeper of the Realm | Anchor digital life to physical; ensure house runs, family supported | Specced |
| Marco | Chief Travel Officer | Orchestrate travel seamlessly; optimize value and loyalty | Specced |
| Seneca | Chief Learning Officer | Impose depth over breadth; build mastery through disciplined focus | Specced |
| Iris | Chief Knowledge Officer | Transform scattered knowledge into accessible wisdom | Specced |

### Haze Gray Consulting (4)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Helena | Business Development Manager | Fill the pipeline before it runs dry; identify and qualify opportunities | Specced |
| Cicero | Chief Persuasion Officer | Win rooms before entering them; construct cases, not just proposals | Specced |
| Dale | Content Strategist | Transform expertise into relationship-opening content | Specced |
| Hamilton | Engagement Manager | Run client operations with ledger precision; track every commitment | Specced |

### Puzzlehouse.com (3)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Ada | Social Media Director | Grow social presence with cultured, platform-native content on autopilot | Specced |
| Franklin | Store Operations Manager | Run Shopify with ledger precision; nothing over/understocked or overdue | Specced |
| Clara | Customer Service Representative | Make every customer feel heard, helped, and happy | Specced |

---

## Key Reporting Relationships

### Supervisory Relationships

| Supervisor | Direct Report | Rationale |
|------------|---------------|-----------|
| Warren | Hetty | Warren owns all finance; Hetty owns all tax within that |
| Franklin | Clara | Franklin owns Puzzlehouse operations; Clara handles customer-facing |

### Coordination Relationships

| Agent A | Agent B | Coordination |
|---------|---------|--------------|
| Dale | Clare | Dale creates content; Clare coaches delivery; JD publishes |
| Helena | Cicero | Helena qualifies leads; Cicero pitches them |
| Helena | Eleanor | Helena queries CRM for warm paths; Eleanor maintains relationships |
| Ada | Franklin | Ada promotes products; Franklin manages inventory alignment |
| Dale | Helena | Dale monitors engagement; Helena receives inbound lead flags |
| Evelyn (EA) | All | Evelyn (EA) coordinates scheduling across all agent requests |
| Evelyn (Memory) | All | Evelyn (Memory) serves knowledge retrieval requests from any agent |
| Evelyn (EA) | Evelyn (Memory) | EA routes meeting prep requests to Memory for context retrieval |

### Escalation Paths

| From | To | Trigger |
|------|-----|---------|
| All agents | Aurelius | Charter-relevant patterns, values conflicts |
| All agents | Xavier | Operational issues, agent health, system problems |
| Hetty | Warren | Tax operational matters (not directly to JD) |
| Clara | Franklin | Product issues, operational escalations |

---

## Design Principles

### 1. Coordination Before Chaos
Xavier (Chief of Staff) prevents agents from operating in silos:
- Routes inbound requests to appropriate agent
- Handles cross-agent coordination
- Manages escalation decisions
- Monitors agent health

### 2. Separation of Content and Delivery
Dale creates content; Clare coaches delivery:
- Content creation focused on substance
- Delivery coaching focused on presentation
- JD maintains final publishing authority

### 3. Domain Clustering
Agents grouped by shared context:
- **Personal Staff**: Calendar, preferences, health data, collective memory
- **HGC Staff**: Client records, pipeline, project timelines
- **Puzzlehouse Staff**: Shopify data, inventory, customers

### 4. Escalation by Exception
Agents handle routine work autonomously. Escalate only:
- Decisions beyond authority
- High-stakes items (money, reputation, legal)
- Novel situations not covered by training
- Charter-relevant patterns (to Aurelius)

### 5. Observable Operations
Every agent logs activity to Notion:
- Audit trail for debugging
- Performance data for optimization
- Accountability for agent health

### 6. Single Source of Truth
One agent owns each domain:
- Warren owns finance (Hetty reports to Warren)
- Franklin owns Puzzlehouse ops (Clara reports to Franklin)
- Evelyn (Memory) owns collective memory (all agents query through her)
- No overlapping authority

### 7. Memory as Infrastructure
Evelyn (Memory) provides a shared knowledge layer:
- Agents write observations and learnings to Memory Entries DB
- Agents query Evelyn (Memory) for context before acting
- Explicit preferences tracked and served on demand
- Periodic consolidation prevents memory bloat

---

## Information Flows

### Daily Rhythm

```
6:00 AM   Evelyn (EA) pulls calendar, flags conflicts
          (Notion agent scheduled trigger)
6:30 AM   Clare compiles morning briefing from agent reports
          Evelyn (Memory) surfaces relevant context for today's meetings
7:00 AM   JD receives video briefing (2-3 min)
          Throughout: Xavier routes inbound, coordinates handoffs
5:00 PM   Aurelius reviews daily commitments, flags misses
6:00 PM   Clare compiles evening summary
```

### Weekly Rhythm

```
Monday    Ada posts weekly content plan
          Helena reviews pipeline, prioritizes outreach
          Dale queues content for the week
          (All triggered by Notion agent scheduled automations)
Friday    All agents submit weekly metrics to Notion
          Clare compiles weekly briefing
          Warren delivers financial letter (includes Hetty's tax data)
          Franklin delivers Puzzlehouse ops report (includes Clara's patterns)
          Evelyn (Memory) runs consolidation pass on the week's entries
```

### Content Publishing Flow

Runs as a Notion agent workflow. Agent handoff logic unchanged:

```
1. Dale creates content (mines recordings, drafts posts/articles)
2. JD reviews and approves substance
3. Clare coaches delivery (voice, audience, presentation)
4. JD publishes
5. Dale monitors engagement
6. Dale flags warm leads to Helena
7. Eleanor coordinates outreach
```

### Lead-to-Client Flow

Runs as a Notion agent workflow. Agent handoff logic unchanged:

```
1. Helena scouts opportunities (news, LinkedIn, triggers)
2. Helena qualifies against ICP
3. Helena hands off to Cicero with dossier
4. Cicero crafts pitch/proposal
5. JD delivers pitch
6. Hamilton takes over post-win for delivery
```

---

## Technology Stack

| Layer | Tools |
|-------|-------|
| Orchestration | Notion AI Agents (primary), n8n/Relay.app (gap-filler for APIs Notion cannot reach) |
| Repository | Notion (central hub for all agent data) |
| Memory | Notion databases + Notion AI semantic search (primary), Pinecone + Gemini Embedding 2 (optional fallback) |
| AI Models | Claude (reasoning), specialized models as needed |
| Voice | ElevenLabs (audio briefings, feedback) |
| Video | Runway Characters (video avatars for briefings) |
| Development | Claude Code, Cursor |
| Finance | QuickBooks Online (via Hetty) |
| CRM | Clay (via Eleanor) |
| E-commerce | Shopify (via Franklin) |
| Calendar/Email | Google Workspace |

---

## Notion Structure

```
Hivefind HQ
+-- Command Dashboard
|   +-- Today's Briefing
|   +-- Active Escalations
|   +-- Agent Health Status
|   +-- Key Metrics
+-- Agent Registry (Database)
|   +-- [Each agent's page with spec, status, logs]
+-- Agent Configurations (Notion AI agent definitions)
|   +-- [One config per agent: trigger rules, prompt, tools, permissions]
+-- Briefing Archive
|   +-- Daily Briefings (Clare)
|   +-- Weekly Summaries (Clare)
+-- Memory Layer
|   +-- Memory Entries DB (observations, learnings, context from all agents)
|   +-- Memory Review Queue DB (pending consolidation and dedup)
|   +-- Explicit Preferences DB (JD's stated preferences, indexed by domain)
+-- Workflows
|   +-- Notion AI Agent Configurations
|   +-- n8n Configurations (gap-filler only)
|   +-- Relay.app Configurations (gap-filler only)
+-- Domain Dashboards
|   +-- Personal (Warren's financial hub, Galen's health)
|   +-- HGC (Helena's pipeline, Hamilton's delivery tracker)
|   +-- Puzzlehouse (Franklin's ops, Ada's social metrics)
+-- QA & Testing
|   +-- Agent health checks, test logs
+-- Documentation
    +-- Architecture (this doc)
    +-- Agent Roster (canonical HR reference)
    +-- Build Plan
    +-- Conventions
```

---

## Open Questions

1. **Notification Channels**: Partially resolved. Notion native notifications handle most agent-to-JD alerts. Remaining gap: which high-urgency alerts still need SMS or push outside Notion.
2. **Failure Handling**: Handled by Notion automations. When an agent task fails, Notion triggers a retry or escalation to Xavier. Edge cases around cascading failures still need testing.
3. **Demo Mode**: How do we show this to clients without exposing real data. Unresolved.
4. **Agent Communication Protocols**: Agents communicate via Notion DB writes. Each handoff creates a record in the receiving agent's inbox database with structured fields (source agent, priority, payload, deadline).

---

*Version: 3.0*
*Status: Canonical Reference*
