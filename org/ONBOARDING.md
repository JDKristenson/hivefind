# Agent Onboarding Checklist

Use this checklist when introducing a new agent to the AI Crew ecosystem.

---

## Pre-Design Phase

Before writing the spec, answer these questions:

### 1. Need Validation

- [ ] **Problem clarity:** What specific pain does this agent solve?
- [ ] **Current state:** How is this handled today? Time/cost?
- [ ] **Frequency:** How often does this need arise?
- [ ] **Value estimate:** What's the expected ROI (time saved, revenue, risk reduction)?

**Gate:** If you can't articulate the problem clearly, stop. You don't need this agent yet.

### 2. Ecosystem Fit

- [ ] **Domain assignment:** Which domain does this agent belong to?
  - [ ] Coordination
  - [ ] Personal
  - [ ] Haze Gray
  - [ ] Puzzlehouse
  - [ ] New domain (requires justification)

- [ ] **Overlap check:** Does any existing agent already handle part of this?
  - If yes: Can existing agent be expanded instead?
  - If expansion not viable: How will responsibilities be divided?

- [ ] **Dependency mapping:** What other agents will this agent need to interact with?
  | Agent | Interaction Type | Frequency |
  |-------|------------------|-----------|
  |       |                  |           |

- [ ] **Data requirements:** What data does this agent need access to?
  | Data Source | Type of Access | Already Available? |
  |-------------|----------------|-------------------|
  |             |                |                   |

**Gate:** If this agent creates significant overlap or requires data you don't have, reconsider.

### 3. Hierarchy Placement

- [ ] **Reports to:** Who is this agent's supervisor?
  - [ ] JD directly
  - [ ] Xavier (operational coordination)
  - [ ] A domain supervisor (Warren, Franklin)
  - [ ] New supervisor needed (rare; requires justification)

- [ ] **Supervises:** Will this agent supervise other agents?
  - If yes: Which ones? Does this change their current reporting?

- [ ] **Coordination touchpoints:** Which coordination agents will interact with this agent?
  - [ ] Xavier (all agents)
  - [ ] Aurelius (if values/accountability relevant)
  - [ ] Clare (if produces content for briefings)

**Gate:** If hierarchy placement is unclear, the agent's scope isn't defined well enough.

---

## Spec Development Phase

### 4. Core Spec Elements

- [ ] **Identity complete:**
  - [ ] Name selected (historical anchor identified)
  - [ ] Title defined
  - [ ] Domain assigned
  - [ ] Reporting relationship specified
  - [ ] Coordination relationships specified

- [ ] **Mission statement:** One sentence, in agent's voice

- [ ] **Personality developed:**
  - [ ] 2-3 paragraph personality description
  - [ ] 3+ voice examples (✓ good)
  - [ ] 2+ anti-patterns (✗ bad)

- [ ] **Problem definition:**
  - [ ] Pain point articulated
  - [ ] Current state described
  - [ ] Who experiences this identified

### 5. Responsibilities

- [ ] **Each responsibility has:**
  - [ ] Clear trigger (WHEN)
  - [ ] Specific action (WHAT)
  - [ ] Defined output destination (WHERE)

- [ ] **Cadence defined:**
  - [ ] Daily tasks listed with timing
  - [ ] Weekly tasks listed with timing
  - [ ] Monthly/periodic tasks listed

- [ ] **No responsibility overlaps with existing agents**
  - If overlap exists: Handoff protocol documented

### 6. Technical Requirements

- [ ] **Integrations identified:**
  | System | Purpose | Auth Method | Access Level |
  |--------|---------|-------------|--------------|
  |        |         |             |              |

- [ ] **All integrations technically feasible** (APIs exist, access available)

- [ ] **Data schemas defined** for any new data structures

- [ ] **AI capabilities required** listed:
  - [ ] NLG (text generation)
  - [ ] Classification
  - [ ] Extraction
  - [ ] Analysis
  - [ ] Other: ___________

### 7. Decision Framework

- [ ] **Autonomous actions defined** (what agent can do without approval)

- [ ] **Escalation triggers defined:**
  | Situation | Escalates To | Urgency |
  |-----------|--------------|---------|
  |           |              |         |

- [ ] **Hard boundaries defined** (what agent must NEVER do)

- [ ] **Thresholds specified** (dollar amounts, time commitments, etc.)

### 8. Success Metrics

- [ ] **Each metric has:**
  - [ ] Clear target
  - [ ] Measurement method
  - [ ] Frequency of measurement

- [ ] **At least one metric per category:**
  - [ ] Efficiency/speed
  - [ ] Quality/accuracy
  - [ ] Impact/value

### 9. Constraints and Guardrails

- [ ] **Content/output rules** defined
- [ ] **Rate limits** documented (API limits, frequency caps)
- [ ] **Budget constraints** specified
- [ ] **Response time expectations** set

---

