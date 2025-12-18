# Relay.app Workflow Builder Template

This template provides the standard format for building Hivefind workflows in Relay.app.

---

## Workflow Naming Convention

**Format**: `[Domain]_[Agent]_[Function]`

**Examples**:
- `Coordination_Xavier_HealthCheck`
- `Personal_Evelyn_EmailTriage`
- `HazeGray_Helena_LeadQualification`
- `Puzzlehouse_Ada_ContentScheduling`

---

## Standard Workflow Structure

Every Hivefind workflow in Relay.app follows this pattern:

```
┌─────────────┐
│   TRIGGER   │  ← Schedule, Webhook, or Manual
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  START LOG  │  ← Write to Activity Log (Notion)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ MAIN LOGIC  │  ← Agent-specific processing
│   (Nodes)   │
└──────┬──────┘
       │
       ├────────────┐
       │            ▼
       │    ┌─────────────┐
       │    │ERROR HANDLER│  ← Catch errors → Create Exception
       │    └─────────────┘
       │
       ▼
┌─────────────┐
│   END LOG   │  ← Write completion to Activity Log
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   HANDOFF   │  ← Trigger next agent (if applicable)
└─────────────┘
```

---

## Template Structure

Each workflow spec in `/workflows/` follows this structure:

```markdown
# [Workflow Name] - Relay.app Build Guide

## Quick Reference
- **Workflow ID**: [Domain]_[Agent]_[Function]
- **Agent**: [Agent name]
- **Domain**: [Domain]
- **Trigger Type**: [Schedule/Webhook/Manual/Agent]
- **Estimated Build Time**: [X minutes]

---

## NODE-BY-NODE BUILD INSTRUCTIONS

### Node 1: Trigger
**Type**: [Trigger type]
**Configuration**:
- Setting 1: [Value]
- Setting 2: [Value]

**Screenshot Reference**: [If applicable]

---

### Node 2: Start Log
**Type**: Notion - Create Database Item
**Database**: Activity Log
**Fields**:
| Property | Value |
|----------|-------|
| Timestamp | `{{now}}` |
| Agent | [Agent name] |
| Action | [Workflow name] |
| Status | "Started" |

---

### Node 3-N: Main Logic
[Detailed node-by-node instructions]

---

### Error Handler Node
**Type**: Error Trigger
**On Error**:
1. Create Exception Queue item
2. Notify Xavier (if critical)
3. Log error details

---

### End Log Node
**Type**: Notion - Update Database Item
**Update**:
| Property | Value |
|----------|-------|
| Status | "Completed" |
| Duration | `{{duration}}` |
| Result | [Summary] |

---

## CONNECTIONS

### Input Connections
[What triggers this workflow]

### Output Connections
[What this workflow triggers]

---

## TEST PROCEDURE

### Step 1: Manual Test
[Instructions]

### Step 2: Integration Test
[Instructions]

### Step 3: End-to-End Test
[Instructions]

---

## TROUBLESHOOTING

### Node-Specific Issues

#### Node [X]: [Name]
| Issue | Cause | Solution |
|-------|-------|----------|
| [Problem] | [Why] | [Fix] |

---

## ROLLBACK PROCEDURE

If the workflow fails in production:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Common Node Patterns

### Pattern 1: Notion Database Read
```
Node Type: Notion - Query Database
Database: [Database name]
Filter: [Filter conditions]
Sort: [Sort order]
Output: items[]
```

### Pattern 2: Notion Database Write
```
Node Type: Notion - Create Database Item
Database: [Database name]
Properties:
  - Property 1: {{value}}
  - Property 2: {{value}}
```

### Pattern 3: AI Processing
```
Node Type: AI Agent
Agent: [Agent name]
Input: {{previous_node.output}}
Instructions: [Context-specific instructions]
Output: response
```

### Pattern 4: Conditional Branch
```
Node Type: IF
Condition: {{value}} [operator] [compare]
True Branch: → [Next node]
False Branch: → [Alternative node]
```

### Pattern 5: HTTP Request
```
Node Type: HTTP Request
Method: [GET/POST/PUT]
URL: [Endpoint]
Headers: [Headers object]
Body: [Request body]
```

### Pattern 6: Loop/Iterator
```
Node Type: Loop
Input Array: {{items}}
For Each: item
  → [Processing nodes]
Output: processed_items[]
```

---

## Error Handling Patterns

### Try-Catch Pattern
```
┌─────────────┐
│  Try Block  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
Success  Error
   │       │
   ▼       ▼
[Continue] [Error Handler]
```

### Retry Pattern
```
Retry Count: 3
Retry Delay: Exponential (2s, 4s, 8s)
On Final Failure: → Exception Queue
```

### Graceful Degradation
```
If integration fails:
1. Log the failure
2. Use cached data if available
3. Mark task as "Partial"
4. Continue workflow
```

---

## Logging Standards

### Activity Log Entry Format
```json
{
  "timestamp": "ISO 8601",
  "agent": "Agent Name",
  "workflow": "Workflow ID",
  "action": "Action description",
  "status": "Started|In Progress|Completed|Failed",
  "duration_ms": 0,
  "input_summary": "Brief input description",
  "output_summary": "Brief output description",
  "error": null
}
```

### Exception Queue Entry Format
```json
{
  "timestamp": "ISO 8601",
  "agent": "Agent Name",
  "workflow": "Workflow ID",
  "exception_type": "Type from Exception_Types",
  "severity": "Low|Medium|High|Critical",
  "description": "What happened",
  "context": "Relevant details",
  "escalation_path": "Xavier|Aurelius|Clare|User",
  "status": "Open",
  "resolution": null
}
```

---

## Quality Checklist

- [ ] All nodes connected properly
- [ ] Start Log node present
- [ ] End Log node present
- [ ] Error handler configured
- [ ] Test with sample data
- [ ] Verify Notion logging works
- [ ] Check rate limits respected
- [ ] Confirm handoffs work
- [ ] Document any deviations from template
