# Content Publisher Workflow Template

**Pattern:** Schedule → Generate → Adapt → Publish

---

## Purpose

Automate social media and content publishing. Used by:
- **Ada** - Puzzlehouse social media (Instagram, Facebook, LinkedIn, TikTok)
- **Dale** - Haze Gray LinkedIn content and thought leadership

---

## Trigger Configuration

### In Relay.app

| Setting | Value |
|---------|-------|
| Type | Schedule Trigger |
| Frequency | Daily (weekdays) or custom |
| Time | Platform-optimal posting times |

### Agent-Specific Schedule

| Agent | Platform | Frequency | Time |
|-------|----------|-----------|------|
| Ada | Instagram | 4x/week | 9:00 AM |
| Ada | Facebook | 3x/week | 9:00 AM |
| Ada | LinkedIn | 2x/week | 8:00 AM |
| Ada | TikTok | 3x/week | 12:00 PM |
| Dale | LinkedIn | 2x/week | 7:30 AM |

---

## Step-by-Step Build

### Step 1: Add Schedule Trigger

1. Create new workflow
2. Select **Schedule Trigger**
3. Set to weekdays at specified time
4. Name: "[Agent] [Platform] Content Publish"

### Step 2: Add Product/Content Selection

**For Ada (Product-Based Content):**
```
Integration: Shopify
Action: Get Products
Filter: In stock, featured, or rotation logic
Return: Product name, description, image, SKU
```

**For Dale (Thought Leadership):**
```
Integration: Notion
Action: Query Content Queue
Filter: Status = "Approved", Platform = "LinkedIn"
Return: Post content, pillar, outreach targets
```

### Step 3: Add Inventory/Context Check

```
Integration: Shopify (Ada only)
Action: Check Inventory Level
If stock < threshold: Skip or select alternate product
```

### Step 4: Add AI Content Generation

**Ada's Instagram Prompt:**
```
Generate an Instagram caption for this product:

Product: {{product.name}}
Description: {{product.description}}
Brand: Puzzlehouse - Maritime heritage, quality puzzles, puzzle community

Write in Ada's voice:
- Warm, unhurried, subtly witty
- Never salesy or breathless
- Sophisticated but accessible
- Meditative, not manic

Include:
- Caption (50-150 words)
- 5-8 relevant hashtags
- No more than 3 emojis

Do not use: "OMG", "HUGE SALE", urgent language
```

**Dale's LinkedIn Prompt:**
```
Generate a LinkedIn post on this topic:

Topic: {{content.topic}}
Pillar: {{content.pillar}}
Key points: {{content.key_points}}

Write in JD's voice:
- Direct, substantive, point of view
- No empty thought leadership clichés
- Concrete examples and insights
- Ends with engagement prompt or takeaway

Length: 150-300 words
Format: Use line breaks for readability
```

### Step 5: Add Platform Adaptation (Multi-Platform)

If publishing to multiple platforms:

```
Path: By Platform
├→ Instagram: Format for visual + caption + hashtags
├→ Facebook: Friendly, slightly longer, community-focused
├→ LinkedIn: Professional, thought leadership angle
└→ TikTok: Casual, behind-the-scenes tone
```

### Step 6: Add Publishing Step

**Option A: Direct Publishing (if integration available)**
```
Integration: Meta Business Suite / LinkedIn / etc.
Action: Create Post
Content: {{ai_content}}
Image: {{product.image}} or {{content.image}}
```

**Option B: Queue to Scheduling Tool**
```
Integration: Buffer / Later / Notion Queue
Action: Add to Queue
Platform: {{platform}}
Scheduled Time: {{optimal_time}}
Content: {{ai_content}}
```

### Step 7: Add Activity Logging

```
Integration: Notion
Action: Create Page
Database: Content Calendar
Properties:
  - Post Title: {{content_summary}}
  - Platform: {{platform}}
  - Status: Published / Scheduled
  - Product: {{product.name}} (if applicable)
  - Publish Date: {{now}}
  - Content: {{ai_content}}
```

---

## Complete Workflow Diagram

```
┌─────────────────────────┐
│   Schedule Trigger      │
│   (9:00 AM weekdays)    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Get Content/Product   │
│   (Shopify or Notion)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Check Inventory       │
│   (Skip if out of stock)│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI: Generate Content  │
│   (Platform-specific)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Path: By Platform     │
│   (Adapt for each)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Publish / Queue       │
│   (Meta/LinkedIn/etc)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Log to Notion         │
│   (Content Calendar)    │
└─────────────────────────┘
```

---

## Quality Controls

### Content Variation

Avoid repetitive patterns:
- Rotate product categories
- Track last posted products (no repeat within 7 days)
- Vary opening sentence structures
- Mix content types (70% product, 30% lifestyle/educational)

### Brand Safety

Built into AI prompts:
- Never post political content
- Never use urgent/salesy language
- Never claim UGC without attribution
- Never make claims not on website
- Max 3 emojis per post
- Max 8 hashtags (Instagram)

---

## Test Checklist

- [ ] Schedule trigger fires correctly
- [ ] Product/content selection works
- [ ] Inventory check skips out-of-stock items
- [ ] AI content matches agent voice
- [ ] Platform formatting correct
- [ ] Publishing/queueing succeeds
- [ ] Notion log created
- [ ] No duplicate products within 7 days

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Content feels robotic | AI prompt too generic | Add more voice examples |
| Wrong product selected | Rotation logic broken | Check selection criteria |
| Post not published | Integration disconnected | Re-authenticate platform |
| Inventory error | Shopify API issue | Verify connection |
| Missing hashtags | Prompt didn't specify | Update AI prompt |

---

## Variations

### "Approval Required" Version

Add human review before publishing:

```
[AI: Generate Content]
    ↓
[Human-in-the-Loop: Approve/Edit]
    ↓
[Path: If Approved]
    ├→ YES: [Publish]
    └→ NO: [Revise or Skip]
```

### "Performance-Based Selection" Version

Select products based on past performance:

```
[Notion: Query Past Posts]
    ↓
[AI: Identify top performers]
    ↓
[Select similar products]
```

---

*Template Version: 1.0 | December 2025*
