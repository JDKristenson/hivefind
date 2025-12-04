# Agent Specification Template

Use this template for all agent job descriptions. Every section should be completed—vague specs lead to broken automations.

---

# AI AGENT JOB DESCRIPTION

## AGENT IDENTITY

**Name:** [Human first name that fits personality and role]  
**Title:** [Clear, descriptive job title]  
**Mission:** [One sentence describing core purpose]

**Persona:** [2-3 sentences describing personality, working style, and voice. This shapes how the agent communicates and makes decisions.]

**Voice Examples:**
- ✓ [Example of good on-brand communication]
- ✓ [Another good example]
- ✗ [Example of what NOT to sound like]

---

## PROBLEM DEFINITION

**Pain Point:** [What specific inefficiency or challenge does this agent address?]

**Current State:** [How is this handled today? Time spent? Error rate? Manual steps?]

**Who Experiences This:** [Who feels this pain and how often?]

---

## KEY RESPONSIBILITIES

Structure each responsibility as: **WHEN** [trigger] → **WHAT** [action] → **HOW** [tools/method]

| # | Responsibility | Trigger → Action → Destination |
|---|----------------|-------------------------------|
| 1 | **[Name]** | [Trigger] → [Action] → [Output destination] |
| 2 | **[Name]** | [Trigger] → [Action] → [Output destination] |
| 3 | **[Name]** | [Trigger] → [Action] → [Output destination] |
| 4 | **[Name]** | [Trigger] → [Action] → [Output destination] |
| 5 | **[Name]** | [Trigger] → [Action] → [Output destination] |

**Cadence Summary:**
- [Daily tasks and timing]
- [Weekly tasks and timing]
- [Monthly/periodic tasks]

---

## WORKFLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────┐
│                         [AGENT NAME]'S LOOP                          │
└─────────────────────────────────────────────────────────────────────┘

  TRIGGERS                    AI PROCESS                    OUTPUTS
  ────────                    ──────────                    ───────
                                   
  [Trigger 1]           ┌─────────────────────┐      [Output 1]
         │               │                     │      [Output 2]
         ▼               │   1. [Step 1]       │      [Output 3]
  ┌─────────────┐        │                     │           │
  │  [Source]   │───────▶│   2. [Step 2]       │           │
  │             │        │                     │           ▼
  └─────────────┘        │   3. [Step 3]       │      ┌─────────┐
                         │                     │      │ [Dest]  │
  [Trigger 2]            │   4. [Step 4]       │      │         │
         │               │                     │      └─────────┘
         ▼               └─────────────────────┘           
  ┌─────────────┐                                          
  │  [Source]   │                                          
  └─────────────┘                                          
```

---

## TECHNICAL REQUIREMENTS

**Inputs:**
- [Data source 1 and what's needed from it]
- [Data source 2 and what's needed from it]
- [Additional inputs]

**Integrations:**

| System | Purpose |
|--------|---------|
| [Integration 1] | [What it's used for] |
| [Integration 2] | [What it's used for] |
| [Integration 3] | [What it's used for] |

**Capabilities Required:**
- [AI capability 1, e.g., natural language generation]
- [AI capability 2, e.g., classification]
- [AI capability 3, e.g., data extraction]

---

## DECISION FRAMEWORK

**Prioritization Criteria:**
1. [How does the agent prioritize when facing multiple tasks?]
2. [What factors determine urgency?]
3. [How are ties broken?]

**Autonomous Actions (No Human Needed):**
- [Action type 1]
- [Action type 2]
- [Action type 3]

**Escalate to Human:**
- [Situation requiring escalation 1]
- [Situation requiring escalation 2]
- [Situation requiring escalation 3]

**Hard Boundaries (Never Do):**
- [Absolute prohibition 1]
- [Absolute prohibition 2]
- [Absolute prohibition 3]

---

## SUCCESS METRICS

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **[Efficiency Metric]** | [Target] | [How measured] |
| **[Quality Metric]** | [Target] | [How measured] |
| **[Impact Metric]** | [Target] | [How measured] |
| **[Consistency Metric]** | [Target] | [How measured] |
| **[Time Saved]** | [Target] | [How measured] |

---

## CONSTRAINTS & GUARDRAILS

**Content/Output Rules:**
- [Rule 1]
- [Rule 2]
- [Rule 3]

**Quality Control:**
- [QC measure 1]
- [QC measure 2]

**Budget/Resources:**
- [Approved tools and costs]
- [Evaluation criteria]

**Response Time:**
- [Expected latency for different task types]

---

## IMPLEMENTATION NOTES

**Platform:** [n8n / Relay.app / Other]

**Phased Rollout:**
- Phase 1: [Scope and timeline]
- Phase 2: [Scope and timeline]
- Phase 3: [Scope and timeline]

**Dependencies:**
- [Other agents this agent depends on]
- [Infrastructure requirements]

**Known Risks:**
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

---

*Spec Version: [X.X] | Created for: [Context] | Agent: [Name]*

---

# TEMPLATE USAGE NOTES

## Before Writing a Spec

1. **Define the trigger clearly.** If you can't specify WHEN the agent acts, you can't automate it.
2. **Be specific about tools.** "Research the web" is vague. "Search LinkedIn Sales Navigator for [criteria]" is automatable.
3. **Challenge yourself on escalation.** Most things people think need human review don't. Be honest about what truly requires judgment.

## Persona Selection (Optional)

Before finalizing, you may want to consider three candidate personas and select the best fit:

**Candidate A: [Name]** - [Working style summary]
- Strengths: [What they excel at]
- Tendencies: [How they approach work]
- Style: [Communication approach]

**Candidate B: [Name]** - [Working style summary]
- Strengths: [What they excel at]
- Tendencies: [How they approach work]
- Style: [Communication approach]

**Candidate C: [Name]** - [Working style summary]
- Strengths: [What they excel at]
- Tendencies: [How they approach work]
- Style: [Communication approach]

## Quality Checklist

Before finalizing any spec, verify:

- [ ] Every responsibility has a clear WHEN trigger
- [ ] All integrations are technically feasible
- [ ] Escalation criteria are specific, not vague
- [ ] Success metrics are measurable
- [ ] Guardrails cover obvious failure modes
- [ ] Persona voice is distinct and consistent
- [ ] Dependencies on other agents are documented
