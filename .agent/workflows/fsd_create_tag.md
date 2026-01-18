---
type: workflow
name: "Create FSD Tag"
slug: /create_fsd
description: "Author FSD tag with validation."
mode: autonomous
inputs:
  - name: title
    type: string
    required: true
  - name: description
    type: string
    required: true
  - name: parent
    type: string
    description: "Parent tag ID (BRD-xxx or NFR-xxx)"
    required: true
context:
  - ".agent/rules/fsd_behavioral_specs.md"
  - ".agent/knowledge/sources/concepts/tier_fsd.md"
  - ".agent/knowledge/sources/constraints/fsd_no_implementation.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., FSD-a1b2c3d4)"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create FSD Tag

## Phase 1: Route
**@fsd_analyst**: Draft FSD content. Describe behavior without implementation details.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier FSD --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier FSD --title "{{inputs.title}}" --parent "{{inputs.parent}}" --description "{{inputs.description}}"
```
