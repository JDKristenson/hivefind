# AI Crew Architecture

## Overview
This document defines the organizational structure, coordination layers, and design principles for JD's AI agent ecosystem—a coordinated team handling personal operations, Haze Gray Consulting, and Puzzlehouse.com.

---

## Agent Roster — Canonical Reference

### 18 Agents Across 4 Domains

| Agent | Named For | Historical Significance | Title | Domain |
|-------|-----------|------------------------|-------|--------|
| **COORDINATION LAYER** |||||
| Xavier | Charles Xavier (Professor X) | Fictional founder of the X-Men; telepathic leader who coordinates a team of individuals with extraordinary abilities | Chief of Staff | Agent fleet operations |
| Clare | Clare Boothe Luce | Playwright, journalist, U.S. Congresswoman, and Ambassador to Italy; first American woman appointed to a major ambassadorship | Communications Officer | Briefings, coaching |
| Aurelius | Marcus Aurelius | Roman Emperor (161–180 AD) and Stoic philosopher; authored *Meditations* while leading military campaigns | Keeper of the Charter | Accountability |
| **PERSONAL STAFF** |||||
| Evelyn | Evelyn Lincoln | Personal secretary to President John F. Kennedy for 12 years; known for unwavering discretion and meticulous organization | Executive Assistant | Email, calendar |
| Eleanor | Eleanor Roosevelt | First Lady, diplomat, and activist; maintained relationships across politics, labor, civil rights, and arts throughout her life | Relationship Steward | CRM, network |
| Warren | Warren Buffett | Chairman of Berkshire Hathaway; built fortune through patient value investing and long-term compounding | Chief Financial Steward | Finance |
| Hetty | Hetty Green | "The Witch of Wall Street"; amassed fortune of $100M+ (early 1900s) through shrewd investing and legendary frugality | Tax Strategist | Tax optimization |
| Galen | Galen of Pergamon | Greek physician (129–216 AD) whose theories dominated Western medicine for 1,500 years; personal physician to Roman emperors | Chief Health Officer | Biometrics, health |
| Martha | Martha (Biblical) + Martha Stewart | Biblical Martha: hospitable and practical, spoke directly to Jesus about priorities. Martha Stewart: built lifestyle empire on home and entertaining | Keeper of the Realm | Home, family |
| Marco | Marco Polo | Venetian explorer (1254–1324) who traveled the Silk Road to China and documented the unknown for European audiences | Chief Travel Officer | Travel logistics |
| Seneca | Seneca the Younger | Roman Stoic philosopher (4 BC–65 AD); advisor to Emperor Nero; wrote extensively on time, focus, and the shortness of life | Chief Learning Officer | Curriculum, focus |
| Iris | Iris (Greek goddess) | Divine messenger who traveled between Olympus and Earth; personification of the rainbow connecting heaven to mortal world | Chief Knowledge Officer | Knowledge management |
| **HAZE GRAY CONSULTING** |||||
| Helena | Helena Rubinstein | Founded global cosmetics empire; pioneered modern beauty industry through systematic market identification and scientific marketing | Business Development Manager | Lead generation |
| Cicero | Marcus Tullius Cicero | Roman statesman and orator (106–43 BC); considered greatest orator in Roman history; his speeches remain models of persuasion | Chief Persuasion Officer | Proposals, pitches |
| Dale | Dale Carnegie | Author of *How to Win Friends and Influence People* (1936); pioneered self-improvement and interpersonal communication training | Content Strategist | LinkedIn, newsletter |
| Hamilton | Alexander Hamilton | First U.S. Secretary of the Treasury; established American financial system; prolific writer of the Federalist Papers | Engagement Manager | Client delivery |
| **PUZZLEHOUSE.COM** |||||
| Ada | Ada Lovelace | World's first computer programmer (1815–1852); wrote algorithm for Charles Babbage's Analytical Engine; daughter of Lord Byron | Social Media Director | Social content |
| Franklin | Benjamin Franklin | Founding Father, inventor, diplomat; known for *Poor Richard's Almanack* and practical wisdom on thrift and industry | Store Operations Manager | E-commerce ops |
| Clara | Clara Barton | Founder of the American Red Cross (1881); served as nurse in Civil War; known as "Angel of the Battlefield" | Customer Service Representative | Support, complaints |

---

## Org Chart

```
                                    JD
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
              XAVIER              AURELIUS            CLARE
           Chief of Staff      Keeper of Charter   Communications
           (Operations)        (Accountability)      (Briefings)
                 │                   ▲                   ▲
    ┌────────────┼────────────┐      │                   │
    │            │            │      │                   │
 PERSONAL    HAZE GRAY    PUZZLE     │                   │
  STAFF       CONSULT      HOUSE     │                   │
    │            │            │      │                   │
    ├─Evelyn     ├─Helena     ├─Ada  │ receives          │ receives
    ├─Eleanor    ├─Cicero     ├─Franklin  escalations    │ agent
    ├─Warren─┐   ├─Dale       └─Clara     from all       │ reports
    │   └─Hetty  └─Hamilton              agents          │
    ├─Galen                                              │
    ├─Martha                                             │
    ├─Marco                                              │
    ├─Seneca                                             │
    └─Iris
```

