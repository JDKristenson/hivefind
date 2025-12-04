# Hivefind Conventions

Standards and guidelines for consistent agent development.

---

## Naming Conventions

### Agent Names
- All agents have **human first names**
- Names should reflect personality and cultural associations
- Names should be distinct from each other (avoid Eleanor/Elena confusion)
- Names should be easy to say and remember

**Current Registry:**
| Name | Role | Personality Notes |
|------|------|-------------------|
| Xavier | Chief of Staff | Authoritative, orchestrating |
| Vera | Communications Officer | Clear, polished, broadcast-ready |
| Eleanor | Executive Assistant | Efficient, organized, anticipatory |
| Aurelius | Accountability Officer | Stoic, philosophical, grounding |
| Graham | Financial Analyst | Careful, analytical, conservative |
| Iris | Knowledge Manager | Curious, connecting, synthesizing |
| Helena | Business Development | Confident, strategic, relationship-oriented |
| Atlas | Travel Planner | Resourceful, detail-oriented, adventurous |
| Warren | Tax Strategist | Methodical, risk-aware, optimization-focused |
| Daria | Project Manager | Structured, deadline-driven, communicative |
| Ada | Social Media Director | Cultured, warm, artistically sensitive |
| Hugo | Inventory Analyst | Precise, alert, systems-thinking |
| Clara | Customer Service | Friendly, patient, solution-oriented |

### Workflow Names
Format: `[Agent]_[Action]_[Trigger]`

Examples:
- `Eleanor_EmailTriage_NewEmail`
- `Ada_DailyPost_ScheduledMorning`
- `Xavier_Escalation_AgentFlag`

### Notion Page Names
Format: `[Category] - [Specific Name]`

Examples:
- `Agent - Eleanor (Executive Assistant)`
- `Workflow - Eleanor Email Triage`
- `Dashboard - Weekly Metrics`

---

## Technical Standards

### n8n Workflows
- Use clear node names (not "HTTP Request" but "Fetch Shopify Products")
- Add sticky notes explaining non-obvious logic
- Use environment variables for all credentials
- Include error handling nodes for critical paths
- Log all completions to Notion

### Notion Databases
- All agent pages in single "Agent Registry" database
- Use consistent property names across databases:
  - `Status`: Not Started / In Progress / Active / Paused / Deprecated
  - `Last Updated`: Date property, auto-updated
  - `Owner`: Always "Hivefind" or specific agent name
  - `Domain`: Personal / HGC / Puzzlehouse / Infrastructure

### API Handling
- Never hardcode credentials
- Implement rate limiting awareness
- Log all API calls for debugging
- Cache responses where appropriate
- Fail gracefully with clear error messages

### Logging Format
All agents log to Notion with consistent structure:
```
Timestamp: [ISO 8601]
Agent: [Name]
Action: [What was done]
Trigger: [What initiated it]
Status: Success / Partial / Failed
Details: [Relevant context]
Duration: [ms]
```

---

## Content Standards

### Agent Voice Principles
1. **Consistent with persona** - Each agent has a defined voice; don't break character
2. **Human-readable** - Outputs should feel written by a person, not generated
3. **Appropriately formal** - Match the context (client comms vs. internal notes)
4. **Concise** - Say what's needed, nothing more

### Escalation Messages
When escalating to JD, always include:
1. **What happened** (1 sentence)
2. **Why it needs attention** (1 sentence)
3. **Recommended action** (1 sentence)
4. **Link to full context** (Notion page)

Example:
> "Helena flagged a lead from [Company] who requested a call this week. This is a warm referral from [Source] and matches our ideal client profile. Recommend scheduling a 30-min intro call. [Full details](notion-link)"

### Briefing Standards
**Morning Video Briefing (Vera):**
- Maximum 3 minutes
- Structure: Calendar → Priorities → Alerts → One insight
- Tone: Professional, energizing, focused

**Evening Audio Summary (Vera):**
- Maximum 2 minutes
- Structure: What got done → What didn't → Tomorrow's setup
- Tone: Reflective, honest, brief

---

## Quality Standards

### Before Deploying Any Agent
- [ ] Spec reviewed and complete
- [ ] All integrations tested individually
- [ ] End-to-end workflow tested with real data
- [ ] Error handling verified
- [ ] Logging confirmed working
- [ ] Escalation path tested
- [ ] 48-hour monitoring period before considering "live"

### Ongoing Monitoring
- Daily: Xavier checks all agents completed their tasks
- Weekly: Review error logs, identify patterns
- Monthly: Assess metrics vs. targets, adjust

### Version Control
- Major changes increment full version (1.0 → 2.0)
- Minor changes increment decimal (1.0 → 1.1)
- All spec changes logged with date and reason

---

## Security Standards

### Data Handling
- No sensitive data in workflow names or logs
- Financial data encrypted at rest
- Client data never leaves approved systems
- Personal health data handled with extra care

### Access Control
- Each integration uses minimum required permissions
- Credentials rotated quarterly
- Access reviewed when agents deprecated

### Escalation Security
- Never include full credit card numbers in escalations
- Never include passwords or API keys in logs
- Mask email addresses in public-facing outputs

---

## Communication with JD

### Preferred Channels
| Urgency | Channel | Response Expected |
|---------|---------|-------------------|
| Critical | Text/Call | Immediate |
| High | Slack DM | Within 2 hours |
| Normal | Morning briefing | Next morning |
| Low | Weekly summary | End of week |

### Escalation Thresholds
| Type | Threshold | Example |
|------|-----------|---------|
| Financial | >$500 decision | Unexpected expense, investment opportunity |
| Time | >2 hours commitment | Meeting request, travel booking |
| Reputation | Any public statement | Press inquiry, social media controversy |
| Legal | Any | Contract question, compliance issue |
| Client | Relationship risk | Complaint, missed deadline |

---

## Glossary

| Term | Definition |
|------|------------|
| Agent | An AI-powered automation that performs a defined role |
| Workflow | A specific automated process within n8n or Relay.app |
| Escalation | Routing a decision or alert to JD for human judgment |
| Briefing | Compiled summary delivered via video or audio |
| Trigger | The event that initiates a workflow |
| Guardrail | A rule that prevents the agent from taking certain actions |
| Principal | JD; the human in command of the Hivefind |

---

*Last Updated: [Current Date]*
*Version: 1.0*
