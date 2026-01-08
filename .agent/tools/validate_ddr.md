---
type: tool
name: validate_ddr
description: "Validates DDR traceability rules. Prereq: docs must be built via sphinx-build -b needs."
command: "& '${workspaceFolder}/.venv/Scripts/python.exe' '${workspaceFolder}/.agent/scripts/validate_ddr.py' --docs-dir '${workspaceFolder}/docs' --sandbox-id '{{args.sandbox_id}}'"
runtime: system
confirmation: never
args:
  sandbox_id:
    type: string
    required: true
    description: "UUID for output directory. Generate via /generate_uuid."
---

# Tool: DDR Validation

Validates the Sphinx-Needs documentation against DDR meta-standard rules. Requires the documentation to be built first to generate the `needs.json` file.
