---
type: workflow
name: DDR Validation
slug: /validate_ddr
description: "Comprehensive DDR meta-standard validation workflow. Builds needs.json and runs DDR validation."
mode: autonomous
context: [".agent/rules/ddr_traceability.md"]
on_finish: "suggest_followup: /rebuild_docs"
---

# DDR Validation Workflow

## 1. Setup Sandbox
1. Run tool: `/generate_uuid`
2. Set `SANDBOX_ID` from output.

// turbo
## 2. Generate Traceability Data
```powershell
& "${workspaceFolder}/.venv/Scripts/sphinx-build.exe" -b needs "${workspaceFolder}/docs" "${workspaceFolder}/docs/_build"
```

// turbo
## 3. Execute Validation
```powershell
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/validate_ddr.py" --docs-dir "${workspaceFolder}/docs" --sandbox-id "$SANDBOX_ID"
```

## 4. Review Results
Read `.agent/.sandbox/validate_ddr-$SANDBOX_ID/ddr_audit.md`
