# Escalation Handler Workflow Template

**Pattern:** Trigger → Evaluate → Route → Alert

---

## Purpose

Route issues to humans when they exceed agent authority. Used by:
- **Clara** - Customer complaints beyond authority
- **Hamilton** - Scope creep, blocked deliverables
- **Franklin** - High-value decisions, compliance issues
- **Aurelius** - Charter alignment concerns
- **All agents** - Errors and exceptions

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Webhook or Conditional (within workflow) |
| Source | Other agents or threshold breach |

### Common Escalation Triggers

| Agent | Escalation Condition |
|-------|---------------------|
| Clara | Refund >$50, unresolved complaint, VIP issue |
| Hamilton | Scope change, blocked >48h, client dissatisfaction |
| Franklin | Purchase >$500, compliance issue, inventory critical |
| Warren | Spending anomaly, investment decision |
| All | Error unrecoverable, uncertain decision |

---

## Step-by-Step Build

### Step 1: Add Escalation Trigger

**Option A: Webhook (from other agents)**
```
Trigger: Webhook
Endpoint: /escalate
Expected payload:
{
  "source_agent": "Clara",
  "escalation_type": "refund_approval",
  "priority": "high",
  "context": {...},
  "recommendation": "Approve $75 refund for VIP customer"
}
```

**Option B: Conditional (within workflow)**
```
[Previous Step]
    ↓
[Path: If exceeds threshold]
    ├→ YES: [Escalation Handler]
    └→ NO: [Continue normal flow]
```

### Step 2: Add Context Compilation

Gather all relevant information:

```
Integration: Notion (Query)
Action: Get related records
- Original request/issue
- Customer/client history
- Previous interactions
- Agent's analysis
```

### Step 3: Add AI Synthesis Step

```
AI Prompt:
"Compile an escalation summary:

Source: {{source_agent}}
Type: {{escalation_type}}
Priority: {{priority}}

Context:
{{context}}

Agent's Recommendation: {{recommendation}}

Create a concise summary that:
1. States the issue clearly
2. Explains why it requires human decision
3. Presents the agent's recommendation
4. Provides clear options for action
5. Includes relevant data/history

Keep it brief and actionable."
```

### Step 4: Add Routing Logic

Route based on priority and type:

```
Path: By Priority
├→ CRITICAL: [Slack] + [Email] + [Notion]
├→ HIGH: [Email] + [Notion]
└→ MEDIUM: [Notion only, batch in daily report]
```

### Step 5: Add Alert Delivery

**For Critical (Slack + Email):**
```
Integration: Slack
Channel: #escalations or DM
Message:
"🚨 Escalation from {{source_agent}}

{{summary}}

[View in Notion] [Approve] [Decline]"

Integration: Gmail
To: JD's email
Subject: [{{priority}}] {{escalation_type}} - Action Required
Body: {{full_escalation}}
```

**For High (Email only):**
```
Integration: Gmail
To: JD's email
Subject: Action Required: {{escalation_type}} from {{source_agent}}
Body: {{full_escalation}}
```

### Step 6: Add Escalation Queue Entry

```
Integration: Notion
Action: Create Page
Database: Escalation Queue
Properties:
  - Title: {{escalation_type}}
  - Source Agent: {{source_agent}}
  - Priority: {{priority}}
  - Status: Pending
  - Summary: {{summary}}
  - Recommendation: {{recommendation}}
  - Created: {{now}}
  - Due: {{calculated_due}}
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Escalation Trigger    │
│   (Webhook or Path)     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Gather Context        │
│   (Notion queries)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI: Synthesize        │
│   (Create summary)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Path: By Priority     │
├─────────────────────────┤
│ CRITICAL  │ HIGH │ MED  │
│     │     │  │   │  │   │
│     ▼     │  ▼   │  ▼   │
│  Slack    │Email │Notion│
│  +Email   │      │only  │
│  +Notion  │+Notion│     │
└───────────┴──────┴──────┘
            │
            ▼
┌─────────────────────────┐
│   Add to Queue          │
│   (Track resolution)    │
└─────────────────────────┘
```

---

## Escalation Types by Agent

### Clara (Customer Support)

| Type | Threshold | Priority |
|------|-----------|----------|
| Refund >$50 | Amount exceeds authority | HIGH |
| Unresolved complaint | 2+ exchanges without resolution | HIGH |
| VIP customer issue | Customer in Eleanor's VIP tier | HIGH |
| Product defect pattern | 3+ same complaint | CRITICAL |
| PR risk | Viral potential | CRITICAL |

### Hamilton (Engagement Manager)

| Type | Threshold | Priority |
|------|-----------|----------|
| Scope change | Any deviation from SOW | HIGH |
| Blocked deliverable | >48 hours no progress | HIGH |
| Client dissatisfaction | Negative feedback | CRITICAL |
| Timeline risk | >5 days before deadline | HIGH |
| Budget variance | >10% overage | HIGH |

### Franklin (Operations)

| Type | Threshold | Priority |
|------|-----------|----------|
| Purchase approval | >$500 | HIGH |
| Compliance issue | Any deviation | CRITICAL |
| Critical inventory | <3 days stock | HIGH |
| Vendor issue | Delivery failure, quality problem | HIGH |

---

## Test Checklist

- [ ] Webhook receives escalation payload
- [ ] Context gathered correctly
- [ ] Summary clear and actionable
- [ ] Priority routing works (Critical/High/Medium)
- [ ] Slack alert delivered (if Critical)
- [ ] Email delivered (if Critical or High)
- [ ] Queue entry created
- [ ] Response mechanism works (approve/decline)

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Escalations not received | Webhook URL incorrect | Verify endpoint in source agent |
| Missing context | Query failed | Check Notion integration |
| Wrong priority | Threshold misconfigured | Review escalation rules |
| Alert not delivered | Integration disconnected | Re-authenticate Slack/Gmail |
| Queue not updating | Notion schema mismatch | Verify database properties |

---

## Resolution Flow

After escalation is resolved:

```
[Human Decision in Notion/Slack]
    ↓
[Update Queue Status: Resolved]
    ↓
[Notify Source Agent]
    ↓
[Source Agent Continues Workflow]
```

---

*Template Version: 1.0 | December 2025*
