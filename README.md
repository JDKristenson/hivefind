# Hivefind

A coordinated ecosystem of 19 AI agents handling personal operations, consulting business, and e-commerce through specialized roles and clear accountability chains.

## What Is This?

This repository contains the "job descriptions" for an AI agent fleet. Each agent has a defined personality, responsibilities, decision authority, and coordination protocols. Think of it as an org chart and employee handbook, but for AI.

**Why share this?** To demonstrate a framework for designing AI agents that work together rather than in isolation. The patterns here (naming conventions, escalation paths, domain clustering, separation of concerns) are transferable to other contexts.

## The Team

### Coordination Layer (3 agents)
The management team that keeps everything running smoothly.

| Agent | Title | Role |
|-------|-------|------|
| **Xavier** | Chief of Staff | Routes work, monitors agent health, handles cross-agent coordination |
| **Clare** | Communications Officer | Compiles briefings, coaches content delivery |
| **Aurelius** | Keeper of the Charter | Maintains accountability, flags values conflicts |

### Personal Staff (10 agents)
Managing life logistics, health, finances, relationships, learning, and institutional memory.

| Agent | Title | Role |
|-------|-------|------|
| **Evelyn (EA)** | Executive Assistant | Email triage, calendar management, meeting prep |
| **Evelyn (Memory)** | Memory Curator | Knowledge curation, consolidation, context serving |
| **Eleanor** | Relationship Steward | CRM, network cultivation, relationship maintenance |
| **Warren** | Chief Financial Steward | Finance oversight, investments, projections |
| **Hetty** | Tax Strategist | Tax optimization, expense categorization (reports to Warren) |
| **Galen** | Chief Health Officer | Biometrics correlation, health pattern recognition |
| **Martha** | Keeper of the Realm | Household operations, maintenance, family logistics |
| **Marco** | Chief Travel Officer | Travel planning, loyalty programs, logistics |
| **Seneca** | Chief Learning Officer | Curriculum design, focus protection, skill building |
| **Iris** | Chief Knowledge Officer | Knowledge synthesis, information retrieval |

### Haze Gray Consulting (4 agents)
Running the consulting business pipeline and delivery.

| Agent | Title | Role |
|-------|-------|------|
| **Helena** | Business Development Manager | Lead generation, opportunity qualification |
| **Cicero** | Chief Persuasion Officer | Proposals, pitches, speaking preparation |
| **Dale** | Content Strategist | LinkedIn, newsletter, thought leadership content |
| **Hamilton** | Engagement Manager | Client delivery operations, commitment tracking |

### Puzzlehouse.com (3 agents)
Operating the e-commerce puzzle store.

| Agent | Title | Role |
|-------|-------|------|
| **Ada** | Social Media Director | Social content creation across platforms |
| **Franklin** | Store Operations Manager | Shopify ops, inventory, vendor relations |
| **Clara** | Customer Service Representative | Customer support (reports to Franklin) |

## Repository Structure

```
hivefind/
├── README.md                 # You are here
├── docs/                     # Architecture and project documentation
│   ├── ARCHITECTURE.md       # Conceptual design, org chart, information flows
│   ├── SYSTEM_ARCHITECTURE.md # Technical three-layer architecture
│   ├── AGENT_ROSTER.md       # Canonical list of all 19 agents
│   ├── BUILD_PLAN.md         # Implementation roadmap
│   ├── CONVENTIONS.md        # Naming and formatting standards
│   ├── AGENTS_MD_CONVERSION_GUIDE.md  # Spec formatting guide
│   └── PROJECT_INSTRUCTIONS.md        # Original project brief
├── specs/                    # Individual agent specifications
│   ├── coordination/         # Xavier, Clare, Aurelius
│   ├── personal/             # Evelyn, Eleanor, Warren, Hetty, Galen,
│   │                         # Martha, Marco, Seneca, Iris
│   ├── haze-gray/            # Helena, Cicero, Dale, Hamilton
│   └── puzzlehouse/          # Ada, Franklin, Clara
├── templates/                # Blank templates for new agents
│   └── AGENT_SPEC_TEMPLATE.md
├── updates/                  # Applied spec updates (historical reference)
├── automations/              # n8n workflows and persona assets
│   ├── README.md             # Automation catalog and setup overview
│   ├── N8N_SETUP.md          # Complete n8n setup guide
│   ├── n8n/                  # 50 n8n workflow JSON files
│   │   ├── coordination/     # Xavier, Clare, Aurelius workflows
│   │   ├── personal/         # Personal domain agent workflows
│   │   ├── haze-gray/        # Haze Gray Consulting workflows
│   │   ├── puzzlehouse/      # Puzzlehouse.com workflows
│   │   ├── integrations/     # Cross-platform workflows
│   │   ├── tools/            # API tool workflows
│   │   └── production/       # Voice/video/music production
│   └── personas/             # Agent personification assets
│       ├── voice-profiles/   # ElevenLabs voice configs
│       ├── video-avatars/    # Runway Characters avatar configs
│       ├── theme-music/      # Suno music prompts
│       └── visual-identity/  # Agent branding
├── process/                  # How this was built (for demos, courses, content)
│   ├── 01-JOURNEY.md         # Timeline from concept to implementation
│   ├── 02-DESIGN-DECISIONS.md # Key choices and rationale
│   ├── 03-SPEC-WRITING.md    # How specs were developed
│   ├── 04-LESSONS-LEARNED.md # What worked, what didn't
│   ├── 05-CLIENT-DEMO.md     # Talking points for presentations
│   └── 06-AUTOMATION-BUILD.md # How the automations were built
├── org/                      # Organizational infrastructure (HR/IT)
│   ├── PROTOCOLS.md          # Hierarchy, communication, conflict resolution
│   ├── ONBOARDING.md         # New agent checklist
│   ├── OFFBOARDING.md        # Agent removal checklist
│   ├── ORG_CHART.md          # Mermaid diagrams
│   └── ORG_CHART.excalidraw  # Editable visual org chart
└── notion/                   # Notion database files (ready for import)
    ├── README.md             # Import instructions and setup guide
    ├── Agent_Registry.csv    # Master roster of all 19 agents
    ├── Activity_Log.csv      # Agent activity logging template
    ├── Exception_Queue.csv   # Issues requiring human review
    └── Exception_Types.csv   # Configurable exception categories
```

