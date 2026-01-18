---
type: workflow
name: "Resolve Orphan Tag"
slug: /resolve_orphan
description: "Synthesize missing parent or child tags to complete traceability chains."
mode: autonomous
inputs:
  - name: orphan_tag_id
    type: string
    description: "ID of the orphan tag (e.g., TDD-a1b2c3d4)"
    required: true
  - name: direction
    type: string
    description: "'upward' or 'downward'"
    required: false
context:
  - ".agent/knowledge/sources/protocols/abstraction_upward.md"
  - ".agent/knowledge/sources/protocols/abstraction_downward.md"
  - ".agent/knowledge/sources/protocols/abstraction_lateral.md"
outputs:
  - name: created_tag_id
    type: string
  - name: resolution_type
    type: string
    description: "upward or downward"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Resolve Orphan Tag

## Phase 1: Analyze
// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/extract_citations.py" --tag-id "{{inputs.orphan_tag_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

## Phase 2: Determine Direction
- No `:links:` → upward (create parent)
- No children → downward (create children)
- `direction` input overrides

## Phase 3: Execute
**Upward**: Follow `.agent/knowledge/sources/protocols/abstraction_upward.md`
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier "{{parent_tier}}" --title "{{abstracted_title}}" --parent "{{grandparent_id}}"
```

**Downward**: Follow `.agent/knowledge/sources/protocols/abstraction_downward.md`

## Phase 4: Validate
// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_traceability_report.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --severity ERROR
```
