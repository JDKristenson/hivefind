# Hivefind Relay - Troubleshooting Guide

Common issues and solutions when building and running Hivefind agents in Relay.app.

---

## Quick Diagnostics

### Workflow Not Running

| Symptom | Check | Solution |
|---------|-------|----------|
| Schedule not triggering | Trigger configuration | Verify time/timezone settings |
| Webhook not receiving | Endpoint URL | Confirm URL in source system |
| No output produced | Integration auth | Re-authenticate connected apps |
| Partial execution | Step failure | Check individual step logs |

### AI Steps Not Working

| Symptom | Check | Solution |
|---------|-------|----------|
| Generic output | System prompt | Verify agent prompt is pasted |
| Wrong format | Output instructions | Add explicit format requirements |
| Truncated response | Token limit | Increase max tokens |
| Timeout | Processing time | Simplify prompt or add timeout |

---

## Integration-Specific Issues

### Notion

| Issue | Cause | Solution |
|-------|-------|----------|
| Database not found | Wrong database ID | Copy ID from URL, not name |
| Properties not matching | Schema mismatch | Verify property names and types |
| Query returns empty | Filter too strict | Broaden filter criteria |
| Create fails | Missing required fields | Check all required properties |
| Relation not linking | Wrong database reference | Verify relation configuration |

**Common Notion Property Types:**
- Title → Use for main identifier
- Select → Single choice from options
- Multi-select → Multiple choices
- Date → Dates and datetimes
- Number → Numeric values
- Rich Text → Longer text content
- Relation → Links to other databases

### Gmail

| Issue | Cause | Solution |
|-------|-------|----------|
| Can't send email | Auth expired | Re-authenticate integration |
| Wrong recipient | Variable not resolving | Check variable syntax {{email}} |
| Formatting broken | HTML not supported | Use plain text or markdown |
| Trigger not firing | Label/filter wrong | Verify Gmail filter configuration |
| Missing attachments | Not supported | Use Drive link instead |

### Google Calendar

| Issue | Cause | Solution |
|-------|-------|----------|
| Events not found | Wrong calendar selected | Verify calendar ID |
| Time zone wrong | Mismatch | Set explicit timezone |
| Conflicts not detected | Query range too narrow | Extend date range |
| Event creation fails | Missing required fields | Include title, start, end |

### Shopify

| Issue | Cause | Solution |
|-------|-------|----------|
| Products not returned | API permissions | Check Shopify app scopes |
| Inventory incorrect | Variant-level data | Query at variant level |
| Order lookup fails | Order ID format | Use numeric ID, not name |
| Customer not found | Email case sensitivity | Normalize email before search |

### Slack

| Issue | Cause | Solution |
|-------|-------|----------|
| Message not sent | Wrong channel | Verify channel name/ID |
| Bot not in channel | Not added | Invite bot to channel |
| Formatting broken | Markdown mismatch | Use Slack's block kit format |
| DM not delivered | User ID required | Use user ID, not username |

---

## AI Step Troubleshooting

### Prompt Issues

| Problem | Symptom | Solution |
|---------|---------|----------|
| Generic output | Doesn't match agent voice | Add voice examples to prompt |
| Wrong format | Missing sections | Add explicit format template |
| Hallucinations | Invents data | Add "only use provided data" |
| Too verbose | Long, rambling | Add length constraint |
| Too terse | Missing detail | Request specific elements |

### Prompt Template

```
You are [Agent Name], [Agent Title].

[System prompt from agent spec]

## TASK
[Specific task for this step]

## INPUT DATA
{{previous_step_data}}

## OUTPUT REQUIREMENTS
- Format: [specific format]
- Length: [word/character limit]
- Include: [required elements]
- Exclude: [what not to include]

## EXAMPLES
[Good example output]
```

### Model Selection

| Use Case | Recommended Model | Rationale |
|----------|------------------|-----------|
| Complex reasoning | GPT-4o / Claude | Better analysis |
| Simple tasks | GPT-4o-mini | Faster, cheaper |
| Long context | Claude | Extended context window |
| Consistency critical | Lower temperature (0.3) | More predictable |
| Creativity needed | Higher temperature (0.7) | More varied |

---

## Path/Routing Issues

