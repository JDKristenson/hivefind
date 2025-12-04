# Notion Database Files

CSV files ready for direct import into Notion to create working databases.

---

## How to Import

1. Open Notion
2. Create a new page (this will be your AI Crew Hub)
3. For each CSV file:
   - Type `/database` and select "Table - Inline"
   - Click the `...` menu on the table
   - Select "Merge with CSV"
   - Upload the CSV file
4. Rename the database to match the file name
5. Set up Relations between databases (see below)

---

## Database Files

| File | Purpose | Records |
|------|---------|---------|
| `Agent_Registry.csv` | Master roster of all 18 agents | 18 |
| `Activity_Log.csv` | Real-time agent activity logging | Sample data |
| `Exception_Queue.csv` | Issues requiring human review | Sample data |
| `Exception_Types.csv` | Reference table of exception categories | 16 |

---

## Database Relationships

After importing, create these Relations in Notion:

### Agent Registry
- No relations needed (this is the master table)

### Activity Log
- **Agent** → Relation to Agent Registry (by Name)
- **Related Agent** → Relation to Agent Registry (by Name)

### Exception Queue
- **Agent** → Relation to Agent Registry (by Name)
- **Exception Type** → Relation to Exception Types
- **Escalated To** → Relation to Agent Registry (by Name)
- **Resolved By** → Relation to Agent Registry (by Name)

### Exception Types
- **Applies To Agents** → Relation to Agent Registry (multi-select or formula)

---

## Column Types (After Import)

Notion will auto-detect most types. Adjust these manually:

### Agent Registry
| Column | Type | Notes |
|--------|------|-------|
| Name | Title | Primary key |
| Status | Select | Options: Active, Inactive, Maintenance |
| Authority Level | Select | 1-Principal, 2-Coordination, 3-Supervisor, 4-Domain Agent |
| Domain | Select | Coordination, Personal, Haze Gray, Puzzlehouse |
| Error Count (30d) | Number | |
| Uptime % | Number | Format as percentage |
| Health Score | Number | 0-100 scale |
| Last Run | Date | |
| Last Error | Date | |

### Activity Log
| Column | Type | Notes |
|--------|------|-------|
| Timestamp | Date | Include time |
| Status | Select | Online, Offline, Error, Maintenance |
| Action Type | Select | Health Check, Briefing, Sync, Triage, etc. |
| Duration (sec) | Number | |

### Exception Queue
| Column | Type | Notes |
|--------|------|-------|
| ID | Title | Auto-generated format: EX-XXX |
| Severity | Select | Critical, High, Medium, Low |
| Status | Select | Open, Pending Review, In Progress, Resolved, Closed |
| Timestamp | Date | Include time |
| Resolved At | Date | Include time |

---

## Recommended Views

### Agent Registry Views
1. **All Agents** (Table) - Default view
2. **By Domain** (Board) - Group by Domain column
3. **Health Dashboard** (Table) - Filter: Status = Active, Sort by Health Score
4. **Needs Attention** (Table) - Filter: Health Score < 90 OR Error Count > 0

### Activity Log Views
1. **Recent Activity** (Table) - Sort by Timestamp desc, limit 50
2. **By Agent** (Board) - Group by Agent
3. **Errors Only** (Table) - Filter: Status = Error OR Last Error Time is not empty

### Exception Queue Views
1. **Open Exceptions** (Table) - Filter: Status != Resolved AND Status != Closed
2. **My Review Queue** (Table) - Filter: Escalated To = JD AND Status = Pending Review
3. **By Severity** (Board) - Group by Severity
4. **By Agent** (Board) - Group by Agent

---

## Automation Suggestions

Once databases are set up, consider these Notion automations:

1. **New Exception Alert**
   - Trigger: New item in Exception Queue with Severity = Critical or High
   - Action: Send notification

2. **Health Score Warning**
   - Trigger: Agent Registry item updated, Health Score < 80
   - Action: Create Exception Queue item

3. **Daily Summary**
   - Trigger: Daily at 6 AM
   - Action: Create page summarizing yesterday's Activity Log

---

## Integration Points

These databases connect to external systems via:

| System | Connection | Purpose |
|--------|------------|---------|
| n8n | Notion API | Agents write to Activity Log and Exception Queue |
| Relay.app | Notion integration | Sync between systems |
| Zapier/Make | Notion connector | Backup automation option |

---

## Sample Data

The CSV files include sample data to demonstrate structure. After import:
- Keep Agent Registry data (it's your real roster)
- Clear sample rows from Activity Log (real data comes from n8n)
- Clear sample rows from Exception Queue (real exceptions come from agents)
- Keep Exception Types (this is your reference configuration)

---

*Import these files to have a working AI Crew command center from day one.*
