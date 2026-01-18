---
type: workflow
name: "Comprehensive Traceability Audit"
slug: /audit_traceability
description: "Full DDR tag validation for completeness, integrity, and chain validity."
mode: autonomous
context:
  - ".agent/knowledge/sources/protocols/traceability_chain.md"
  - ".agent/knowledge/sources/protocols/reconciliation_dirty_flag.md"
  - ".agent/knowledge/sources/constraints/sibling_prohibition.md"
outputs:
  - name: orphan_count
    type: integer
  - name: violations
    type: integer
  - name: report_path
    type: string
on_finish: "suggest_followup: /resolve_orphan"
---

# Workflow: Comprehensive Traceability Audit

// turbo
## Phase 1: Build needs.json
```powershell
& "${workspaceFolder}/.venv/Scripts/sphinx-build.exe" -b needs "${workspaceFolder}/docs" "${workspaceFolder}/docs/_build"
```

// turbo
## Phase 2: Dependency Graph
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/build_dependency_graph.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

// turbo
## Phase 3: Manifest Integrity
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/check_manifest_integrity.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

// turbo
## Phase 4: Anti-Patterns
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/detect_anti_patterns.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json"
```

// turbo
## Phase 5: Report
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_traceability_report.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --format markdown
```