## Agent Spec Format

Each agent specification follows a consistent structure:

1. **Identity** - Name, title, namesake, domain, reporting relationships
2. **Mission Statement** - One-sentence purpose in the agent's voice
3. **Personality** - How the agent communicates and approaches problems
4. **Problem Definition** - What pain point the agent addresses
5. **Core Responsibilities** - Specific duties with triggers, actions, outputs
6. **Workflow Diagram** - Visual representation of the agent's operating loop
7. **Technical Requirements** - Integrations, data needs, AI capabilities
8. **Decision Framework** - What the agent can do autonomously vs. escalate
9. **Success Metrics** - How to measure effectiveness
10. **Constraints & Guardrails** - Boundaries and rules
11. **Sample Outputs** - Examples of what the agent produces

## Key Design Principles

**Coordination Before Chaos** - Xavier routes all work; agents don't operate in silos.

**Separation of Content and Delivery** - Dale creates content; Clare coaches presentation; human publishes.

**Domain Clustering** - Agents grouped by shared context (personal, business, e-commerce).

**Escalation by Exception** - Agents handle routine work autonomously; escalate only decisions beyond authority, high-stakes items, or novel situations.

**Observable Operations** - Every agent logs activity for debugging and accountability.

**Single Source of Truth** - One agent owns each domain. No overlapping authority.

## Naming Convention

All agents are named after historical figures, mythological characters, or notable individuals whose attributes match the agent's role:

- **Warren** (Buffett) for finance
- **Cicero** for persuasion
- **Marco** (Polo) for travel
- **Clara** (Barton) for customer care
- And so on...

This makes agents memorable and their roles intuitive.

## System Architecture

Hivefind operates on a three-layer model:

| Layer | Purpose | Tool |
|-------|---------|------|
| **Human Interface** | Your cockpit; status, decisions, exceptions | Notion |
| **Orchestration** | Routing, triggers, execution, coordination | Notion AI Agents (primary), n8n (gap-filler) |
| **Data Layer** | Persistent storage, logs, historical record | Notion databases |

See [SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) for full technical details.

## Technology Stack

| Layer | Tools |
|-------|-------|
| Orchestration | Notion AI Agents (primary), n8n/Relay.app (gap-filler) |
| Data Hub | Notion |
| AI Models | Claude (primary) |
| Voice | ElevenLabs |
| Video | Runway Characters |
| Finance | QuickBooks Online |
| CRM | Clay |
| E-commerce | Shopify |
| Calendar/Email | Google Workspace |

## Status

All 19 agent specifications are complete and documented.

**Automations:** 50 n8n workflows built and ready for deployment:
- 10 coordination layer workflows
- 12 personal domain workflows
- 4 Haze Gray domain workflows
- 8 Puzzlehouse domain workflows
- 6 cross-platform integration workflows
- 6 API tool workflows
- 4 voice/video production workflows

**Persona Assets:** 12 configuration files for agent personification:
- Voice profiles for 7 agents (ElevenLabs)
- Video avatars for 3 agents (Runway Characters)
- Theme music prompts for all 19 agents (Suno)
- Visual identity for all 19 agents

See [automations/README.md](automations/README.md) for the full catalog and setup instructions.

## How This Was Built

Want to understand the process behind designing an AI workforce? The [`process/`](process/) folder documents:
- The journey from concept to 19 agents
- Key design decisions and their rationale
- The spec-writing methodology
- Lessons learned along the way
- Talking points for client demos

This material is useful for anyone wanting to replicate the approach or understand the thinking behind the system.

## License

This is a personal project shared for educational purposes. Feel free to use the patterns and frameworks as inspiration for your own AI agent designs.

---

*Questions? The agent specs themselves are the best documentation. Start with [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the big picture, then dive into individual specs.*
