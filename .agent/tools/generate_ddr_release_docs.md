---
type: tool
name: "generate_ddr_release_docs"
description: "Generate the governed DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair."
command: '& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/generate_ddr_release_docs.py"'
runtime: system
confirmation: never
args: {}
---

# Tool: Generate DDR Release Docs

## Overview

Generates the two owned v7.0 markdown release surfaces from the authoritative YAML pair:

1. `ddr/DDR System(v7.0).md`
2. `ddr/ddr_ref_manual_v7.0.md`

## Inputs

- `ddr/ddr_system_v7.0.yaml`
- `ddr/ddr_node_schema_v7.0.yaml`

## Outputs

- `ddr/DDR System(v7.0).md`
- `ddr/ddr_ref_manual_v7.0.md`

## Provenance Rules

- Both outputs must begin with the generator-owned provenance header.
- The provenance header must name `.agent/scripts/generate_ddr_release_docs.py` as the generator.
- The provenance header must point back to `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml`.
- Generated markdown is explanatory only; it must not claim stronger authority than the YAML pair.

## Execution Contract

- Default command: `.venv/Scripts/python .agent/scripts/generate_ddr_release_docs.py`
- Optional direct invocation may override `--system`, `--schema`, `--canonical-out`, and `--manual-out`.
- Halt immediately if either YAML input is missing, malformed, or has a non-mapping root.

## Halt-On-Failure

- Do not keep partially trusted markdown outputs if the command reports an input failure.
- Run the owned validator after generation when the release package is being prepared or checked.