## Integration Phase

### 10. Ecosystem Updates

Before building automation:

- [ ] **ARCHITECTURE.md updated:**
  - [ ] Agent added to roster table
  - [ ] Org chart updated
  - [ ] Domain registry updated
  - [ ] Information flows updated (if new flows created)

- [ ] **AGENT_ROSTER.md updated:**
  - [ ] Agent added with namesake
  - [ ] Domain section updated

- [ ] **PROTOCOLS.md updated:**
  - [ ] Decision authority matrix updated
  - [ ] Communication channels updated (if new channels)
  - [ ] Conflict resolution scenarios updated (if new scenarios)

- [ ] **Affected agents notified:**
  | Agent | Change to Their Spec | Updated? |
  |-------|---------------------|----------|
  |       |                     |          |

### 11. Technical Setup

- [ ] **Notion databases created:**
  | Database | Purpose | Schema Documented? |
  |----------|---------|-------------------|
  |          |         |                   |

- [ ] **API connections established:**
  | Integration | Authenticated? | Tested? |
  |-------------|----------------|---------|
  |             |                |         |

- [ ] **Environment variables configured:**
  | Variable | Purpose | Set in n8n? |
  |----------|---------|-------------|
  |          |         |             |

- [ ] **Logging configured:**
  - [ ] Activity log database ready
  - [ ] Log format matches standard
  - [ ] Error logging enabled

### 12. Workflow Build

- [ ] **Workflows built in n8n:**
  | Workflow | Purpose | Tested? |
  |----------|---------|---------|
  |          |         |         |

- [ ] **Error handling implemented:**
  - [ ] API failure handling
  - [ ] Data validation
  - [ ] Escalation on failure

- [ ] **Scheduling configured:**
  - [ ] Cron jobs set correctly
  - [ ] Timezone verified

---

## Validation Phase

### 13. Testing

- [ ] **Unit tests passed:**
  - [ ] Each workflow tested individually
  - [ ] Each integration tested individually

- [ ] **Integration tests passed:**
  - [ ] End-to-end workflow test
  - [ ] Cross-agent handoff test (if applicable)

- [ ] **Edge cases tested:**
  | Edge Case | Expected Behavior | Passed? |
  |-----------|-------------------|---------|
  |           |                   |         |

- [ ] **Failure mode testing:**
  - [ ] API down scenario
  - [ ] Invalid data scenario
  - [ ] Rate limit scenario

### 14. Monitoring Setup

- [ ] **Xavier configured to monitor new agent:**
  - [ ] Health check added
  - [ ] Error threshold set
  - [ ] Performance baseline established

- [ ] **Dashboards updated:**
  - [ ] Agent metrics visible
  - [ ] Domain dashboard includes agent

### 15. Soft Launch

- [ ] **48-hour observation period:**
  - Start date: ___________
  - End date: ___________

- [ ] **Daily review during observation:**
  - [ ] Day 1: No critical errors
  - [ ] Day 2: No critical errors

- [ ] **Metrics baseline captured:**
  | Metric | Baseline Value |
  |--------|----------------|
  |        |                |

---

## Go-Live Phase

### 16. Documentation Finalized

- [ ] **Agent spec finalized** (all sections complete)
- [ ] **Spec added to repository** (correct folder, correct naming)
- [ ] **README updated** if needed
- [ ] **Process docs updated** if this changes any processes

### 17. Communication

- [ ] **Xavier notified:** New agent is live
- [ ] **Clare notified:** Include in briefings as appropriate
- [ ] **Aurelius notified:** Add to accountability reviews
- [ ] **Affected agents notified:** Any workflow changes

### 18. Sign-Off

- [ ] **JD approval:** Agent approved for production
- [ ] **First week review scheduled:** Date: ___________
- [ ] **30-day review scheduled:** Date: ___________

---

## Post-Launch Review

### After 1 Week

- [ ] **Error rate acceptable?**
- [ ] **Metrics on track vs. targets?**
- [ ] **User (JD) feedback positive?**
- [ ] **Any unexpected interactions with other agents?**
- [ ] **Adjustments needed?**

### After 30 Days

- [ ] **Success metrics achieved?**
- [ ] **ROI validated?**
- [ ] **Integration stable?**
- [ ] **Handoffs to other agents working?**
- [ ] **Any spec updates needed based on learnings?**

---

## Quick Reference: Red Flags

Stop and reconsider if:

- ❌ You can't clearly articulate the problem being solved
- ❌ Significant overlap with existing agent responsibilities
- ❌ Required data or integrations don't exist
- ❌ Hierarchy placement is unclear
- ❌ More than 3 agents affected by this addition
- ❌ No clear success metrics
- ❌ Testing reveals frequent errors
- ❌ 48-hour observation shows problems

---

*A well-onboarded agent integrates seamlessly. A poorly-onboarded agent creates chaos. Take the time.*
