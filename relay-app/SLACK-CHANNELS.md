# Hivefind Slack Channel Architecture

## Overview

All Hivefind agents route notifications through a tiered Slack channel system. Channels are organized by **urgency**, not by agent, to minimize noise and ensure critical items surface.

---

## Channel Structure

### Tier 1: Command (Must Watch)
| Channel | Purpose | Who Posts | Frequency |
|---------|---------|-----------|-----------|
| `#hf-command` | Escalations requiring human decision | Xavier, Aurelius, any agent with urgent escalation | Rare (goal: <3/week) |

**Examples:**
- Agent retirement recommendations
- Platform migration approvals
- Budget/spending decisions
- Charter breach alerts
- Critical system failures

---

### Tier 2: Briefings (Daily Check)
| Channel | Purpose | Who Posts | Frequency |
|---------|---------|-----------|-----------|
| `#hf-briefings` | Scheduled reports and summaries | Clare, Xavier, domain leads | Daily/Weekly |

**Examples:**
- Clare's daily briefing
- Xavier's monthly fleet review
- Weekly domain summaries
- Scheduled performance reports

---

### Tier 3: Alerts (Monitor)
| Channel | Purpose | Who Posts | Frequency |
|---------|---------|-----------|-----------|
| `#hf-alerts` | Errors, warnings, issues needing visibility | Any agent | As needed |

**Examples:**
- API failures (non-critical)
- Rate limit warnings
- Task failures
- Integration issues
- Recovery notifications

---

### Tier 4: Activity (Optional/Muted)
| Channel | Purpose | Who Posts | Frequency |
|---------|---------|-----------|-----------|
| `#hf-activity` | General activity log, FYI items | Any agent | Frequent |

**Examples:**
- Task completions
- Health check confirmations
- Routine notifications
- Debug/audit trail

---

### Domain Channels (Business Separation)
| Channel | Purpose | Who Posts | Frequency |
|---------|---------|-----------|-----------|
| `#hf-hazegray` | Haze Gray Consulting operations | Helena, Cicero, Dale, Hamilton | As needed |
| `#hf-puzzlehouse` | Puzzle House operations | Ada, Clara, Franklin | As needed |

**Use for:**
- Client-specific notifications
- Business domain escalations
- Revenue/operations alerts
- Domain-specific reports

---

## Routing Rules

### By Severity

| Severity | Channel | Action Required |
|----------|---------|-----------------|
| **CRITICAL** | `#hf-command` | Immediate decision needed |
| **HIGH** | `#hf-alerts` | Review within 24h |
| **MEDIUM** | `#hf-alerts` | Review when convenient |
| **LOW** | `#hf-activity` | FYI only |

### By Message Type

| Type | Channel |
|------|---------|
| Escalation (decision needed) | `#hf-command` |
| Scheduled report | `#hf-briefings` |
| Error/warning | `#hf-alerts` |
| Task completion | `#hf-activity` |
| Haze Gray business | `#hf-hazegray` |
| Puzzle House business | `#hf-puzzlehouse` |

---

## Agent Channel Assignments

### Coordination Agents
| Agent | Primary Channel | Escalation Channel |
|-------|-----------------|-------------------|
| Xavier | `#hf-alerts` | `#hf-command` |
| Clare | `#hf-briefings` | `#hf-command` |
| Aurelius | `#hf-briefings` | `#hf-command` |
| Evelyn (Memory) | `#hf-activity` | `#hf-alerts` |

### Personal Agents
| Agent | Primary Channel | Escalation Channel |
|-------|-----------------|-------------------|
| Eleanor | `#hf-activity` | `#hf-alerts` |
| Warren | `#hf-briefings` | `#hf-command` |
| Seneca | `#hf-activity` | `#hf-alerts` |
| Martha | `#hf-activity` | `#hf-alerts` |
| Galen | `#hf-activity` | `#hf-alerts` |
| Marco | `#hf-activity` | `#hf-alerts` |
| Iris | `#hf-activity` | `#hf-alerts` |
| Hetty | `#hf-activity` | `#hf-alerts` |
| Evelyn (EA) | `#hf-briefings` | `#hf-command` |

### Haze Gray Agents
| Agent | Primary Channel | Escalation Channel |
|-------|-----------------|-------------------|
| Helena | `#hf-hazegray` | `#hf-command` |
| Cicero | `#hf-hazegray` | `#hf-command` |
| Dale | `#hf-hazegray` | `#hf-command` |
| Hamilton | `#hf-hazegray` | `#hf-command` |

### Puzzle House Agents
| Agent | Primary Channel | Escalation Channel |
|-------|-----------------|-------------------|
| Ada | `#hf-puzzlehouse` | `#hf-command` |
| Clara | `#hf-puzzlehouse` | `#hf-command` |
| Franklin | `#hf-puzzlehouse` | `#hf-command` |

---

## Message Formatting

### Standard Format
```
[AGENT] Action/Status

Details here.

-[Initial]
```

### Escalation Format
```
[URGENT] Brief issue description

What happened. Impact. Recommendation.

Yes/no question or clear ask.

-[Initial]
```

### Report Format
```
[REPORT] Title - Date

Summary content.

- Bullet points
- Key metrics

-[Initial]
```

---

## Slack Setup Checklist

- [ ] Create `#hf-command` (private, JD only)
- [ ] Create `#hf-briefings` (private, JD only)
- [ ] Create `#hf-alerts` (private, JD only)
- [ ] Create `#hf-activity` (private, can be muted)
- [ ] Create `#hf-hazegray` (private, business sensitive)
- [ ] Create `#hf-puzzlehouse` (private, business sensitive)
- [ ] Connect Relay.app Slack integration
- [ ] Test post to each channel

---

## Quick Reference Card

```
Need a decision?     → #hf-command
Sending a report?    → #hf-briefings
Error or warning?    → #hf-alerts
Just FYI?           → #hf-activity
Haze Gray business? → #hf-hazegray
Puzzle House?       → #hf-puzzlehouse
```

---

*Document Version: 1.0*
*Created: December 2025*
