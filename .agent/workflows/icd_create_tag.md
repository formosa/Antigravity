---
type: workflow
name: "Create ICD Tag"
slug: /create_icd
description: "Author ICD tag with validation."
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
    description: "Parent tag ID (SAD-xxx or NFR-xxx)"
    required: true
context:
  - ".agent/rules/icd_interface_contracts.md"
  - ".agent/knowledge/sources/concepts/tier_icd.md"
outputs:
  - name: tag_id
    type: string
    description: "Generated tag ID (e.g., ICD-a1b2c3d4)"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create ICD Tag

## Phase 1: Route
**@icd_dataengineer**: Draft ICD content. Include schema or contract specification.

// turbo
## Phase 2: Validate
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/validate_tier_compliance.py" --tier ICD --content "{{draft_content}}"
```

// turbo
## Phase 3: Create
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier ICD --title "{{inputs.title}}" --parent "{{inputs.parent}}" --description "{{inputs.description}}"
```
