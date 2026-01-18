---
type: workflow
name: "Create BRD Tag"
slug: /create_brd
description: "Author BRD tag with validation."
mode: autonomous
inputs:
  - name: title
    type: string
    required: true
  - name: description
    type: string
    required: true
context:
  - ".agent/rules/brd_technology_agnostic.md"
  - ".agent/rules/brd_measurable_metrics.md"
  - ".agent/rules/brd_stakeholder_focus.md"
  - ".agent/knowledge/sources/concepts/tier_brd.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., BRD-a1b2c3d4)"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create BRD Tag

## Phase 1: Route
**@brd_strategist**: Draft BRD content. Ensure technology-agnostic language and measurable business metrics.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier BRD --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier BRD --title "{{inputs.title}}" --description "{{inputs.description}}"
```
