# Email Handler Workflow Template

**Pattern:** Event → Categorize → Route → Respond

---

## Purpose

Process incoming emails with AI categorization and routing. Used by:
- **Clara** - Customer support email handling
- **Helena** - Lead inquiry processing
- **Hamilton** - Client communication tracking
- **Evelyn (EA)** - Executive email triage

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Email Trigger or Schedule (polling) |
| Source | Support inbox / Business inbox |
| Frequency | Real-time or Every 15-30 minutes |

### Agent-Specific Configuration

| Agent | Email Source | Processing |
|-------|-------------|------------|
| Clara | support@puzzlehouse.com | Real-time response |
| Helena | inquiries@hazegray.com | Lead qualification |
| Hamilton | Client-specific domains | Commitment tracking |
| Evelyn | JD's inbox | Triage and summarize |

---

## Step-by-Step Build

### Step 1: Add Email Trigger

1. Create new workflow
2. Select **Email Trigger** or **Schedule + Gmail Query**
3. Configure inbox to monitor
4. Name: "[Agent] Email Handler"

### Step 2: Add AI Categorization Step

```
Integration: AI Step (Agent)
Action: Categorize incoming email

Prompt Template:
"Categorize this email:

From: {{email.from}}
Subject: {{email.subject}}
Body: {{email.body}}

Categories:
- ORDER_STATUS: Questions about existing orders
- COMPLAINT: Issues, problems, dissatisfaction
- RETURN_REQUEST: Return or exchange requests
- PRODUCT_QUESTION: Questions about products
- URGENT: Requires immediate attention
- SPAM: Junk or irrelevant

Return category and confidence (0-1)."
```

### Step 3: Add Shopify/Context Lookup (if applicable)

For customer service agents:
```
Integration: Shopify
Action: Search Customers
Query: {{email.from}}
Return: Order history, customer status
```

### Step 4: Add Path Routing

Create paths based on category:

```
Path 1: ORDER_STATUS
  → Shopify: Get order details
  → AI: Generate status response
  → Gmail: Send response

Path 2: COMPLAINT
  → AI: Generate empathetic response with solution
  → Notion: Log complaint
  → Gmail: Send response

Path 3: RETURN_REQUEST
  → AI: Validate against policy
  → Shopify: Initiate return (if approved)
  → Gmail: Send instructions

Path 4: URGENT
  → Slack: Alert human
  → Notion: Log for follow-up

Path 5: SPAM
  → Archive (no action)
```

### Step 5: Add Response Generation

**AI Prompt for Response:**
```
Generate a response to this customer email.

Email: {{email.body}}
Category: {{category}}
Customer History: {{shopify.customer}}
Order Details: {{shopify.orders}}

Use the voice and tone specified in your agent instructions.
Be warm, helpful, and solution-focused.
Never blame the customer or hide behind policy.
```

### Step 6: Add Notion Logging

```
Integration: Notion
Action: Create Page
Database: Support Log (or appropriate log)
Properties:
  - Customer: {{email.from}}
  - Subject: {{email.subject}}
  - Category: {{category}}
  - Status: Responded / Escalated
  - Response: {{ai_response}}
  - Timestamp: {{now}}
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Email Trigger         │
│   (New email received)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI: Categorize        │
│   (ORDER/COMPLAINT/etc) │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Context Lookup        │
│   (Shopify/CRM)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Path: By Category     │
├───────────┬─────────────┤
│ ORDER     │ COMPLAINT   │
│   │       │      │      │
│   ▼       │      ▼      │
│ Get order │ Log + Alert │
│ details   │             │
└───────────┴─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI: Generate Response │
│   (Agent voice)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Gmail: Send Response  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Notion: Log           │
└─────────────────────────┘
```

---

## Test Checklist

- [ ] Email trigger receives test email
- [ ] Categorization returns correct category
- [ ] Context lookup retrieves customer data
- [ ] Path routing works for each category
- [ ] Response generated in agent's voice
- [ ] Email sent successfully
- [ ] Interaction logged to Notion
- [ ] Escalation alerts human (for urgent)

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Emails not triggering | Integration disconnected | Re-authenticate Gmail |
| Wrong category | AI prompt too vague | Add more examples |
| Generic responses | Missing context | Ensure customer lookup working |
| Response too slow | Too many API calls | Optimize step sequence |
| Missing logs | Notion step failing | Check database schema |

---

## Variations

### "Human Approval" Version

Add human-in-the-loop before sending:

```
[AI: Generate Response]
    ↓
[Human-in-the-Loop: Approve/Edit]
    ↓
[Gmail: Send Response]
```

### "Escalation Threshold" Version

Auto-escalate based on customer value:

```
[Context Lookup]
    ↓
[Path: If VIP Customer]
    ├→ YES: [Alert + Priority Response]
    └→ NO: [Standard Response]
```

---

*Template Version: 1.0 | December 2025*
