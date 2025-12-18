# Alert Monitor Workflow Template

**Pattern:** Schedule → Query → Evaluate → Alert (if threshold)

---

## Purpose

Monitor metrics and alert when thresholds are breached. Used by:
- **Franklin** - Inventory levels, accounts payable
- **Warren** - Spending anomalies, account activity
- **Galen** - Health metrics, recovery scores
- **Xavier** - Agent health, error rates

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Schedule Trigger |
| Frequency | Varies by metric criticality |

### Agent-Specific Schedules

| Agent | Monitor | Frequency |
|-------|---------|-----------|
| Franklin | Inventory levels | Daily 7:00 AM |
| Franklin | AP due dates | Daily 7:00 AM |
| Warren | Spending vs. baseline | Daily 8:00 AM |
| Warren | Account activity | Real-time (if available) |
| Galen | Recovery score | Daily 6:00 AM |
| Xavier | Agent error rates | Every 6 hours |

---

## Step-by-Step Build

### Step 1: Add Schedule Trigger

1. Create new workflow
2. Select **Schedule Trigger**
3. Set frequency based on metric urgency
4. Name: "[Agent] [Metric] Monitor"

### Step 2: Add Data Query Step

**Franklin - Inventory:**
```
Integration: Shopify
Action: Get Inventory Levels
Return: All products with current stock, reorder point, velocity
```

**Warren - Spending:**
```
Integration: Notion
Action: Query Transactions
Filter: Date >= 7 days ago
Return: Amounts by category, comparison to baseline
```

**Galen - Health:**
```
Integration: HTTP Request (Oura/Whoop API) or Notion
Action: Get Today's Metrics
Return: Recovery score, HRV, sleep quality
```

**Xavier - Agent Health:**
```
Integration: Notion
Action: Query Activity Log
Filter: Agent errors, Date >= 24 hours
Return: Error counts, error types, affected agents
```

### Step 3: Add AI Evaluation Step

```
AI Prompt:
"Evaluate these metrics against thresholds:

Data:
{{query_results}}

Thresholds:
{{agent_thresholds}}

For each metric:
1. Compare current value to threshold
2. Calculate severity (OK, WARNING, CRITICAL)
3. If breached, provide context and recommendation

Return structured analysis:
- Metrics OK (list)
- Metrics WARNING (list with values)
- Metrics CRITICAL (list with values)
- Recommendations (for each breach)"
```

### Step 4: Add Conditional Path

```
Path: If any CRITICAL or WARNING
├→ CRITICAL: [Immediate Alert + Log]
├→ WARNING: [Standard Alert + Log]
└→ OK: [Log only, no notification]
```

### Step 5: Add Alert Delivery

**For Critical:**
```
Integration: Slack
Channel: #alerts or DM
Message:
"🚨 CRITICAL: {{metric_name}}

Current: {{current_value}}
Threshold: {{threshold}}

{{recommendation}}

Action required immediately."
```

**For Warning:**
```
Integration: Gmail
To: JD's email
Subject: ⚠️ Warning: {{metric_name}} approaching threshold
Body:
"{{metric_name}} is at {{current_value}} (threshold: {{threshold}})

{{context}}

Recommended action: {{recommendation}}"
```

### Step 6: Add Notion Logging

```
Integration: Notion
Action: Create Page
Database: Alert Log
Properties:
  - Alert Type: {{metric_name}}
  - Severity: {{severity}}
  - Value: {{current_value}}
  - Threshold: {{threshold}}
  - Status: Alerted / Resolved
  - Timestamp: {{now}}
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Schedule Trigger      │
│   (Based on frequency)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Query Metrics         │
│   (Shopify/API/Notion)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI: Evaluate vs.      │
│   Thresholds            │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Path: By Severity     │
├─────────────────────────┤
│ CRITICAL │ WARN  │ OK   │
│     │    │   │   │  │   │
│     ▼    │   ▼   │  ▼   │
│  Slack   │ Email │ Log  │
│  +Email  │ +Log  │ only │
│  +Log    │       │      │
└──────────┴───────┴──────┘
```

---

## Threshold Configuration by Agent

### Franklin (Operations)

| Metric | Warning | Critical |
|--------|---------|----------|
| Inventory (units) | < Reorder Point | < 3 days supply |
| AP Due Date | Due in 3 days | Due today/overdue |
| Stockout Risk | < 7 days | < 3 days |

### Warren (Finance)

| Metric | Warning | Critical |
|--------|---------|----------|
| Daily Spending | 150% of baseline | 200% of baseline |
| Unusual Transaction | > $500 new merchant | > $1000 new merchant |
| Account Balance | < 2 months expenses | < 1 month expenses |

### Galen (Health)

| Metric | Warning | Critical |
|--------|---------|----------|
| Recovery Score | < 70 | < 50 |
| Sleep Quality | < 70% | < 50% |
| Consecutive Skip | 2 days | 4 days |

### Xavier (Fleet)

| Metric | Warning | Critical |
|--------|---------|----------|
| Agent Error Rate | > 5% | > 15% |
| Consecutive Errors | 3 | 5 |
| Agent Offline | 1 hour | 4 hours |

---

## Test Checklist

- [ ] Schedule trigger fires correctly
- [ ] Data query returns expected metrics
- [ ] AI evaluation identifies breaches correctly
- [ ] Path routing works for each severity
- [ ] Slack alert delivered (Critical)
- [ ] Email alert delivered (Warning)
- [ ] Alert logged to Notion
- [ ] OK status logs without notification

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No metrics returned | API connection failed | Re-authenticate integration |
| False positives | Threshold too sensitive | Adjust threshold values |
| Alerts not sent | Integration disconnected | Check Slack/Gmail connection |
| Duplicate alerts | No deduplication | Add check for recent alerts |
| Missing context | AI prompt incomplete | Add more data to evaluation |

---

## Variations

### "Trend-Based" Version

Alert based on trends, not just current value:

```
[Query Last 7 Days]
    ↓
[AI: Detect Trend]
    ↓
[Path: If declining trend]
    ├→ YES: [Proactive Alert]
    └→ NO: [Standard monitoring]
```

### "Auto-Recovery" Version

Attempt automatic resolution before alerting:

```
[Threshold Breach Detected]
    ↓
[Attempt Auto-Fix] (e.g., retry, restart)
    ↓
[Path: If still breached]
    ├→ YES: [Alert Human]
    └→ NO: [Log recovery, no alert]
```

---

*Template Version: 1.0 | December 2025*
