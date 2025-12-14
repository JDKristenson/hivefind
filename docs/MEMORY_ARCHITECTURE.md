# HiveFind Memory Architecture

## Purpose

The memory layer transforms HiveFind from a collection of stateless automations into a learning system. Agents accumulate wisdom from their own experiences and benefit from the collective knowledge of the entire fleet.

**Design Philosophy:**
- Memory is a first-class architectural component, not an afterthought
- Agents should get smarter over time, not just faster
- Cross-agent learning surfaces patterns no single agent would discover
- Human corrections are the highest-value training signal

---

## Two-Layer Architecture

### Layer 1: Explicit Knowledge (Notion)

Structured, curated knowledge that humans can read, edit, and override.

**Contents:**
- Explicit preferences ("JD prefers window seats", "Never schedule before 8 AM")
- Business rules ("Haze Gray invoices NET 30", "Puzzlehouse ships via USPS Priority")
- Relationship context ("Client X prefers email over calls", "Vendor Y always negotiates")
- Decision frameworks ("When budget exceeds $500, escalate to JD")

**Characteristics:**
- Human-readable and editable
- Authoritative (overrides experiential memory when conflicts arise)
- Relatively stable (updated intentionally, not automatically)
- Tagged by domain, agent, and confidence level

### Layer 2: Experiential Memory (Vector Database)

Semantic, accumulated wisdom from task execution.

**Contents:**
- Task outcomes (what was attempted, what happened, lessons learned)
- Pattern observations ("Flights to London are 30% cheaper on Tuesdays")
- Correction records (when JD overrode an agent decision, why)
- Cross-agent correlations ("High stress weeks correlate with travel + client deadlines")

**Characteristics:**
- Semantic retrieval (query by meaning, not just keywords)
- Continuously growing
- Probabilistic (confidence scores, not absolute truth)
- Requires periodic consolidation and pruning

---

## Memory Types

### 1. Preferences
Learned or stated user preferences.

```
{
  "type": "preference",
  "domain": "travel",
  "subject": "flight_timing",
  "observation": "JD consistently chooses morning departures over evening when price difference < $100",
  "confidence": 0.85,
  "evidence_count": 12,
  "source_agent": "Atlas",
  "last_updated": "2025-12-01"
}
```

### 2. Patterns
Discovered correlations and regularities.

```
{
  "type": "pattern",
  "domain": "productivity",
  "observation": "Task completion rate drops 40% on days with 4+ meetings",
  "correlation_strength": 0.72,
  "sample_size": 45,
  "discovered_by": "Clare",
  "contributing_agents": ["Hamilton", "Galen"],
  "actionable": true,
  "suggested_action": "Limit meeting days to 3 meetings max"
}
```

### 3. Outcomes
Results of specific decisions or actions.

```
{
  "type": "outcome",
  "task_id": "atlas_booking_2025_11_15",
  "decision": "Booked connecting flight via Frankfurt instead of direct",
  "rationale": "Saved $450, added 3 hours travel time",
  "result": "negative",
  "feedback": "JD: 'Not worth it for client meetings. Direct flights for business travel.'",
  "lesson": "Prioritize direct flights for client-facing travel regardless of cost savings",
  "agent": "Atlas"
}
```

### 4. Corrections
Human overrides of agent decisions.

```
{
  "type": "correction",
  "agent": "Eleanor",
  "original_action": "Classified email from john@newclient.com as low priority",
  "correction": "JD escalated to high priority, responded immediately",
  "context": "New lead from conference, time-sensitive",
  "lesson": "Emails from unknown senders mentioning recent events (conferences, webinars) should be flagged for review",
  "severity": "medium"
}
```

### 5. Relationships
Information about people and organizations.

```
{
  "type": "relationship",
  "entity": "Sarah Chen",
  "entity_type": "client",
  "organization": "TechCorp Inc",
  "observations": [
    "Prefers Zoom over phone calls",
    "Usually reschedules Monday meetings",
    "Decision maker, but checks with CFO for purchases > $50k"
  ],
  "interaction_count": 23,
  "last_interaction": "2025-11-28",
  "contributing_agents": ["Eleanor", "Helena", "Hamilton"]
}
```

---

## Memory Agent: Evelyn

A dedicated agent owns the memory layer. This prevents memory from being "everyone's job and no one's responsibility."

### Evelyn's Responsibilities

