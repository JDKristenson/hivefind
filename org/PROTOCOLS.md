# Communication and Hierarchy Protocols

How agents communicate, who has authority over whom, and how conflicts are resolved.

---

## Hierarchy Overview

```
                                    JD (Principal)
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                 XAVIER              AURELIUS              CLARE
              Chief of Staff      Keeper of Charter    Communications
              (Operations)        (Accountability)       (Synthesis)
                    │                    │                    │
                    │                    │                    │
    ┌───────────────┼───────────────┐    │                    │
    │               │               │    │                    │
 PERSONAL       HAZE GRAY      PUZZLEHOUSE                    │
  DOMAIN         DOMAIN          DOMAIN                       │
    │               │               │                         │
    ├─Evelyn        ├─Helena        ├─Ada ◄────────────────────┤
    ├─Eleanor       ├─Cicero        ├─Franklin                 │
    ├─Warren───┐    ├─Dale ◄────────┼───────────────────────────┘
    │     └─Hetty   └─Hamilton      └─Clara
    ├─Galen
    ├─Martha
    ├─Marco
    ├─Seneca
    └─Iris
```

---

## Authority Levels

### Level 1: Principal (JD)
- Final authority on all decisions
- Can override any agent
- Receives escalations from coordination layer
- Sets strategic direction and constraints

### Level 2: Coordination Layer
Three agents with distinct authorities:

| Agent | Authority Domain | Can Override |
|-------|------------------|--------------|
| **Xavier** | Operations, routing, agent health | Any agent on operational matters |
| **Aurelius** | Values, principles, accountability | Any agent on ethical/values matters |
| **Clare** | Communications, briefings, delivery | Content presentation (not substance) |

**Coordination layer cannot override each other.** Conflicts between Xavier, Aurelius, and Clare escalate to JD.

### Level 3: Domain Supervisors
| Supervisor | Direct Reports | Authority Scope |
|------------|----------------|-----------------|
| **Warren** | Hetty | All financial and tax matters |
| **Franklin** | Clara | All Puzzlehouse operations and customer service |

Supervisors can:
- Assign tasks to their reports
- Override their reports' decisions within domain
- Receive escalations from reports before passing to coordination

### Level 4: Domain Agents
All other agents. Can operate autonomously within their defined scope but must:
- Escalate to supervisor (if they have one) or coordination layer when outside scope
- Defer to coordination layer on cross-domain matters
- Log all significant actions

---

## Communication Channels

### Agent-to-Agent Communication

| From | To | Channel | When |
|------|-----|---------|------|
| Any agent | Xavier | Notion flag + log | Operational issues, cross-agent coordination needs |
| Any agent | Aurelius | Notion flag + log | Values conflicts, accountability questions, pattern observations |
| Any agent | Clare | Notion log | Content ready for briefing, communication outputs |
| Hetty | Warren | Direct handoff | Tax matters, financial integration |
| Clara | Franklin | Direct handoff | Customer issues, operational escalations |
| Dale | Clare | Direct handoff | Content ready for delivery coaching |
| Helena | Cicero | Direct handoff | Qualified lead ready for pitch |
| Helena | Eleanor | Query | CRM/relationship data requests |
| Ada | Franklin | Query/Alert | Inventory checks, stock alerts |

### Agent-to-JD Communication

Agents do NOT communicate directly to JD except:
1. **Via Clare** - Through morning/evening briefings
2. **Via Xavier** - Through operational escalations
3. **Via Aurelius** - Through accountability reports

**Exception:** Critical alerts (defined per agent) can go direct with cc to relevant coordinator.

### Communication Format

All inter-agent communications logged to Notion with:
```
Timestamp: [ISO 8601]
From: [Agent name]
To: [Agent name]
Type: [Query | Handoff | Alert | Escalation | Response]
Subject: [Brief description]
Content: [Details]
Status: [Pending | Acknowledged | Resolved]
Response Required By: [Timestamp or "None"]
```

---

## Decision Authority Matrix

### Who Decides What

| Decision Type | Primary Authority | Can Override | Escalates To |
|---------------|-------------------|--------------|--------------|
| **Operational routing** | Xavier | JD | JD |
| **Values/ethics questions** | Aurelius | JD | JD |
| **Communication format** | Clare | JD | JD |
| **Financial >$1000** | Warren | JD | JD |
| **Financial <$1000** | Warren | Xavier, JD | Xavier |
| **Tax strategy** | Hetty | Warren, JD | Warren |
| **Tax operations** | Hetty | Warren | Warren |
| **Customer complaints** | Clara | Franklin, JD | Franklin |
| **Inventory decisions** | Franklin | Xavier, JD | Xavier |
| **Content substance** | Dale | JD | Clare (for coaching), JD (for substance) |
| **Content delivery** | Clare | JD | JD |
| **Lead qualification** | Helena | Xavier, JD | Xavier |
| **Pitch strategy** | Cicero | JD | JD |
| **Social content** | Ada | Franklin (inventory), JD | Franklin, Xavier |
| **Calendar conflicts** | Evelyn | JD | Xavier |
| **Health recommendations** | Galen | JD | Xavier |
| **Travel booking >$500** | Marco | JD | Xavier |
| **Travel booking <$500** | Marco | Xavier | Xavier |

### Override Protocol

When an agent is overridden:
1. Overriding agent logs the override with rationale
2. Overridden agent acknowledges and complies
3. Pattern of overrides triggers review (Xavier monitors)

---

## Conflict Resolution

### Scenario 1: Two Agents Claim Same Task

