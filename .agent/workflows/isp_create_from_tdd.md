---
type: workflow
name: "Create ISP from TDD"
slug: /create_isp
description: "Generate Python stub from Technical Design."
mode: autonomous
inputs:
  - name: tdd_id
    type: string
    description: "Source TDD tag ID"
    required: true
context:
  - ".agent/rules/isp_stub_only.md"
  - ".agent/rules/isp_numpy_docstring.md"
  - ".agent/rules/isp_traceability_required.md"
  - ".agent/knowledge/sources/concepts/tier_isp.md"
outputs:
  - name: isp_id
    type: string
  - name: stub_file_path
    type: string
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Create ISP from TDD

// turbo
## Phase 1: Extract TDD
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/extract_citations.py" --tag-id "{{inputs.tdd_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

## Phase 2: Route
**@isp_codegenerator**: Generate stub.

// turbo
## Phase 3: Generate
**Class**:
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_class_stub.py" --tdd-id "{{inputs.tdd_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

**Method**:
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_method_stub.py" --tdd-id "{{inputs.tdd_id}}" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

// turbo
## Phase 4: Hints
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/add_implementation_hints.py" --tdd-id "{{inputs.tdd_id}}" --stub-file "{{stub_path}}"
```

// turbo
## Phase 5: Create Tag
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier ISP --title "Stub: {{class_name}}" --parent "{{inputs.tdd_id}}"
```