**Curation:**
- Review new memories for quality and accuracy
- Merge duplicate or similar observations
- Escalate uncertain or high-impact learnings for human review
- Prune stale or contradicted memories

**Consolidation:**
- Weekly: Synthesize task outcomes into pattern candidates
- Monthly: Promote validated patterns to explicit knowledge (Notion)
- Quarterly: Archive or deprecate outdated memories

**Cross-Agent Intelligence:**
- Surface relevant memories to agents before they act
- Identify cross-domain patterns (e.g., financial stress + health decline)
- Alert when agent behaviors contradict established knowledge

**Query Interface:**
- Agents query Evelyn, not the databases directly
- Evelyn decides which layer to search and how to weight results
- Provides context-appropriate responses (full detail vs. summary)

### Evelyn's Workflows

1. **Memory Ingestion** (continuous)
   - Trigger: Agent completes task and submits memory payload
   - Action: Validate, tag, embed, store
   - Output: Confirmation or request for clarification

2. **Pre-Action Briefing** (on-demand)
   - Trigger: Agent requests relevant knowledge before acting
   - Action: Query both layers, rank by relevance and recency
   - Output: Synthesized brief with confidence indicators

3. **Correction Processing** (event-driven)
   - Trigger: Human overrides agent decision
   - Action: Capture context, extract lesson, update memories, notify originating agent
   - Output: Updated memory, optional workflow adjustment recommendation

4. **Weekly Consolidation** (scheduled)
   - Trigger: Sunday 11 PM
   - Action: Analyze week's memories, identify patterns, flag for review
   - Output: Consolidation report to Notion

5. **Memory Health Check** (scheduled)
   - Trigger: First of month
   - Action: Audit memory quality, identify gaps, measure retrieval accuracy
   - Output: Health report with recommendations

---

## Agent Integration

### Writing to Memory

Every agent workflow should end with a memory submission step:

```
Task Complete → Evaluate Outcome → Generate Memory Payload → Submit to Evelyn
```

**Memory Payload Template:**
```json
{
  "agent": "string",
  "task_id": "string",
  "task_type": "string",
  "outcome": "success | partial | failure",
  "decision_made": "string",
  "rationale": "string",
  "result_summary": "string",
  "lessons": ["string"],
  "confidence": 0.0-1.0,
  "tags": ["string"],
  "related_entities": ["string"],
  "human_feedback": "string | null"
}
```

### Reading from Memory

Before making non-trivial decisions, agents query Evelyn:

```
Identify Decision Point → Formulate Query → Request from Evelyn → Incorporate into Reasoning
```

**Query Types:**
- `preference_check`: "What are JD's preferences for X?"
- `pattern_lookup`: "What patterns exist around X?"
- `outcome_search`: "What happened last time we did X?"
- `entity_brief`: "What do we know about person/org X?"
- `cross_domain`: "What might agent Y know that's relevant to X?"

---

## Technical Implementation

### Vector Database Selection: Pinecone

**Rationale:**
- Managed service (no infrastructure to maintain)
- Good documentation and n8n integration
- Scales from hobby to production
- Reasonable free tier for initial development

**Alternatives Considered:**
- Chroma: Simpler, but requires self-hosting for persistence
- Weaviate: More features, but more complexity than needed initially
- Qdrant: Strong performance, but less ecosystem support

### Schema Design

**Pinecone Index Structure:**
```
Index: hivefind-memory
Dimension: 1536 (OpenAI ada-002) or 1024 (Cohere)
Metric: cosine

Metadata fields:
- type: string (preference, pattern, outcome, correction, relationship)
- agent: string
- domain: string
- confidence: float
- timestamp: datetime
- tags: string[]
- entity_refs: string[]
```

**Notion Databases:**

1. **Explicit Preferences**
   - Name, Domain, Rule, Source, Confidence, Last Validated

2. **Business Rules**
   - Name, Category, Rule, Exceptions, Owner Agent

3. **Entity Directory**
   - Name, Type, Organization, Key Facts, Relationship Strength, Last Contact

4. **Memory Review Queue**
   - Memory Summary, Source Agent, Proposed Action, Status, Reviewer Notes

---

