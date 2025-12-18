# Hivefind Relay - Architecture Guide

## Understanding Relay.app Agents (December 2025)

This document explains how Relay.app's new **Agents** feature works and how the Hivefind agent specs translate into the platform.

> **Note**: The Agents feature is currently a Feature Preview (December 2025). This guide reflects the latest architecture.

---

## How Relay.app Agents Work

### Key Concept: Agents are AI Teammates that Own Workflows

In Relay.app, an **Agent is an AI teammate** that owns a set of responsibilities defined as **Workflows**. Think of Agents as extending your org chart—each Agent takes ownership of a different area of work.

### The Mental Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RELAY.APP AGENT ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────┘

                              YOUR ORG CHART
                              ─────────────
                                    │
                                   JD
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
     ┌─────────┐              ┌─────────┐              ┌─────────┐
     │ AGENT   │              │ AGENT   │              │ AGENT   │
     │ Xavier  │              │ Clara   │              │  Ada    │
     │ Chief   │              │ Support │              │ Social  │
     │ of Staff│              │  Agent  │              │ Media   │
     └────┬────┘              └────┬────┘              └────┬────┘
          │                        │                        │
    ┌─────┴─────┐            ┌─────┴─────┐            ┌─────┴─────┐
    │ WORKFLOWS │            │ WORKFLOWS │            │ WORKFLOWS │
    │ owned by  │            │ owned by  │            │ owned by  │
    │ Xavier:   │            │ Clara:    │            │ Ada:      │
    │           │            │           │            │           │
    │ • Daily   │            │ • Email   │            │ • Daily   │
    │   Briefing│            │   Response│            │   Post    │
    │ • Priority│            │ • Returns │            │ • Trend   │
    │   Triage  │            │   Process │            │   Research│
    │ • Calendar│            │ • Weekly  │            │ • Weekly  │
    │   Sync    │            │   Report  │            │   Report  │
    └───────────┘            └───────────┘            └───────────┘
```

### What is an Agent?

An **Agent** in Relay.app is:
- An **AI teammate** with a specific job (e.g., "Customer Support Agent")
- **Owns multiple Workflows** that define its responsibilities
- Has an **activity history** showing all completed work
- Has a **chat interface** where you can ask it to create new workflows

### What is a Workflow?

A **Workflow** is:
- An automation that defines "what should happen when"
- Has a **Trigger** (schedule, webhook, app event)
- Has **Steps/Actions** that execute in sequence
- Can be standalone OR owned by an Agent

### Agents vs. Folders

| Feature | Folders | Agents |
|---------|---------|--------|
| Group workflows | ✓ | ✓ |
| AI teammate mental model | ✗ | ✓ |
| Activity history | ✗ | ✓ |
| Chat interface | ✗ | ✓ |
| Create workflows via chat | ✗ | ✓ |

### Agent Structure

```
AGENT: Clara (Customer Support)
├── ACTIVITY CALENDAR (shows busy days)
├── CHAT INTERFACE (create new workflows, ask questions)
└── OWNED WORKFLOWS:
    │
    ├── WORKFLOW: Email Response Handler
    │   ├── Trigger: New email to support inbox
    │   └── Steps: AI categorize → Shopify lookup → AI respond → Log
    │
    ├── WORKFLOW: Return Processing
    │   ├── Trigger: Return request detected
    │   └── Steps: Validate → Process in Shopify → Send confirmation
    │
    ├── WORKFLOW: Weekly Support Digest
    │   ├── Trigger: Friday 4pm schedule
    │   └── Steps: Query logs → Analyze patterns → Send report
    │
    └── WORKFLOW: Review Request
        ├── Trigger: 3 days after positive resolution
        └── Steps: Check satisfaction → Send review request
