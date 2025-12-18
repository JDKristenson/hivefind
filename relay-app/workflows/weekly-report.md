# Weekly Report Workflow Template

**Pattern:** Schedule → Query → AI → Output

---

## Purpose

Generate an end-of-week summary or digest. Used by virtually all agents:
- **Xavier** - Weekly priorities summary
- **Aurelius** - Weekly reflection
- **Warren** - Weekly financial report
- **Franklin** - Weekly operations report
- **Hamilton** - Weekly engagement report
- **Ada** - Weekly social performance
- **Clara** - Weekly support digest
- **Eleanor** - Weekly relationship pulse

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Schedule Trigger |
| Frequency | Weekly |
| Day | Friday (most agents) or Sunday (Aurelius) |
| Time | See agent spec (typically 4-5 PM) |

### Agent-Specific Schedule

| Agent | Day | Time | Rationale |
|-------|-----|------|-----------|
| Xavier | Friday | 5:00 PM | End of work week |
| Aurelius | Sunday | 7:00 PM | Weekend reflection |
| Warren | Friday | 4:00 PM | Before markets close |
| Franklin | Friday | 5:00 PM | End of operations |
| Hamilton | Friday | 4:00 PM | Client week wrap-up |
| Ada | Friday | 5:00 PM | Social performance |
| Clara | Friday | 4:00 PM | Support metrics |
| Eleanor | Friday | 3:00 PM | Before weekend |

---

## Step-by-Step Build

### Step 1: Add Schedule Trigger

1. Create new workflow
2. Select **Schedule Trigger**
3. Set to weekly on specified day/time
4. Name: "[Agent] Weekly [Report Type]"

### Step 2: Add Data Query Steps

Query the week's activity. Typical pattern:

**Query 2a: This Week's Completed Items**
```
Integration: Notion
Action: Query Database
Database: [Relevant tracker]
Filter:
  - Status = "Complete"
  - Date >= [7 days ago]
```

**Query 2b: This Week's Activity Log**
```
Integration: Notion
Action: Query Database
Database: Activity Log
Filter:
  - Agent = [This Agent]
  - Date >= [7 days ago]
```

**Query 2c: Domain-Specific Data**

| Agent | Query |
|-------|-------|
| Warren | Portfolio performance, transactions |
| Franklin | Inventory movements, AP/AR |
| Ada | Social metrics, post performance |
| Clara | Support tickets, resolution rates |
| Hamilton | Deliverables by client |

### Step 3: Add AI Processing Step

1. Add **AI Step**
2. Paste agent's system prompt
3. Add weekly report prompt:

**AI Prompt Template:**

```
Generate your weekly report based on the following data:

## Completed This Week
{{step2a.results}}

## Activity Log
{{step2b.results}}

## Domain Data
{{step2c.results}}

Follow the weekly report format from your instructions.
Include:
- Key metrics and trends
- Notable accomplishments
- Patterns or concerns
- Recommendations for next week
```

### Step 4: Add Output Steps

**Email to User:**
```
Integration: Gmail
Action: Send Email
To: [User's email]
Subject: "[Agent] Weekly Report — Week of {{week_start_date}}"
Body: {{ai_step.output}}
```

**Save to Notion:**
```
Integration: Notion
Action: Create Page
Database: Agent Reports
Properties:
  - Agent: [Agent Name]
  - Date: {{date}}
  - Type: Weekly Report
  - Content: {{ai_step.output}}
```

### Step 5: Coordinate with Other Agents (Optional)

For agents whose reports feed into others:

**Xavier consumes other agents' reports:**
```
Before Xavier's Friday report:
  - Query Agent Reports database
  - Filter: Type = "Weekly Report", Date = this week
  - Include summaries in Xavier's compilation
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Schedule Trigger      │
│   (Weekly @ Friday 5pm) │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Query Week's Data     │
│   • Completed items     │
│   • Activity log        │
│   • Domain metrics      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI Step: Compile      │
│   Weekly Report         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Send Email            │
│   (To user)             │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Save to Notion        │
│   (Agent Reports DB)    │
└─────────────────────────┘
```

---

## Aurelius Special: Weekly Reflection

Aurelius's weekly report is different—it's a charter alignment reflection:

### Modified Step 2 for Aurelius

```
Query 2a: Notion → This week's agent reports (all agents)
Query 2b: Notion → Charter principles
Query 2c: Notion → Escalations flagged this week
Query 2d: Notion → Activity patterns (decisions made)
```

### Modified AI Prompt for Aurelius

```
As Aurelius, conduct your Weekly Reflection.

## This Week's Agent Activity
{{step2a.results}}

## Charter Principles
{{step2b.charter}}

## Escalations
{{step2c.escalations}}

Analyze:
1. What went well? What aligned with the charter?
2. What patterns concern you?
3. Where did decisions drift from stated values?
4. What should be different next week?

Write the reflection in your philosophical voice.
```

---

## Test Checklist

- [ ] Trigger fires on correct day/time
- [ ] Week date range calculated correctly
- [ ] All data sources return relevant data
- [ ] Metrics are accurate
- [ ] AI output follows agent's format
- [ ] Email delivered with proper formatting
- [ ] Report saved to Notion
- [ ] Report accessible to other agents if needed

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Empty report | No activity logged | Verify daily logging working |
| Wrong date range | Filter calculation off | Check date math in filters |
| Missing metrics | Query incomplete | Add all data sources |
| Report not in agent voice | System prompt missing | Add full agent prompt |
| Duplicate reports | Trigger firing twice | Check schedule configuration |

---

## Variations

### "Conditional Escalation" Version

If concerning patterns found, alert separately:

```
[AI Step: Generate Report]
    ↓
[AI Step: Evaluate for Concerns]
    ↓
[Path: If concerns exist]
    ├→ YES: [Email Report] + [Escalation to Aurelius]
    └→ NO: [Email Report only]
```

### "Include Comparison" Version

Compare to previous week:

```
[Query This Week] + [Query Last Week]
    ↓
[AI Step: Generate with Week-over-Week comparison]
```

---

*Template Version: 1.0 | December 2025*
