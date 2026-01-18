---
type: workflow
name: "Create NFR Tag"
slug: /create_nfr
description: "Author NFR tag with validation."
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
    description: "Parent tag ID (BRD-xxx)"
    required: true
context:
  - ".agent/rules/nfr_numeric_targets.md"
  - ".agent/knowledge/sources/concepts/tier_nfr.md"
  - ".agent/knowledge/sources/constraints/nfr_numeric_constraints.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., NFR-a1b2c3d4)"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create NFR Tag

## Phase 1: Route
**@nfr_enforcer**: Draft NFR content. Ensure numeric constraints are specified.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier NFR --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier NFR --title "{{inputs.title}}" --parent "{{inputs.parent}}" --description "{{inputs.description}}"
```
