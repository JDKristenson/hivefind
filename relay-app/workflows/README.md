# Hivefind Relay - Workflow Templates

This directory contains reusable workflow templates for building Hivefind agents in Relay.app.

## Quick Navigation

| Template | Description | Used By |
|----------|-------------|---------|
| [Daily Report](./daily-report.md) | Scheduled morning report workflow | Xavier, Warren, Franklin |
| [Weekly Report](./weekly-report.md) | End-of-week summary workflow | All agents |
| [Email Handler](./email-handler.md) | Process incoming emails | Clara, Helena, Hamilton |
| [Content Publisher](./content-publisher.md) | Social media posting workflow | Ada |
| [Alert Monitor](./alert-monitor.md) | Threshold-based alerting | Franklin, Warren, Galen |
| [Escalation Handler](./escalation-handler.md) | Route issues to humans | Clara, Hamilton, Aurelius |

## How to Use These Templates

### Step 1: Identify the Workflow Pattern

Each Hivefind agent has Core Responsibilities in their spec. Each responsibility maps to a Workflow:

| Responsibility Type | Template to Use |
|--------------------|-----------------|
| "Daily briefing" or "Morning scan" | Daily Report |
| "Weekly summary" or "Friday digest" | Weekly Report |
| "Handle incoming [emails/messages]" | Email Handler |
| "Post content" or "Publish" | Content Publisher |
| "Monitor [metric] and alert" | Alert Monitor |
| "Escalate when [condition]" | Escalation Handler |

### Step 2: Create the Workflow in Relay.app

1. Go to your Agent's page
2. Click **"Create Workflow"** or use the Chat to say "Create a workflow for [responsibility]"
3. Use the template as your reference for triggers and steps

### Step 3: Move Workflow to Agent (if created standalone)

If you created the workflow outside the Agent:
- **From Workspace**: Right-click workflow → "Move to Agent" → Select your Agent
- **From Editor**: Click [...] menu → "Move to Agent"

---

## Template Structure

Each template includes:

1. **Purpose** - What this workflow accomplishes
2. **Trigger Configuration** - How the workflow starts
3. **Step-by-Step Build** - Each node to add
4. **AI Prompt Template** - Paste-ready prompts
5. **Path Logic** - Conditional routing
6. **Output Configuration** - Where results go
7. **Test Checklist** - How to verify it works

---

## Common Patterns

### Pattern A: Schedule → Query → AI → Output

```
[Schedule Trigger]
    ↓
[Integration: Query data]
    ↓
[AI Step: Process/analyze]
    ↓
[Integration: Send/save output]
    ↓
[Notion: Log activity]
```

**Used for:** Daily reports, weekly summaries, monitoring scans

### Pattern B: Event → Categorize → Route → Respond

```
[Event Trigger (email/webhook)]
    ↓
[AI Step: Categorize]
    ↓
[Path: Route by category]
    ├→ [Category A handling]
    ├→ [Category B handling]
    └→ [Escalation]
    ↓
[Integration: Respond/notify]
    ↓
[Notion: Log]
```

**Used for:** Email handlers, customer service, triage

### Pattern C: Query → Evaluate → Alert (if threshold)

```
[Schedule Trigger]
    ↓
[Integration: Query metric]
    ↓
[AI Step: Evaluate against threshold]
    ↓
[Path: If threshold breached]
    ├→ YES: [Send alert]
    └→ NO: [Log only]
```

**Used for:** Inventory alerts, health monitors, compliance checks

---

## Integration Reference

### Most Common Integrations

| Integration | Common Uses |
|-------------|-------------|
| **Notion** | Databases, logs, trackers, coordination |
| **Gmail** | Send emails, monitor inbox |
| **Google Calendar** | Schedule queries, event creation |
| **Shopify** | Orders, inventory, customers |
| **Slack** | Alerts, notifications |

### Notion Database Patterns

All Hivefind agents coordinate via shared Notion databases:

- **Agent Reports** - Daily/weekly outputs from each agent
- **Escalation Queue** - Items flagged for human review
- **Activity Log** - Audit trail of all agent actions
- **[Domain] Tracker** - Domain-specific tracking (Support Log, Inventory, etc.)

---

*See individual template files for detailed build instructions.*
