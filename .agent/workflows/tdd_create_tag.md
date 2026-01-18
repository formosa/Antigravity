---
type: workflow
name: "Create TDD Tag"
slug: /create_tdd
description: "Author TDD tag with validation."
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
    description: "Parent tag ID (SAD-xxx or ICD-xxx)"
    required: true
context:
  - ".agent/rules/tdd_structural_blueprints.md"
  - ".agent/knowledge/sources/concepts/tier_tdd.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., TDD-a1b2c3d4)"
on_finish: "suggest_followup: /create_isp"
---

# Workflow: Create TDD Tag

## Phase 1: Route
**@tdd_designer**: Draft TDD content. Include class/method structure.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier TDD --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier TDD --title "{{inputs.title}}" --parent "{{inputs.parent}}" --description "{{inputs.description}}"
```
