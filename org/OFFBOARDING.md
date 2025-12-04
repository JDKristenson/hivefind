# Agent Offboarding Checklist

Use this checklist when removing an agent from the Hivefind ecosystem.

---

## Decision Phase

Before proceeding with removal, validate the decision:

### 1. Reason for Removal

- [ ] **Document the reason:**
  - [ ] Not adding value (metrics below threshold)
  - [ ] Causing more problems than solving
  - [ ] Functionality absorbed by another agent
  - [ ] Domain no longer relevant
  - [ ] Persistent errors that can't be fixed
  - [ ] Cost/complexity not justified
  - [ ] Other: ___________

- [ ] **Evidence documented:**
  | Metric/Issue | Expected | Actual | Duration |
  |--------------|----------|--------|----------|
  |              |          |        |          |

- [ ] **Alternatives considered:**
  - [ ] Can the agent be fixed rather than removed?
  - [ ] Can responsibilities be reduced rather than eliminated?
  - [ ] Is this a temporary issue that will resolve?

**Gate:** If removal reason isn't clear and documented, pause and reconsider.

### 2. Impact Assessment

- [ ] **What gap will removal create?**

  Describe the gap: _________________________________________________

- [ ] **Who currently depends on this agent?**
  | Dependent | Dependency Type | Impact of Removal |
  |-----------|-----------------|-------------------|
  |           |                 |                   |

- [ ] **What tasks will go unhandled?**
  | Task | Frequency | Current Handler | New Handler |
  |------|-----------|-----------------|-------------|
  |      |           |                 |             |

- [ ] **Gap mitigation plan:**
  - [ ] Tasks absorbed by existing agent: ___________
  - [ ] Tasks returned to manual: ___________
  - [ ] Tasks eliminated (no longer needed): ___________
  - [ ] New agent will be created: ___________ (link to onboarding)

**Gate:** If gap cannot be mitigated acceptably, reconsider removal.

### 3. Approval

- [ ] **Xavier review:** Operational impact assessed
- [ ] **Aurelius review:** Values/accountability impact assessed (if relevant)
- [ ] **JD approval:** Removal authorized

  Approval date: ___________
  Approved by: ___________

---

## Preparation Phase

### 4. Communication Plan

- [ ] **Affected agents identified:**
  | Agent | How Affected | Notification Method |
  |-------|--------------|---------------------|
  |       |              |                     |

- [ ] **Timeline communicated:**
  - Removal date: ___________
  - Transition period: ___________ to ___________

### 5. Responsibility Transfer

For each responsibility being transferred:

| Responsibility | Current Owner | New Owner | Transfer Method | Verified? |
|----------------|---------------|-----------|-----------------|-----------|
|                |               |           |                 |           |

- [ ] **Transfer documentation created** for each responsibility
- [ ] **New owners confirmed** they can handle additional load
- [ ] **New owners' specs updated** with transferred responsibilities

### 6. Data Migration

- [ ] **Data inventory completed:**
  | Data Type | Location | Disposition |
  |-----------|----------|-------------|
  |           |          | Archive / Transfer / Delete |

- [ ] **Archive requirements:**
  - [ ] Activity logs archived
  - [ ] Performance history archived
  - [ ] Configuration documented

- [ ] **Data transferred** to new owners where applicable

---

## Execution Phase

### 7. Workflow Deactivation

- [ ] **Scheduled tasks disabled:**
  | Workflow | Cron/Trigger | Disabled? |
  |----------|--------------|-----------|
  |          |              |           |

- [ ] **Real-time triggers disabled:**
  | Trigger | Source | Disabled? |
  |---------|--------|-----------|
  |         |        |           |

- [ ] **Workflows set to inactive** (not deleted yet)

### 8. Integration Disconnection

- [ ] **API connections reviewed:**
  | Integration | Shared with Others? | Action |
  |-------------|---------------------|--------|
  |             |                     | Disconnect / Keep |

- [ ] **Credentials rotated** (if agent had unique credentials)

- [ ] **Webhook endpoints removed:**
  | Endpoint | Purpose | Removed? |
  |----------|---------|----------|
  |          |         |          |

### 9. Monitoring Updates

- [ ] **Xavier updated:**
  - [ ] Health monitoring removed for this agent
  - [ ] Alerts disabled
  - [ ] Performance tracking stopped

- [ ] **Dashboards updated:**
  - [ ] Agent removed from domain dashboard
  - [ ] Metrics archived

