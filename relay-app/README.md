# Hivefind Relay

**A Relay.app Implementation of the Hivefind Agent Ecosystem**

This is the Relay.app-specific fork of the Hivefind project, designed to leverage Relay.app's agent builder and workflow automation platform.

## Project Name: Hivefind Relay

This implementation maintains the same 18 agents with identical personas, names, and responsibilities as the main Hivefind project, but with build instructions optimized for Relay.app's:
- Agent Builder interface
- Workflow Builder nodes
- Native integrations
- Trigger system

## Directory Structure

```
relay-app/
├── README.md                    # This file
├── templates/
│   ├── AGENT_BUILDER_TEMPLATE.md    # Standard format for agent creation
│   └── WORKFLOW_TEMPLATE.md         # Standard format for workflows
├── agents/
│   ├── coordination/            # Xavier, Clare, Aurelius, Evelyn (Memory)
│   ├── personal/               # Evelyn (EA), Eleanor, Warren, Hetty, Galen, Martha, Marco, Seneca, Iris
│   ├── haze-gray/              # Helena, Cicero, Dale, Hamilton
│   └── puzzlehouse/            # Ada, Franklin, Clara
├── workflows/                   # Workflow builder configurations
└── troubleshooting/            # Node-by-node debugging guides
```

## Agent Roster (18 Agents)

### Coordination Layer (4)
| Agent | Role | Relay Status |
|-------|------|--------------|
| Xavier | Chief of Staff | Ready to Build |
| Clare | Chief Communications Officer | Ready to Build |
| Aurelius | Keeper of the Charter | Ready to Build |
| Evelyn | Memory Curator | Ready to Build |

### Personal Staff (9)
| Agent | Role | Relay Status |
|-------|------|--------------|
| Evelyn | Executive Assistant | Ready to Build |
| Eleanor | Relationship Steward | Ready to Build |
| Warren | Chief Financial Steward | Ready to Build |
| Hetty | Tax Strategist | Ready to Build |
| Galen | Chief Health Officer | Ready to Build |
| Martha | Keeper of the Realm | Ready to Build |
| Marco | Chief Travel Officer | Ready to Build |
| Seneca | Chief Learning Officer | Ready to Build |
| Iris | Chief Knowledge Officer | Ready to Build |

### Haze Gray Consulting (4)
| Agent | Role | Relay Status |
|-------|------|--------------|
| Helena | Business Development Manager | Ready to Build |
| Cicero | Chief Persuasion Officer | Ready to Build |
| Dale | Content Strategist | Ready to Build |
| Hamilton | Engagement Manager | Ready to Build |

### Puzzlehouse.com (3)
| Agent | Role | Relay Status |
|-------|------|--------------|
| Ada | Social Media Director | Ready to Build |
| Franklin | Store Operations Manager | Ready to Build |
| Clara | Customer Service Representative | Ready to Build |

## How to Use This Documentation

### Building an Agent in Relay.app

1. Open the agent's spec file from `/agents/[domain]/[AgentName].md`
2. Copy the **Agent Builder Paste Block** section
3. Paste into Relay.app's Agent Builder
4. Configure the triggers as specified
5. Connect the integrations listed
6. Test with the provided test scenarios

### Building Workflows

1. Open the workflow file from `/workflows/`
2. Follow the node-by-node instructions
3. Use the troubleshooting guide if issues arise

## Key Differences from Main Hivefind

| Aspect | Main Hivefind | Hivefind Relay |
|--------|---------------|----------------|
| Orchestration | n8n (self-hosted) | Relay.app (cloud) |
| Complexity | Full enterprise | Streamlined for Relay |
| Memory Layer | Pinecone + Notion | Relay.app native + Notion |
| Setup Time | Days | Hours |

## Build Order (Recommended)

1. **Phase 1**: Xavier (coordination foundation)
2. **Phase 2**: Clare (communications)
3. **Phase 3**: Evelyn EA (personal foundation)
4. **Phase 4**: Aurelius (accountability)
5. **Phase 5**: Remaining agents by domain priority

---

*Hivefind Relay - Same agents, same personas, built for Relay.app*