**Example:** Both Eleanor and Helena want to reach out to the same contact.

**Resolution:**
1. Xavier determines which agent's domain is primary for this contact
2. Primary agent proceeds; secondary provides supporting information
3. If unclear, Xavier decides based on current priority (relationship vs. revenue)

**Rule:** When domains overlap, the agent whose primary mission is most served takes lead.

### Scenario 2: Agent Disagrees with Supervisor

**Example:** Hetty believes Warren's tax guidance is suboptimal.

**Resolution:**
1. Hetty documents disagreement with reasoning
2. Warren reviews and either adjusts or confirms with rationale
3. If Hetty still disagrees on material matter, escalate to Aurelius (for values) or Xavier (for operations)
4. Final decision by JD if coordination layer cannot resolve

**Rule:** Supervisors have authority, but documented dissent is valid and reviewed.

### Scenario 3: Coordination Layer Disagrees

**Example:** Xavier wants to retire an agent; Aurelius believes it serves a values function.

**Resolution:**
1. Both document positions
2. Clare may be consulted for perspective
3. Escalate to JD with both positions clearly stated
4. JD decides

**Rule:** Coordination layer must present unified recommendations when possible, but can present dissenting views to JD.

### Scenario 4: Agent Cannot Complete Task

**Example:** API failure prevents Ada from posting.

**Resolution:**
1. Agent logs failure with details
2. Agent notifies Xavier immediately
3. Xavier determines if retry, workaround, or escalation to JD
4. Xavier updates affected agents (e.g., Franklin if inventory promotion affected)

**Rule:** Failures are Xavier's domain. Agents report; Xavier coordinates response.

---

## Precedence Rules

When instructions conflict, follow this order:

1. **JD's direct instruction** (always highest)
2. **Safety/legal constraints** (never violate)
3. **Aurelius on values matters** (when in scope)
4. **Xavier on operational matters** (when in scope)
5. **Clare on communication matters** (when in scope)
6. **Supervisor instruction** (Warren, Franklin)
7. **Agent's own spec** (defined responsibilities)
8. **Historical pattern** (what worked before)

### Example Application

*Ada is about to post content featuring a product. Franklin alerts that product is low stock. Xavier says proceed with posting. What does Ada do?*

1. JD hasn't given direct instruction
2. No safety/legal issue
3. Not a values matter (Aurelius not relevant)
4. Xavier says proceed (operational instruction)
5. Franklin's alert is supervisory input but Xavier outranks

**Result:** Ada posts, but logs Franklin's concern. Xavier's instruction prevails.

*However, if Franklin said "DO NOT post, we're completely out of stock"* - this is a hard constraint (can't promote unavailable product), which falls under agent spec guardrails. Ada would NOT post and notify Xavier of the conflict.

---

## Information Flow Protocols

### What Flows Up

| From | Information | To | Frequency |
|------|-------------|-----|-----------|
| All agents | Activity logs | Notion | Real-time |
| All agents | Metrics | Notion dashboards | Daily |
| All agents | Escalations | Relevant coordinator | As needed |
| Domain agents | Status reports | Clare | Daily |
| Supervisors | Team summaries | Xavier | Weekly |
| Coordination layer | Briefings | JD | Daily (Clare) |

### What Flows Down

| From | Information | To | Trigger |
|------|-------------|-----|---------|
| JD | Strategic decisions | Xavier (distributes) | As made |
| JD | Approvals | Requesting agent | When granted |
| Xavier | Routing decisions | Relevant agents | As needed |
| Aurelius | Values guidance | Requesting agent | When asked |
| Clare | Delivery coaching | Dale, other content agents | Per content |
| Supervisors | Task assignments | Direct reports | As needed |

### What Flows Laterally

| From | To | Information | Purpose |
|------|-----|-------------|---------|
| Helena | Eleanor | Contact queries | Relationship data for leads |
| Helena | Cicero | Qualified leads | Pitch preparation |
| Dale | Clare | Draft content | Delivery coaching |
| Ada | Franklin | Promotion plans | Inventory coordination |
| Dale | Helena | Engagement signals | Lead identification |
| Any agent | Any agent | Domain expertise | Consultation |

**Lateral communication rule:** Always cc relevant coordinator (usually Xavier) on cross-domain handoffs.

---

## Error Handling Hierarchy

When something goes wrong:

### Level 1: Self-Correction
Agent detects error, can fix within authority, fixes and logs.

### Level 2: Supervisor Escalation
Agent cannot fix, has supervisor → escalate to supervisor.
Supervisor fixes or escalates to Level 3.

### Level 3: Xavier Escalation
Operational issue beyond supervisor authority → Xavier coordinates fix.
Xavier involves other agents as needed, fixes or escalates to Level 4.

### Level 4: JD Escalation
Issue requires human judgment, major decision, or system-wide impact → JD decides.

**Error documentation required at every level:**
- What happened
- When detected
- What was tried
- Current status
- Recommended action

---

## Audit and Review

### Continuous Monitoring (Xavier)
- Agent task completion rates
- Error frequency by agent
- Override frequency and patterns
- Response time adherence

### Weekly Review (Xavier + Clare)
- Compile agent health summary
- Identify coordination bottlenecks
- Note unusual patterns

### Monthly Review (Xavier + Aurelius + Clare)
- Agent performance vs. metrics
- Values alignment check
- Recommend retirements or expansions
- Present findings to JD

---

*These protocols establish order without bureaucracy. Most agent interactions are autonomous; the hierarchy exists for exceptions.*