### 10. Documentation Updates

- [ ] **ARCHITECTURE.md updated:**
  - [ ] Agent removed from roster table
  - [ ] Org chart updated
  - [ ] Domain registry updated
  - [ ] Information flows updated

- [ ] **AGENT_ROSTER.md updated:**
  - [ ] Agent removed or marked as retired

- [ ] **PROTOCOLS.md updated:**
  - [ ] Decision authority matrix updated
  - [ ] Communication channels updated
  - [ ] Conflict scenarios updated (if any removed)

- [ ] **Affected agents' specs updated:**
  | Agent | Change Made | Verified? |
  |-------|-------------|-----------|
  |       |             |           |

---

## Verification Phase

### 11. Gap Testing

- [ ] **Test each transferred responsibility:**
  | Responsibility | New Owner | Test Result |
  |----------------|-----------|-------------|
  |                |           | Pass / Fail |

- [ ] **Test dependent agents:**
  | Agent | Test Performed | Result |
  |-------|----------------|--------|
  |       |                | Pass / Fail |

- [ ] **Test information flows:**
  - [ ] Data that used to flow through removed agent still reaches destination
  - [ ] Handoffs that involved removed agent work with new routing

### 12. Observation Period

- [ ] **48-hour observation:**
  - Start date: ___________
  - End date: ___________

- [ ] **Daily check during observation:**
  - [ ] Day 1: No unexpected issues
  - [ ] Day 2: No unexpected issues

- [ ] **Issues discovered:**
  | Issue | Severity | Resolution |
  |-------|----------|------------|
  |       |          |            |

---

## Cleanup Phase

### 13. Archive

- [ ] **Agent spec archived:**
  - [ ] Copy moved to `archive/` folder with date suffix
  - [ ] Original removed from active `specs/` folder

- [ ] **Workflow exports saved:**
  - [ ] n8n workflows exported as JSON
  - [ ] Stored in archive with agent spec

- [ ] **Final performance snapshot:**
  - [ ] Lifetime metrics documented
  - [ ] Reason for retirement documented

### 14. Permanent Removal

Only after successful observation period:

- [ ] **Workflows deleted** from n8n
- [ ] **Notion databases archived** or deleted
- [ ] **API credentials revoked** (if unique to this agent)

### 15. Final Documentation

- [ ] **Post-mortem documented:**
  - Why was this agent created?
  - Why is it being removed?
  - What did we learn?
  - How do we avoid this in future?

- [ ] **Lessons learned added to** `process/04-LESSONS-LEARNED.md`

---

## Post-Removal Review

### After 1 Week

- [ ] **Gap mitigation working?**
- [ ] **Dependent agents functioning normally?**
- [ ] **Any unexpected issues surfaced?**
- [ ] **User (JD) feedback on removal impact?**

### After 30 Days

- [ ] **Was removal the right decision?**
- [ ] **Any regrets or reconsiderations?**
- [ ] **System operating better, same, or worse without this agent?**

---

## Quick Reference: What Gets Removed

| Component | Location | Action |
|-----------|----------|--------|
| Agent spec | `specs/[domain]/` | Archive to `archive/` |
| Workflows | n8n | Export, then delete |
| Databases | Notion | Archive or delete |
| API credentials | `.env`, n8n credentials | Revoke if unique |
| Monitoring | Xavier config | Remove |
| Dashboard entries | Notion | Remove |
| Architecture docs | `docs/` | Update all references |
| Protocol docs | `org/` | Update all references |
| Roster | `docs/AGENT_ROSTER.md` | Remove or mark retired |

---

## Quick Reference: Red Flags

Pause if:

- ❌ Gap mitigation plan is incomplete
- ❌ Dependent agents haven't been updated
- ❌ No approval from JD
- ❌ Testing reveals failures in transferred responsibilities
- ❌ Observation period shows unexpected problems
- ❌ You're removing an agent to avoid fixing it (consider fixing first)

---

## Archive Structure

When archiving a retired agent:

```
archive/
└── [Agent Name] - Retired [YYYY-MM-DD]/
    ├── spec.md                    # Original spec
    ├── workflows/                 # Exported n8n workflows
    │   └── [workflow-name].json
    ├── metrics.md                 # Final performance snapshot
    ├── post-mortem.md            # Why retired, lessons learned
    └── data-export/              # Any relevant data exports
```

---

*A clean offboarding prevents orphaned dependencies and forgotten responsibilities. Do it right.*
