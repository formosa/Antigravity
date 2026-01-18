---
type: workflow
name: "Create SAD Tag"
slug: /create_sad
description: "Author SAD tag with validation."
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
    description: "Parent tag ID (FSD-xxx)"
    required: true
context:
  - ".agent/rules/sad_architecture_topology.md"
  - ".agent/knowledge/sources/concepts/tier_sad.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., SAD-a1b2c3d4)"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create SAD Tag

## Phase 1: Route
**@sad_architect**: Draft SAD content. Include topology and architectural patterns.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier SAD --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier SAD --title "{{inputs.title}}" --parent "{{inputs.parent}}" --description "{{inputs.description}}"
```
