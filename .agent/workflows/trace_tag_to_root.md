---
type: workflow
name: "Trace Tag to Root"
slug: /trace_tag
description: "Display citation chain from tag to BRD root."
mode: autonomous
inputs:
  - name: tag_id
    type: string
    description: "Tag ID to trace (e.g., TDD-a1b2c3d4)"
    required: true
context:
  - ".agent/knowledge/sources/protocols/traceability_chain.md"
  - ".agent/knowledge/sources/concepts/information_flow.md"
outputs:
  - name: chain
    type: array
  - name: visualization
    type: string
on_finish: "suggest_followup: /resolve_orphan"
---

# Workflow: Trace Tag to Root

// turbo
## Phase 1: Extract Chain
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/extract_citations.py" --tag-id "{{inputs.tag_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --recursive
```

// turbo
## Phase 2: Visualize
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/visualize_traceability.py" --tag-id "{{inputs.tag_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --format mermaid
```