### Conditional Logic

| Issue | Cause | Solution |
|-------|-------|----------|
| Wrong path taken | Condition syntax | Verify comparison operators |
| Path never triggered | Value mismatch | Check data types (string vs number) |
| All paths skip | No matching condition | Add default/else path |

### Common Conditions

```
# String comparison
{{category}} == "ORDER_STATUS"

# Numeric comparison
{{amount}} > 50

# Contains
{{text}} contains "urgent"

# Empty check
{{value}} is not empty

# Boolean
{{is_vip}} == true
```

---

## Debugging Strategies

### 1. Isolate the Problem

Test each step independently:
1. Remove all steps after the failing one
2. Add a temporary output step
3. Verify data at that point
4. Add steps back one at a time

### 2. Check Variables

Common variable issues:
- Wrong syntax: `{variable}` vs `{{variable}}`
- Nested access: `{{step.data.field}}` vs `{{step_data_field}}`
- Array access: `{{items[0]}}` vs `{{items.0}}`

### 3. Use Test Runs

Before deploying:
1. Use manual trigger
2. Provide sample data
3. Verify each step output
4. Check final result

### 4. Monitor Logs

After deployment:
- Check workflow run history
- Review step-by-step execution
- Identify where failures occur
- Note error messages

---

## Agent-Specific Issues

### Xavier (Fleet Operations)

| Issue | Cause | Solution |
|-------|-------|----------|
| Can't monitor other agents | No access to their logs | Ensure Activity Log shared |
| Health check incomplete | Missing integrations | Connect all required services |
| Grades incorrect | Activity data incomplete | Verify all agents log activity |

### Aurelius (Charter)

| Issue | Cause | Solution |
|-------|-------|----------|
| Reflections generic | Charter empty | Populate Charter database |
| Missing principles | Domain not tagged | Add domain tags to principles |
| Weekly synthesis blank | No activity logged | Verify agent Activity Log entries |

### Clara (Customer Support)

| Issue | Cause | Solution |
|-------|-------|----------|
| Can't find order | Shopify not connected | Verify Shopify integration |
| Response tone wrong | System prompt missing | Paste full Clara prompt |
| Escalations not routing | Path logic broken | Check escalation thresholds |

### Ada (Social Media)

| Issue | Cause | Solution |
|-------|-------|----------|
| Content repetitive | No rotation logic | Track posted products |
| Wrong platform format | Missing adaptation | Add platform-specific formatting |
| Hashtags missing | Prompt incomplete | Add hashtag requirements |

### Franklin (Operations)

| Issue | Cause | Solution |
|-------|-------|----------|
| Inventory alerts not firing | Thresholds not set | Configure reorder points |
| Thank-you notes generic | Product not captured | Verify Shopify webhook data |
| AP reminders missing | Due dates not entered | Populate AP database |

---

## Performance Optimization

### Reduce Execution Time

1. **Parallelize independent queries**
   - Query Notion and Shopify simultaneously
   - Don't chain unnecessarily

2. **Minimize AI calls**
   - Combine related tasks into one prompt
   - Cache repeated lookups

3. **Filter early**
   - Apply filters at query level
   - Don't fetch everything then filter

### Reduce Costs

1. **Use appropriate model**
   - GPT-4o-mini for simple tasks
   - Full models only when needed

2. **Limit context**
   - Don't include unnecessary data in prompts
   - Summarize long inputs

3. **Avoid redundant runs**
   - Check if action needed before executing
   - Skip workflows when no new data

---

## Getting Help

### Relay.app Resources

- [Relay.app Documentation](https://docs.relay.app/)
- [AI Steps Guide](https://docs.relay.app/ai/ai-steps)
- [Integration Guides](https://docs.relay.app/integrations)

### Hivefind Resources

- ARCHITECTURE.md - System design overview
- Individual agent specs - Section 6 (Troubleshooting)
- Workflow templates - Troubleshooting sections

### Debug Information to Collect

When reporting issues, include:
1. Agent name and workflow name
2. Trigger type and configuration
3. Step where failure occurs
4. Error message (exact text)
5. Sample input data (sanitized)
6. Expected vs. actual output

---

*Troubleshooting Guide Version: 1.0 | December 2025*