## Memory Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        MEMORY LIFECYCLE                          │
└─────────────────────────────────────────────────────────────────┘

    CREATION                VALIDATION              CONSOLIDATION
        │                       │                        │
        ▼                       ▼                        ▼
  ┌──────────┐           ┌──────────┐            ┌──────────┐
  │  Agent   │           │  Evelyn  │            │  Evelyn  │
  │ submits  │──────────►│ reviews  │───────────►│ merges   │
  │ memory   │           │ & tags   │            │ patterns │
  └──────────┘           └──────────┘            └──────────┘
                               │                       │
                               ▼                       ▼
                         ┌──────────┐            ┌──────────┐
                         │  Vector  │            │  Notion  │
                         │    DB    │            │ (if high │
                         │ (store)  │            │  conf.)  │
                         └──────────┘            └──────────┘

    RETRIEVAL                DECAY                  PRUNING
        │                      │                       │
        ▼                      ▼                       ▼
  ┌──────────┐           ┌──────────┐            ┌──────────┐
  │  Agent   │           │ Confidence│           │  Evelyn  │
  │ queries  │           │ decays    │           │ archives │
  │ Evelyn   │           │ over time │           │ or       │
  └──────────┘           └──────────┘            │ deletes  │
        │                      │                 └──────────┘
        ▼                      ▼
  ┌──────────┐           ┌──────────┐
  │  Evelyn  │           │ Re-verify│
  │ returns  │           │ or decay │
  │ relevant │           │ further  │
  │ memories │           └──────────┘
  └──────────┘
```

---

## Confidence and Decay

### Confidence Scoring

| Source | Initial Confidence |
|--------|-------------------|
| Human explicit statement | 1.0 |
| Human correction | 0.95 |
| Validated pattern (5+ instances) | 0.8 |
| Single task outcome | 0.5 |
| Agent inference | 0.4 |

### Decay Rules

- Preferences: No decay (until contradicted)
- Patterns: -0.05 per month without reinforcement
- Outcomes: -0.1 per month (older experiences less relevant)
- Corrections: -0.02 per month (lessons fade slowly)

### Contradiction Handling

When new evidence contradicts existing memory:
1. Flag both memories for review
2. Do not automatically delete either
3. Present conflict to Evelyn's weekly consolidation
4. If high-stakes, escalate to human immediately

---

## Privacy and Sensitivity

### Classification Levels

| Level | Description | Access | Example |
|-------|-------------|--------|---------|
| Open | Any agent can access | All | "JD prefers morning flights" |
| Domain | Only relevant agents | Tagged | Financial patterns (Warren, Graham) |
| Restricted | Human approval required | Evelyn + Human | Health correlations, relationship details |
| Private | Human-only | None | Specific financial figures, personal health data |

### Data Handling

- All memories encrypted at rest
- No raw financial account numbers in memory
- Health data stored as patterns, not raw metrics
- Relationship data anonymizable for demos

---

## Success Metrics

### Quantitative
- Memory retrieval relevance score (human-rated sample)
- Pattern prediction accuracy (did the pattern hold?)
- Agent decision quality improvement over time
- Correction frequency (should decrease as system learns)

### Qualitative
- JD reports agents "feel smarter"
- Agents surface insights JD hadn't considered
- Cross-agent patterns identify non-obvious correlations
- System recommends workflow improvements

---

## Implementation Phases

### Phase 0.5: Memory Infrastructure (Add to existing Phase 0)
- [ ] Set up Pinecone account and index
- [ ] Create Notion memory databases
- [ ] Build memory ingestion n8n workflow
- [ ] Build memory query n8n workflow
- [ ] Test with synthetic memories

### Phase 1.5: Evelyn MVP (After Eleanor, before Ada)
- [ ] Draft Evelyn agent spec
- [ ] Build memory curation workflow
- [ ] Build pre-action briefing workflow
- [ ] Build correction processing workflow
- [ ] Integrate with Eleanor as first memory-enabled agent

### Ongoing: Memory Integration
- Each subsequent agent includes memory read/write in workflows
- Monthly review of memory quality and system improvements

---

## Open Questions

1. **Embedding model choice:** OpenAI ada-002 is standard, but Cohere or local models could reduce costs. Decision can be deferred.

2. **Memory visualization:** Should there be a dashboard showing what the system has learned? Useful for trust-building but adds scope.

3. **Export/portability:** If you want to switch vector DBs later, need an export strategy. Worth building from the start?

4. **Demo mode:** For client demos, should there be a way to show the memory system without exposing personal data?

---

*Version: 1.0*
*Created: December 2025*
*Owner: Evelyn (Memory Curator)*
