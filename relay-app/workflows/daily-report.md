# Daily Report Workflow Template

**Pattern:** Schedule → Query → AI → Output

---

## Purpose

Generate a morning briefing or daily status report. Used by:
- **Xavier** - Daily briefing for JD
- **Warren** - Daily financial scan
- **Franklin** - Daily inventory monitor
- **Hamilton** - Daily client status
- **Galen** - Daily health check-in

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Schedule Trigger |
| Frequency | Daily |
| Time | See agent spec (typically 6-8 AM) |
| Timezone | User's local timezone |

### Agent-Specific Times

| Agent | Time | Rationale |
|-------|------|-----------|
| Xavier | 6:00 AM | Before JD's day starts |
| Warren | 7:00 AM | After market pre-open |
| Franklin | 7:00 AM | Before store opens |
| Hamilton | 8:00 AM | Start of business day |
| Galen | 7:00 AM | Morning wellness check |

---

## Step-by-Step Build

### Step 1: Add Schedule Trigger

1. Create new workflow
2. Select **Schedule Trigger**
3. Set to daily at specified time
4. Name: "[Agent] Daily [Report Type]"

### Step 2: Add Data Query Steps

Add one or more integration steps to gather data:

**For Xavier (Chief of Staff):**
```
Step 2a: Google Calendar → Get Today's Events
Step 2b: Notion → Query Inbox (filter: unread/new)
Step 2c: Notion → Query Agent Reports (filter: yesterday)
```

**For Warren (Financial):**
```
Step 2a: [Market Data API] → Get overnight changes
Step 2b: Notion → Query Portfolio
Step 2c: Notion → Query Pending Transactions
```

**For Franklin (Operations):**
```
Step 2a: Shopify → Get Inventory Levels
Step 2b: Notion → Query Accounts Payable (due within 7 days)
Step 2c: Shopify → Get Yesterday's Orders
```

**For Hamilton (Engagement):**
```
Step 2a: Notion → Query Active Deliverables
Step 2b: Google Calendar → Get Today's Client Meetings
Step 2c: Notion → Query Blocked Items
```

### Step 3: Add AI Processing Step

1. Add **AI Step** (Agent or AI Generate)
2. Select model (GPT-4o recommended)
3. Paste agent's system prompt from spec
4. Add processing prompt:

**AI Prompt Template:**

```
Based on the following data, generate today's [briefing/report]:

## Calendar
{{step2a.events}}

## Inbox/Pending Items
{{step2b.results}}

## Recent Activity
{{step2c.results}}

Generate the report in the format specified in your instructions.
Highlight anything requiring immediate attention.
```

### Step 4: Add Output Step

**Option A: Email (most agents)**
```
Integration: Gmail
Action: Send Email
To: [User's email]
Subject: "[Agent] Daily [Report] — {{date}}"
Body: {{ai_step.output}}
```

**Option B: Notion (for logging)**
```
Integration: Notion
Action: Create Page
Database: Agent Reports
Properties:
  - Agent: [Agent Name]
  - Date: {{date}}
  - Type: Daily Report
  - Content: {{ai_step.output}}
```

### Step 5: Add Activity Log (Optional but Recommended)

```
Integration: Notion
Action: Create Page
Database: Activity Log
Properties:
  - Agent: [Agent Name]
  - Action: Daily Report Generated
  - Timestamp: {{now}}
  - Status: Complete
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Schedule Trigger      │
│   (Daily @ [time])      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Query Data Sources    │
│   (Calendar, Notion,    │
│   Shopify, etc.)        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI Step: Compile      │
│   (Use agent prompt)    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Send Output           │
│   (Gmail or Notion)     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Log Activity          │
│   (Notion Activity Log) │
└─────────────────────────┘
```

---

## Test Checklist

- [ ] Trigger fires at correct time
- [ ] All data sources return data
- [ ] AI output matches agent voice
- [ ] Email/output delivered correctly
- [ ] Activity logged in Notion
- [ ] Run manually to verify format

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No data returned | Query filter too strict | Broaden filter, check date range |
| Report not sent | Email step failed | Verify Gmail connection |
| Wrong time | Timezone mismatch | Check trigger timezone setting |
| AI output generic | System prompt missing | Paste full agent prompt |
| Report too long | Too much data | Add limits to queries |

---

## Variations

### "Only When Needed" Version

Add a path after data query:
```
[Query Data]
    ↓
[Path: If items exist]
    ├→ YES: [Continue to AI + Output]
    └→ NO: [Skip or minimal log]
```

### "Include Alerts" Version

Add conditional alerting:
```
[AI Step]
    ↓
[Path: If urgent items]
    ├→ YES: [Send Email] + [Slack Alert]
    └→ NO: [Send Email only]
```

---

*Template Version: 1.0 | December 2025*
