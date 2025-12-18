# Relay.app Agent Builder Template

This template provides the standard format for creating Hivefind agents in Relay.app.

---

## How to Use This Template

When building an agent in Relay.app's Agent Builder:

1. **Name**: Use the agent's first name (e.g., "Xavier")
2. **Description**: Copy from the "Agent Description" section
3. **System Prompt**: Copy the entire "System Prompt Block"
4. **Triggers**: Configure as listed in "Trigger Configuration"
5. **Tools/Integrations**: Enable the listed connections
6. **Test**: Run the test scenarios provided

---

## Template Structure

Each agent spec in `/agents/` follows this structure:

```markdown
# [Agent Name] - Relay.app Build Guide

## Quick Reference
- **Name**: [First name]
- **Full Title**: [Title from main spec]
- **Domain**: [coordination/personal/haze-gray/puzzlehouse]
- **Named For**: [Historical figure]
- **Reports To**: [Supervisor agent or "User"]
- **Supervises**: [List or "None"]

---

## SECTION 1: AGENT BUILDER PASTE BLOCK

### Agent Name
[Paste this into the Name field]

### Agent Description
[Paste this into the Description field]

### System Prompt
[Paste this entire block into the System Prompt field]

---

## SECTION 2: TRIGGER CONFIGURATION

### Primary Triggers
[List of triggers to configure]

### Webhook Setup (if applicable)
[Webhook configuration details]

### Schedule Setup (if applicable)
[Cron/schedule configuration]

---

## SECTION 3: INTEGRATIONS & TOOLS

### Required Integrations
[List of Relay.app integrations to enable]

### API Connections
[External APIs needed]

### Data Sources
[Notion databases, etc.]

---

## SECTION 4: WORKFLOW CONNECTIONS

### Upstream Agents
[Agents that trigger this one]

### Downstream Agents
[Agents this one triggers]

### Handoff Protocol
[How to pass data between agents]

---

## SECTION 5: TEST SCENARIOS

### Test Case 1: [Name]
**Input**: [Test input]
**Expected Output**: [What should happen]
**Verify**: [How to confirm success]

### Test Case 2: [Name]
[Additional test cases]

---

## SECTION 6: TROUBLESHOOTING

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| [Problem] | [Why] | [Fix] |

### Debug Checklist
- [ ] Check item 1
- [ ] Check item 2
- [ ] Check item 3

---

## SECTION 7: SAMPLE OUTPUTS

### Example 1: [Scenario]
[Sample agent output]

### Example 2: [Scenario]
[Sample agent output]
```

---

## Relay.app-Specific Considerations

### Agent Builder Fields

| Field | What to Enter | Source |
|-------|---------------|--------|
| Name | Agent first name | Quick Reference |
| Description | 1-2 sentence summary | Agent Description |
| System Prompt | Full persona + instructions | System Prompt Block |
| Model | claude-3-5-sonnet (recommended) | Standard |
| Temperature | 0.7 (default) or as specified | Per agent |

### Integration Mapping

| Hivefind Integration | Relay.app Equivalent |
|---------------------|---------------------|
| Gmail | Google Gmail integration |
| Google Calendar | Google Calendar integration |
| Notion | Notion integration |
| Slack | Slack integration |
| Shopify | Shopify integration |
| LinkedIn | LinkedIn integration |
| Custom API | HTTP Request node |

### Trigger Types in Relay.app

| Trigger Type | Use Case | Configuration |
|--------------|----------|---------------|
| Schedule | Timed jobs (briefings, checks) | Cron expression |
| Webhook | External events | Webhook URL |
| Manual | User-initiated | Button/command |
| Agent Output | Chain from another agent | Agent connection |

---

## Quality Checklist Before Deployment

- [ ] Agent name matches Hivefind roster
- [ ] System prompt captures full persona
- [ ] All required integrations connected
- [ ] Triggers configured correctly
- [ ] Test scenarios pass
- [ ] Escalation paths defined
- [ ] Logging to Notion Activity Log enabled
- [ ] Error handling configured
