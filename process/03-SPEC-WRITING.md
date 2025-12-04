# Spec Writing Process

How individual agent specifications were developed, with examples and patterns.

---

## The Core Insight

Agent specs are job descriptions for AI. The same principles that make a human job description useful apply:

- Clear scope (what is and isn't your job)
- Defined authority (what you can decide vs. escalate)
- Success criteria (how we know you're doing well)
- Cultural fit (voice, values, working style)

The difference: AI specs need to be *automation-ready*. Every responsibility needs a trigger specific enough to code.

---

## The Template Evolution

### Version 1: Too Vague

Early specs were narrative-heavy:

```
## Responsibilities
Ada manages social media for Puzzlehouse.com, creating engaging content
that showcases our puzzle collection and builds community with puzzle
enthusiasts.
```

**Problem:** Can't automate "manages social media." What triggers what? When? To where?

### Version 2: Better Structure

Added the Trigger → Action → Output format:

```
| # | Responsibility | Trigger → Action → Destination |
|---|----------------|-------------------------------|
| 1 | **Daily Content** | Weekday mornings → Generate platform-native post from Shopify product → Publish to scheduled platforms |
```

**Better:** Now we know when (weekday mornings), what (generate post), and where (platforms).

### Version 3: Complete Specification

Final template includes:
- Identity section with personality and voice examples
- Problem definition (what pain this solves)
- Responsibilities in Trigger → Action → Output format
- Workflow diagram (visual representation)
- Technical requirements (integrations, APIs)
- Decision framework (autonomous vs. escalate vs. never)
- Success metrics (measurable outcomes)
- Constraints and guardrails

---

## Writing Process: Step by Step

### Step 1: Define the Pain

Before writing anything, answer:
- What's the actual problem being solved?
- How much time/money does this cost today?
- Who experiences this pain and how often?

**Example (Ada - Social Media Director):**
> Puzzlehouse.com is a newly acquired brand with zero social presence.
> Creating consistent, quality content manually would take 5-10 hours/week
> that the owner doesn't have. Without content, no organic discovery happens.

This grounds the spec in reality. If you can't articulate the pain, you might not need this agent.

### Step 2: List Everything

Brain dump everything this agent should do. Don't organize yet.

**Example (Ada):**
- Post to Instagram
- Post to Facebook
- Post to LinkedIn
- Post to TikTok
- Research trending hashtags
- Monitor competitors
- Track engagement metrics
- Respond to comments
- Identify UGC opportunities
- Plan content calendar
- Coordinate with inventory (don't promote out-of-stock)
- Generate reports
- Etc.

### Step 3: Structure as Responsibilities

Group and structure the brain dump into distinct responsibilities, each with Trigger → Action → Output:

| # | Responsibility | Trigger → Action → Destination |
|---|----------------|-------------------------------|
| 1 | **Publish Daily Content** | Weekday mornings → Pull product from Shopify, generate platform-native post → Publish to scheduled platforms |
| 2 | **Research Trends** | Monday mornings → Scan hashtags and competitors → Log insights to Notion |
| 3 | **Monitor Mentions** | Daily → Search for brand mentions → Log notable mentions to Notion |
| 4 | **Track Performance** | Friday evenings → Pull analytics, compile report → Update Notion dashboard |

### Step 4: Reality-Check Technical Feasibility

For each responsibility, verify:
- What API/integration is needed?
- Is that integration available?
- What data do we actually have access to?
- What are the rate limits?

This often forces revisions. "Monitor all competitor activity" becomes "Check top 3 competitor accounts weekly" when you realize API limitations.

### Step 5: Define Decision Boundaries

Three categories:

**Autonomous (No Approval):**
- Publish scheduled content
- Respond to positive comments with brief thanks
- Log metrics

**Escalate to Human:**
- Negative comments or complaints
- Press or partnership inquiries
- Viral moments (need amplification decision)

**Never Do:**
- Post political content
- Engage with trolls
- Claim UGC without attribution

This section gets the most revision. The default is to over-escalate. Push yourself: does this *really* need human judgment, or am I just nervous about delegation?

### Step 6: Develop Voice and Personality

Write example communications in the agent's voice:

**Good (✓):**
- "There's something deeply satisfying about finding that last corner piece."
- "Monet's water lilies, now in 1,000 pieces. Take your time."

**Bad (✗):**
- "OMG you NEED this puzzle!! Link in bio!"
- "Check out our amazing new arrival!"

The anti-patterns are as important as the examples. They define the boundaries.

### Step 7: Set Success Metrics

Make them measurable:

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Posting Cadence** | 95% adherence | Posts delivered / scheduled |
| **Engagement Rate** | Baseline + 10% monthly | Platform analytics |
| **Follower Growth** | 500/platform in 90 days | Platform analytics |
| **"AI Slop" Complaints** | Zero | Manual review |

### Step 8: Iterate

First drafts are always too vague or too ambitious. Revision cycle:
1. Re-read each responsibility. Can you specify the exact trigger?
2. Review escalation criteria. Are you over-escalating out of caution?
3. Check voice examples. Are they distinct from other agents?
4. Validate technical requirements. Have you actually confirmed API access?

Usually takes 2-3 passes.

---

## Common Patterns Across Specs

### The Daily Rhythm Pattern

Most agents have daily, weekly, and monthly cycles:
- **Daily:** Core operational tasks (post content, triage email, check health data)
- **Weekly:** Analysis and planning (compile metrics, review pipeline, plan content)
- **Monthly:** Review and adjustment (performance evaluation, strategy update)

### The Monitor → Flag → Act Pattern

Many responsibilities follow this flow:
1. Monitor a data source continuously
2. Flag anomalies or triggers
3. Act autonomously OR escalate based on criteria

Example (Warren - Finance):
- Monitor transactions daily
- Flag unusual patterns (>$500 unexpected, failed charges)
- Log routine transactions autonomously; escalate flagged items

### The Synthesize → Deliver Pattern

Coordination agents especially use this:
1. Collect data from multiple sources/agents
2. Synthesize into a coherent summary
3. Deliver in appropriate format (briefing, report, alert)

Example (Clare - Communications):
- Collect outputs from all domain agents
- Synthesize into morning briefing
- Deliver as 2-3 minute video

---

## Spec Complexity Spectrum

Not all specs are equal complexity:

### Simple Specs (~2 hours)
- Single domain focus
- Few integrations
- Clear triggers
- Minimal coordination with other agents

*Example: Ada (Social Media) - pulls from Shopify, posts to platforms*

### Medium Specs (~3-4 hours)
- Cross-domain considerations
- Multiple integrations
- Some coordination required
- More nuanced decision boundaries

*Example: Warren (Finance) - aggregates from multiple financial sources, supervises Hetty*

### Complex Specs (~4-6 hours)
- Coordination role spanning many agents
- Complex information flows
- Nuanced escalation criteria
- Multiple output formats

*Example: Xavier (Chief of Staff) - monitors all agents, handles cross-agent coordination*

---

## Using AI to Write Specs

Claude was extensively used for spec development. Effective patterns:

### Pattern 1: Start with Context
```
"I'm building an AI agent ecosystem. This agent's role is [X].
The domain is [Y]. Key integrations will be [Z]. Draft a spec
following this template: [template]"
```

### Pattern 2: Push for Specificity
```
"This responsibility is too vague. What exactly triggers it?
What's the specific output? Where does it go?"
```

### Pattern 3: Challenge Decisions
```
"You have X in the 'escalate to human' category. Does this really
need human judgment, or could the agent handle it autonomously
with the right rules?"
```

### Pattern 4: Request Edge Cases
```
"What edge cases haven't I considered? What could go wrong with
this agent's responsibilities?"
```

### Pattern 5: Voice Development
```
"Write 5 example communications in this agent's voice. Then write
3 anti-patterns showing what this agent would never say."
```

---

## Example: Full Development Session

Here's an abbreviated version of how a spec gets developed:

**Session 1 (Initial Draft)**
- Provide context: role, domain, key functions
- Claude drafts initial spec
- Review: too vague on triggers, responsibilities overlap

**Session 2 (Refinement)**
- Request specific triggers for each responsibility
- Ask about technical feasibility
- Clarify decision boundaries

**Session 3 (Voice and Polish)**
- Develop personality section with examples
- Write success metrics
- Add constraints and guardrails

**Session 4 (Final Review)**
- Read through complete spec
- Check for consistency with other agents
- Verify technical requirements are realistic
- Sign off on final version

---

## Quality Checklist

Before considering a spec complete:

- [ ] Every responsibility has a specific trigger
- [ ] All integrations are technically feasible
- [ ] Decision boundaries are explicit (autonomous vs. escalate vs. never)
- [ ] Voice examples are distinct from other agents
- [ ] Success metrics are measurable
- [ ] Guardrails cover obvious failure modes
- [ ] Dependencies on other agents are documented
- [ ] The spec could be handed to someone else to implement

---

*The goal: a spec so complete that building the automation is just translation, not design.*