---

## Agent Registry by Domain

### Coordination Layer (3)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Xavier | Chief of Staff | Keep the trains on time invisibly; surface only what requires command decision | Specced |
| Clare | Communications Officer | Start and close the day with clarity; coach communications delivery | Specced |
| Aurelius | Keeper of the Charter | Capture and reflect JD's principles; maintain accountability | Specced |

### Personal Staff (9)

| Agent | Title | Mission | Status |
|-------|-------|---------|--------|
| Evelyn | Executive Assistant | Protect JD's time; triage email, manage calendar, prep meetings | Specced |
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
| Dale | Clare | Dale creates content → Clare coaches delivery → JD publishes |
| Helena | Cicero | Helena qualifies leads → Cicero pitches them |
| Helena | Eleanor | Helena queries CRM for warm paths; Eleanor maintains relationships |
| Ada | Franklin | Ada promotes products; Franklin manages inventory alignment |
| Dale | Helena | Dale monitors engagement; Helena receives inbound lead flags |
| Evelyn | All | Evelyn coordinates scheduling across all agent requests |

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
- **Personal Staff**: Calendar, preferences, health data
- **HGC Staff**: Client records, pipeline, project timelines
- **Puzzlehouse Staff**: Shopify data, inventory, customers

### 4. Escalation by Exception
Agents handle routine work autonomously. Escalate only:
- Decisions beyond authority
- High-stakes items (money, reputation, legal)
- Novel situations not covered by training
- Charter-relevant patterns (→ Aurelius)

### 5. Observable Operations
Every agent logs activity to Notion:
- Audit trail for debugging
- Performance data for optimization
- Accountability for agent health

### 6. Single Source of Truth
One agent owns each domain:
- Warren owns finance (Hetty reports to Warren)
- Franklin owns Puzzlehouse ops (Clara reports to Franklin)
- No overlapping authority

---

## Information Flows

### Daily Rhythm
```
6:00 AM   Evelyn pulls calendar, flags conflicts
6:30 AM   Clare compiles morning briefing from agent reports
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
Friday    All agents submit weekly metrics to Notion
          Clare compiles weekly briefing
          Warren delivers financial letter (includes Hetty's tax data)
          Franklin delivers Puzzlehouse ops report (includes Clara's patterns)
```

### Content Publishing Flow
```
1. Dale creates content (mines recordings, drafts posts/articles)
2. JD reviews and approves substance
3. Clare coaches delivery (voice, audience, presentation)
4. JD publishes
5. Dale monitors engagement
6. Dale flags warm leads → Helena
7. Eleanor coordinates outreach
```

### Lead-to-Client Flow
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
| Orchestration | n8n (primary), Relay.app (alternative) |
| Repository | Notion (central hub for all agent data) |
| AI Models | Claude (reasoning), specialized models as needed |
| Voice | ElevenLabs (audio briefings, feedback) |
| Video | HeyGen (video avatars for briefings) |
| Development | Claude Code, Cursor |
| Finance | QuickBooks Online (via Hetty) |
| CRM | Clay (via Eleanor) |
| E-commerce | Shopify (via Franklin) |
| Calendar/Email | Google Workspace |

---

## Notion Structure

```
📁 AI Crew HQ
├── 🎯 Command Dashboard
│   ├── Today's Briefing
│   ├── Active Escalations
│   ├── Agent Health Status
│   └── Key Metrics
├── 📋 Agent Registry (Database)
│   └── [Each agent's page with spec, status, logs]
├── 📊 Briefing Archive
│   ├── Daily Briefings (Clare)
│   └── Weekly Summaries (Clare)
├── 🔄 Workflows
│   ├── n8n Configurations
│   └── Relay.app Configurations
├── 📈 Domain Dashboards
│   ├── Personal (Warren's financial hub, Galen's health)
│   ├── HGC (Helena's pipeline, Hamilton's delivery tracker)
│   └── Puzzlehouse (Franklin's ops, Ada's social metrics)
├── 🧪 QA & Testing
│   └── Agent health checks, test logs
└── 📚 Documentation
    ├── Architecture (this doc)
    ├── Agent Roster (canonical HR reference)
    ├── Build Plan
    └── Conventions
```

---

## Open Questions

1. **Notification Channels**: Which alerts go to Slack vs. text vs. email vs. briefing?
2. **Failure Handling**: What happens when an agent can't complete a task?
3. **Demo Mode**: How do we show this to clients without exposing real data?
4. **Agent Communication Protocols**: Standard format for inter-agent handoffs?

---

*Last Updated: December 2024*
*Version: 2.0*
*Status: Canonical Reference*