```

---

## Translating Hivefind Specs to Relay.app

### What Each Hivefind Agent Spec Becomes

| Hivefind Spec Section | Relay.app Component |
|----------------------|---------------------|
| Agent Name & Description | **Agent** (the AI teammate) |
| System Prompt | Context for AI steps within workflows |
| Core Responsibilities | **Workflows** owned by the Agent |
| Triggers | Workflow triggers (schedule, webhook, app event) |
| Integrations | Steps within each Workflow |
| Decision Framework | Logic within AI steps + workflow paths |
| Output Formats | AI formatting instructions in steps |

### Example Translation: Xavier (Chief of Staff)

**From the Hivefind spec:**
- Agent: Xavier - Chief of Staff
- Core Responsibilities: Daily briefing, priority triage, calendar coordination

**In Relay.app:**

```
AGENT: Xavier (Chief of Staff)
│
├── CHAT: "Create a new workflow for urgent escalations"
│
└── OWNED WORKFLOWS:
    │
    ├── WORKFLOW: Daily Briefing
    │   ├── Trigger: Schedule (6:00 AM daily)
    │   ├── Step 1: Google Calendar → Get today's events
    │   ├── Step 2: Notion → Query inbox database
    │   ├── Step 3: Notion → Get agent reports
    │   ├── Step 4: AI Step → Compile briefing (use Xavier's voice)
    │   └── Step 5: Gmail → Send to JD
    │
    ├── WORKFLOW: Priority Triage
    │   ├── Trigger: New item in Notion inbox
    │   ├── Step 1: AI Step → Categorize and prioritize
    │   ├── Step 2: Path → Route by urgency
    │   └── Step 3: Notion → Update status
    │
    └── WORKFLOW: Calendar Sync
        ├── Trigger: Every 30 minutes
        ├── Step 1: Google Calendar → Check for conflicts
        ├── Step 2: AI Step → Identify issues
        └── Step 3: If conflict → Alert via email
```

### Key Difference from Previous Model

**Before (Mini AI Agents within workflows):**
- One workflow with an AI Agent step that calls Actions

**Now (Agents own multiple Workflows):**
- Agent is a first-class entity on the dashboard
- Agent owns multiple full workflows
- Each workflow has its own trigger and steps
- Chat with the Agent to create new workflows

---

## Building Hivefind Agents in Relay.app

### Step 1: Create the Agent

1. Go to your Relay.app dashboard
2. Click **"Create Agent"** in the Agents section
3. Give your Agent a name (e.g., "Xavier - Chief of Staff")
4. Add a description of the Agent's responsibilities

### Step 2: Create Workflows for the Agent

Each "Core Responsibility" from the Hivefind spec becomes a **Workflow** owned by the Agent.

| Agent | Workflows to Create |
|-------|---------------------|
| Xavier | Daily Briefing, Priority Triage, Calendar Sync |
| Aurelius | Weekly Reflection, Charter Breach Monitor |
| Eleanor | Relationship Event Handler, Weekly Pulse |
| Warren | Daily Financial Scan, Monthly Report |
| Ada | Daily Content Publish, Trend Research, Weekly Report |
| Clara | Email Response, Returns Processing, Weekly Digest |
| etc. | ... |

### Step 3: Build Each Workflow

For each Workflow:

1. **Add a Trigger** (schedule, webhook, or app event)
2. **Add Steps** using integrations (Notion, Gmail, Google Calendar, etc.)
3. **Use AI Steps** for intelligence (include the Agent's voice/personality from the spec)
4. **Move the Workflow** to be owned by your Agent

**Example: Aurelius Weekly Reflection Workflow**

```
WORKFLOW: Weekly Reflection
├── Trigger: Schedule (Sunday 7:00 PM)
├── Step 1: Notion → Query week's completed tasks
├── Step 2: Notion → Query week's calendar events
├── Step 3: Notion → Get charter principles
├── Step 4: AI Step → "As Aurelius, analyze alignment and generate reflection"
├── Step 5: Notion → Save reflection document
└── Step 6: Gmail → Email reflection to JD
```

### Step 4: Use the Agent Chat

Once your Agent has workflows, you can use the **Chat interface** to:
- Ask the Agent to create new workflows
- (Coming soon) Ask about past work
- (Coming soon) Give feedback to improve the Agent

### Moving Existing Workflows to an Agent

If you already have standalone workflows:
1. **From Workspace view**: Right-click workflow → "Move to Agent" → Select Agent
2. **From Workflow Editor**: Click [...] menu → "Move to Agent"

---

## AI Model Selection

Relay.app supports multiple AI models:

| Model | Best For | Notes |
|-------|----------|-------|
| **GPT-4o** | General purpose, included in plans | Default recommendation |
| **GPT-4.5** | Complex reasoning | Higher cost |
| **Claude** | Long context, nuanced responses | Good for detailed specs |
| **Gemini 2.0** | Fast, cost-effective | Good for simple tasks |
| **LLaMA** | Self-hosted option | For privacy-sensitive |

**Recommendation:** Start with GPT-4o (included), then optimize based on performance.

---

## Capabilities and Limitations

### What Relay.app Agents CAN Do:
- **Own multiple workflows** with different triggers
- **Chat interface** to create new workflows
- **Activity calendar** showing busy days and completed runs
- Access 100+ app integrations
- Include human-in-the-loop steps for approvals
- Use paths and conditions for complex logic
- Run on schedules or in response to events

### What Relay.app Agents CANNOT Do (Currently):
- Run continuously (workflows activate on triggers)
- Remember across workflow runs (use Notion for state)
- Communicate with other agents directly (use shared Notion databases)
- Access arbitrary APIs without integration setup

### Coming Soon (Per Relay.app Roadmap):
- Chat about past work
- Ask Agent about its knowledge
- Give feedback to improve Agent
- Send one-off automation requests
- Agent templates

### Coordination Between Agents

Hivefind agents coordinate through **shared Notion databases**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     AGENT COORDINATION LAYER                             │
└─────────────────────────────────────────────────────────────────────────┘

   Xavier                    Notion Databases                    Aurelius
   ──────                    ────────────────                    ────────
      │                                                              │
      │     ┌─────────────────────────────────────────────┐          │
      │     │                                             │          │
      ├────▶│  📋 Daily Briefings                         │◀─────────┤
      │     │  📊 Agent Reports                           │          │
      │     │  🎯 Active Priorities                       │          │
      │     │  📝 Charter Principles                      │          │
      │     │  ⚠️ Escalation Queue                        │          │
      │     │                                             │          │
      │     └─────────────────────────────────────────────┘          │
      │                          ▲                                   │
      │                          │                                   │
      │           ┌──────────────┼──────────────┐                    │
      │           │              │              │                    │
   Eleanor    Warren         Martha         Seneca              All Agents
```

---

## Recommended Implementation Order

### Phase 1: Foundation (Week 1)
1. Set up Notion workspace with shared databases
2. Build Xavier (Chief of Staff) - central coordinator
3. Build Aurelius (Accountability) - charter alignment
4. Test coordination between Xavier and Aurelius

### Phase 2: Personal Domain (Weeks 2-3)
5. Build personal agents in order of priority
6. Connect to Xavier for daily briefings
7. Test escalation flows to Aurelius

### Phase 3: Business Domains (Weeks 4-5)
8. Build Haze Gray agents (Helena, Cicero, Dale, Hamilton)
9. Build Puzzlehouse agents (Ada, Franklin, Clara)
10. Test domain-specific workflows

### Phase 4: Optimization (Ongoing)
11. Tune prompts based on output quality
12. Add/remove actions based on usage
13. Optimize model selection per workflow

---

## Quick Reference: Building in Relay.app

### Creating a New Agent Workflow

1. **New Workflow** → Name it (e.g., "Xavier Daily Briefing")
2. **Add Trigger** → Schedule, Webhook, or App trigger
3. **Add AI Step** → Select "AI Agent" from AI menu
4. **Write Prompt** → Paste from Hivefind spec system prompt
5. **Add Actions** → Build mini-workflows for each responsibility
6. **Test** → Run with sample data
7. **Deploy** → Set live

### Action Building Pattern

```
For each Core Responsibility in the Hivefind spec:
  1. Create an Action with descriptive name
  2. Add integration steps (Notion, Gmail, etc.)
  3. Add AI steps for processing/formatting
  4. Add output step (save, send, notify)
  5. Test the action independently
  6. Connect to the agent
```

---

## Sources & Documentation

- [Relay.app Documentation](https://docs.relay.app/)
- [AI Steps Guide](https://docs.relay.app/ai/ai-steps)
- [Agentic Tool Use](https://docs.relay.app/ai/agentic-tool-use)
- [Prompt Tips](https://docs.relay.app/ai/prompt-tips)
- [How to Build an AI Agent on top of your CRM](https://www.relay.app/blog/how-to-build-an-ai-agent-on-top-of-your-crm)

---

*Document Version: 1.0*
*Created: December 2024*
*Status: Reference Guide*
