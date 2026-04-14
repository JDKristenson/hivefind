# HiveFind Memory Architecture

## Purpose

The memory layer transforms HiveFind from stateless automations into a learning system. Agents accumulate wisdom from their own experiences and benefit from collective fleet knowledge.

**Design Philosophy:**
- Memory is a first-class architectural component, not an afterthought
- Notion databases are the source of truth -- structured, human-readable, editable
- Agents get smarter over time through curated memory, not raw data accumulation
- Human corrections are the highest-value training signal
- Vector search exists as an optional fallback, not the primary path

---

## Architecture Overview

### Primary: Notion Memory Databases

All memory lives in structured Notion databases. Agents write directly. Evelyn (Memory) curates, consolidates, and serves context.

**Why Notion-native:**
- Human-readable and editable without tooling
- Notion AI provides built-in semantic search across all properties
- Structured properties replace vector metadata (type, agent, domain, confidence, tags)
- Automations handle decay, rollups, and lifecycle without external services
- Single platform for both explicit knowledge and experiential memory (no two-layer split)

### Fallback: Pinecone Vector Search

Available when Notion semantic search proves insufficient for a query. See [Appendix: Vector Search Fallback](#appendix-vector-search-fallback).

---

## Agent Roles

### Evelyn (EA) -- Executive Assistant

Email triage, calendar management, scheduling. May query memory for context (preferences, relationships) but does not own or curate it.

| Responsibility | Memory Interaction |
|---|---|
| Email triage and routing | Reads relationship and preference memories |
| Calendar and scheduling | Reads scheduling preferences |
| Task outcomes | Writes outcome memories after task completion |
| Corrections received | Forwards corrections to Evelyn (Memory) |

### Evelyn (Memory) -- Memory Curator

Dedicated Notion agent that owns the memory layer. Curates, consolidates, and serves context from Notion memory databases. Prevents memory from being "everyone's job and no one's responsibility."

| Responsibility | Details |
|---|---|
| **Curation** | Review new memories for quality and accuracy. Merge duplicates. Escalate uncertain or high-impact learnings for human review. Prune stale or contradicted entries. |
| **Consolidation** | Weekly: synthesize outcomes into pattern candidates. Monthly: promote validated patterns to high-confidence entries. Quarterly: archive or deprecate outdated memories. |
| **Cross-Agent Intelligence** | Surface relevant memories to agents before they act. Identify cross-domain patterns. Alert when agent behaviors contradict established knowledge. |
| **Query Interface** | Agents query Evelyn (Memory), not the databases directly. She decides which DB to search, how to weight results, and whether to fall back to Pinecone. Returns context-appropriate responses (full detail vs. summary). |

### Evelyn (Memory) Workflows

**1. Memory Ingestion** (continuous)
- Trigger: Agent completes task and submits memory payload to Notion DB
- Action: Validate properties, check for duplicates, tag, store
- Output: Confirmation or request for clarification

**2. Pre-Action Briefing** (on-demand)
- Trigger: Agent requests relevant knowledge before acting
- Action: Query Notion DBs via semantic search, rank by relevance and recency
- Fallback: If Notion search returns low-confidence results, query Pinecone
- Output: Synthesized brief with confidence indicators

**3. Correction Processing** (event-driven)
- Trigger: Human overrides agent decision
- Action: Capture context, extract lesson, create correction entry, notify originating agent
- Output: Updated memory, optional workflow adjustment recommendation

**4. Weekly Consolidation** (scheduled, Sunday 11 PM)
- Trigger: Cron
- Action: Analyze week's memories, identify pattern candidates, flag for review
- Output: Consolidation report page in Notion

**5. Memory Health Check** (scheduled, first of month)
- Trigger: Cron
- Action: Audit memory quality, run decay formulas, identify gaps, measure retrieval accuracy
- Output: Health report with recommendations

---

## Memory Types

All memory types are entries in Notion databases with shared core properties and type-specific fields.

### Core Properties (All Types)

| Property | Type | Description |
|---|---|---|
| `type` | Select | preference, pattern, outcome, correction, relationship |
| `agent` | Select | Originating agent name |
| `domain` | Select | travel, productivity, financial, health, etc. |
| `confidence` | Number (0.0-1.0) | Current confidence score |
| `timestamp` | Date | Creation date |
| `tags` | Multi-select | Free-form categorization |
| `entity_refs` | Relation | Links to Entity Directory entries |
| `modality` | Select | text, image, audio, video, pdf, multimodal |
| `last_validated` | Date | Last confirmation or reinforcement |
| `decay_eligible` | Checkbox | Whether decay formula applies |

### 1. Preferences

Learned or stated user preferences.

```json
{
  "type": "preference",
  "domain": "travel",
  "title": "Morning departure preference",
  "observation": "JD consistently chooses morning departures over evening when price difference < $100",
  "confidence": 0.85,
  "evidence_count": 12,
  "agent": "Atlas",
  "last_validated": "2025-12-01"
}
```

### 2. Patterns

Discovered correlations and regularities.

```json
{
  "type": "pattern",
  "domain": "productivity",
  "title": "Meeting overload drops completion rate",
  "observation": "Task completion rate drops 40% on days with 4+ meetings",
  "correlation_strength": 0.72,
  "sample_size": 45,
  "agent": "Clare",
  "contributing_agents": ["Hamilton", "Galen"],
  "actionable": true,
  "suggested_action": "Limit meeting days to 3 meetings max"
}
```

### 3. Outcomes

Results of specific decisions or actions.

```json
{
  "type": "outcome",
  "task_id": "atlas_booking_2025_11_15",
  "title": "Connecting flight cost tradeoff -- negative",
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

```json
{
  "type": "correction",
  "agent": "Evelyn EA",
  "title": "Conference lead misclassified as low priority",
  "original_action": "Classified email from john@newclient.com as low priority",
  "correction": "JD escalated to high priority, responded immediately",
  "context": "New lead from conference, time-sensitive",
  "lesson": "Emails from unknown senders mentioning recent events (conferences, webinars) should be flagged for review",
  "severity": "medium"
}
```

### 5. Relationships

Information about people and organizations.

```json
{
  "type": "relationship",
  "title": "Sarah Chen -- TechCorp Inc",
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
  "contributing_agents": ["Evelyn EA", "Helena", "Hamilton"]
}
```

---

## Notion Database Schema

### Memory DB (Primary)

Stores all five memory types in a single database with views filtered by type.

| Property | Notion Type | Notes |
|---|---|---|
| Title | Title | Short descriptive name |
| Type | Select | preference, pattern, outcome, correction, relationship |
| Agent | Select | Originating agent |
| Domain | Select | travel, productivity, financial, health, relationships, business |
| Confidence | Number | 0.0-1.0, formula-adjusted for decay |
| Evidence Count | Number | Times reinforced |
| Observation | Rich text | Primary content |
| Lesson | Rich text | Extracted learning (outcomes, corrections) |
| Tags | Multi-select | Free-form |
| Entity Refs | Relation | Links to Entity Directory |
| Modality | Select | text, image, audio, video, pdf, multimodal |
| Created | Created time | Auto |
| Last Validated | Date | Manual or automation-updated |
| Decay Eligible | Checkbox | Patterns and outcomes: yes. Preferences and corrections: no. |
| Confidence (Decayed) | Formula | `confidence - (decay_rate * months_since_validated)` |
| Status | Select | active, review, archived, contradicted |

**Views:**
- All Active Memories (filter: status = active)
- Preferences (filter: type = preference)
- Patterns (filter: type = pattern)
- Outcomes (filter: type = outcome)
- Corrections (filter: type = correction)
- Relationships (filter: type = relationship)
- Review Queue (filter: status = review)
- Low Confidence (filter: Confidence Decayed < 0.3)
- By Agent (group by: agent)

### Entity Directory DB

| Property | Notion Type | Notes |
|---|---|---|
| Name | Title | Person or organization |
| Type | Select | client, vendor, colleague, partner, personal |
| Organization | Rich text | Company affiliation |
| Key Facts | Rich text | Structured observations |
| Relationship Strength | Select | strong, moderate, weak, new |
| Last Contact | Date | |
| Contributing Agents | Multi-select | Which agents contributed info |
| Related Memories | Relation | Back-link to Memory DB |

### Memory Review Queue DB

| Property | Notion Type | Notes |
|---|---|---|
| Memory Link | Relation | Link to Memory DB entry |
| Source Agent | Select | Who submitted |
| Proposed Action | Select | merge, archive, escalate, promote |
| Status | Select | pending, approved, rejected |
| Reviewer Notes | Rich text | Human or Evelyn (Memory) notes |
| Priority | Select | high, medium, low |

---

## Memory Lifecycle

```
    CREATION                  CURATION                CONSOLIDATION
        |                        |                         |
        v                        v                         v
  +-----------+            +-----------+             +-----------+
  |  Agent    |            | Evelyn    |             | Evelyn    |
  |  writes   |----------->| (Memory)  |------------>| (Memory)  |
  |  to       |            | reviews,  |             | merges    |
  |  Notion   |            | tags,     |             | patterns, |
  |  DB       |            | dedupes   |             | promotes  |
  +-----------+            +-----------+             +-----------+
                                |                         |
                                v                         v
                          +-----------+             +-----------+
                          | Notion DB |             | High-conf |
                          | (stored   |             | entries   |
                          |  as       |             | promoted  |
                          |  active)  |             | to prefs  |
                          +-----------+             +-----------+

    RETRIEVAL                  DECAY                   PRUNING
        |                        |                         |
        v                        v                         v
  +-----------+            +-----------+             +-----------+
  |  Agent    |            | Notion    |             | Evelyn    |
  |  queries  |            | formula   |             | (Memory)  |
  |  Evelyn   |            | reduces   |             | archives  |
  |  (Memory) |            | confidence|             | or        |
  +-----------+            | over time |             | deletes   |
        |                  +-----------+             +-----------+
        v                        |
  +-----------+            +-----------+
  | Notion    |            | Below     |
  | semantic  |            | threshold |
  | search    |            | -> review |
  | returns   |            | queue     |
  | results   |            +-----------+
  +-----------+
        |
        v (if insufficient)
  +-----------+
  | Pinecone  |
  | fallback  |
  | query     |
  +-----------+
```

---

## Confidence and Decay

### Confidence Scoring

| Source | Initial Confidence |
|---|---|
| Human explicit statement | 1.0 |
| Human correction | 0.95 |
| Validated pattern (5+ instances) | 0.8 |
| Single task outcome | 0.5 |
| Agent inference | 0.4 |

### Decay Rules

Implemented as Notion formula fields on `Confidence (Decayed)`.

| Type | Decay Rate | Decay Eligible | Notes |
|---|---|---|---|
| Preferences | None | No | Stable until contradicted |
| Patterns | -0.05/month | Yes | Without reinforcement |
| Outcomes | -0.1/month | Yes | Older experiences less relevant |
| Corrections | -0.02/month | Yes | Lessons fade slowly |
| Relationships | None | No | Updated on interaction |

`months_since_validated` = `dateBetween(now(), prop("Last Validated"), "months")`

Entries where `Confidence (Decayed)` drops below 0.3 auto-move to the Review Queue via Notion automation.

### Contradiction Handling

When new evidence contradicts an existing memory:
1. Flag both entries with status = `contradicted`
2. Do not delete either
3. Create a Review Queue entry with proposed action = `merge` or `escalate`
4. If high-stakes (confidence > 0.8 on the contradicted entry), escalate to human immediately
5. Otherwise, queue for Evelyn (Memory) weekly consolidation

---

## Agent Integration

### Writing to Memory

Every agent workflow ends with a memory submission step. Agents write directly to the Notion Memory DB.

```
Task Complete -> Evaluate Outcome -> Write to Notion Memory DB -> Evelyn (Memory) curates
```

**Memory Payload Template:**

```json
{
  "agent": "string",
  "task_id": "string",
  "task_type": "string",
  "type": "preference | pattern | outcome | correction | relationship",
  "domain": "string",
  "outcome": "success | partial | failure",
  "decision_made": "string",
  "rationale": "string",
  "result_summary": "string",
  "lessons": ["string"],
  "confidence": 0.0-1.0,
  "tags": ["string"],
  "entity_refs": ["string"],
  "modality": "text | image | audio | video | pdf | multimodal",
  "human_feedback": "string | null"
}
```

Agents map this payload to Notion DB properties when creating pages. The Notion MCP `notion-create-pages` tool handles the write.

### Reading from Memory

Before making non-trivial decisions, agents query Evelyn (Memory).

```
Identify Decision Point -> Formulate Query -> Request from Evelyn (Memory) -> Incorporate into Reasoning
```

**Query Types:**

| Query Type | Description | Primary Search |
|---|---|---|
| `preference_check` | What are JD's preferences for X | Notion filter: type = preference, domain = X |
| `pattern_lookup` | What patterns exist around X | Notion AI semantic search on observation field |
| `outcome_search` | What happened last time we did X | Notion filter: type = outcome + keyword search |
| `entity_brief` | What do we know about person/org X | Entity Directory lookup + related memories |
| `cross_domain` | What might agent Y know relevant to X | Notion filter: agent = Y, semantic search on X |

Evelyn (Memory) uses Notion's built-in semantic search first. If results score below a confidence threshold or return empty, she falls back to Pinecone vector search (when available).

---

## Privacy and Sensitivity

### Classification Levels

| Level | Description | Notion Access | Example |
|---|---|---|---|
| Open | Any agent can access | All workspace members | "JD prefers morning flights" |
| Domain | Only relevant agents | Restricted to tagged agents via DB permissions | Financial patterns (Warren, Graham) |
| Restricted | Human approval required | Evelyn (Memory) + Human only | Health correlations, relationship details |
| Private | Human-only | Page-level lock, no agent access | Financial figures, personal health data |

### Implementation

- Notion page-level permissions enforce classification levels
- Domain-level entries tagged with allowed agents in a multi-select property
- Restricted entries require Evelyn (Memory) to request human unlock before serving to agents
- Private entries excluded from all agent queries via filtered views
- No raw financial account numbers in memory
- Health data stored as patterns, not raw metrics
- Relationship data anonymizable for demos

---

## Success Metrics

### Quantitative

| Metric | Target | Measurement |
|---|---|---|
| Memory retrieval relevance | >80% human-rated useful | Monthly sample review |
| Pattern prediction accuracy | >60% hold rate | Track pattern vs. actual outcome |
| Correction frequency | Decreasing trend | Monthly count, grouped by agent |
| Query response time | <3s for Notion, <5s with fallback | Logged per query |
| Memory DB health | <10% stale entries | Monthly health check |

### Qualitative
- JD reports agents "feel smarter"
- Agents surface insights JD had not considered
- Cross-agent patterns identify non-obvious correlations
- System recommends workflow improvements

---

## Implementation Phases

### Phase 0.5: Memory Infrastructure

- [ ] Create Notion Memory DB with schema above
- [ ] Create Entity Directory DB
- [ ] Create Memory Review Queue DB
- [ ] Configure Notion views (by type, by agent, review queue, low confidence)
- [ ] Set up Notion automations for decay threshold alerts
- [ ] Test with synthetic memories (10 per type)
- [ ] Verify Notion AI semantic search returns relevant results

### Phase 1.5: Evelyn (Memory) MVP

- [ ] Draft Evelyn (Memory) agent spec
- [ ] Build memory ingestion workflow (agent writes to Notion DB)
- [ ] Build pre-action briefing workflow (Notion semantic search)
- [ ] Build correction processing workflow
- [ ] Integrate with Evelyn (EA) as first memory-enabled agent
- [ ] Validate Notion search quality; decide if Pinecone fallback needed

### Phase 2: Full Fleet Integration

- [ ] Each subsequent agent includes memory read/write in workflows
- [ ] Weekly consolidation automation
- [ ] Monthly health check automation
- [ ] If Pinecone fallback activated: build sync pipeline from Notion to Pinecone

### Ongoing

- Monthly review of memory quality
- Quarterly archive of low-confidence entries
- Evaluate whether Pinecone fallback adds value or can be dropped entirely

---

## Appendix: Vector Search Fallback

### When to Use

Pinecone vector search is a fallback for cases where Notion semantic search is insufficient:
- High-volume similarity matching across thousands of entries
- Cross-modal search (querying text against image/audio/video embeddings)
- Sub-second latency requirements on large memory sets

### Existing Setup

| Component | Value |
|---|---|
| Index | `hivefind-memory-v2` |
| Dimensions | 3072 (Gemini Embedding 2, MRL-compressible to 1536/768) |
| Metric | Cosine |
| Embedding model | `gemini-embedding-2-preview` |
| Embed service | `services/embed/` (FastAPI, port 8766) |
| Status | Available but not primary. Embed service shut down 2026-03-26. |

### Metadata Schema (Pinecone)

```
type: string (preference, pattern, outcome, correction, relationship)
agent: string
domain: string
confidence: float
timestamp: datetime
tags: string[]
entity_refs: string[]
modality: string (text, image, audio, video, pdf, multimodal)
```

These fields mirror the Notion DB properties. If Pinecone fallback is activated, a sync pipeline copies new Notion entries to Pinecone with embeddings generated by the embed service.

### Sync Pipeline (If Activated)

```
Notion Memory DB -> Notion webhook -> Embed service generates vector -> Upsert to Pinecone
```

This pipeline only needs to be built if Notion semantic search proves insufficient during Phase 1.5 validation.

---

## Open Questions

1. **Memory visualization:** Should there be a dashboard showing what the system has learned. Useful for trust-building but adds scope.

2. **Export/portability:** Notion export covers the primary store. If Pinecone fallback is active, need a separate export strategy for vectors.

3. **Demo mode:** For client demos, should there be a way to show the memory system without exposing personal data.

4. **Notion AI search limits:** Notion's semantic search is good for hundreds to low thousands of entries. If memory grows past 10K entries, Pinecone fallback may become the primary path. Monitor and reassess.

---

*Version: 2.0*
*Created: December 2025*
*Updated: April 2026 (Notion-native memory; Pinecone demoted to fallback)*
*Owners: Evelyn (Memory) -- curation and retrieval; Evelyn (EA) -- consumer only*
