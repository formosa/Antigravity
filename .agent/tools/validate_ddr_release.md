---
type: tool
name: "validate_ddr_release"
description: "Run the owned DDR v7.0 release gate against the authority pair, generated markdown, and conformance corpus."
command: '& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/validate_ddr_release.py"'
runtime: system
confirmation: never
args: {}
---

# Tool: Validate DDR Release

## Overview

Runs the owned DDR v7.0 release gate across:

1. YAML authority validation
2. Markdown provenance verification
3. Conformance corpus execution

## Inputs

- `ddr/ddr_system_v7.0.yaml`
- `ddr/ddr_node_schema_v7.0.yaml`
- `ddr/DDR System(v7.0).md`
- `ddr/ddr_ref_manual_v7.0.md`
- `ddr/conformance/v7.0/manifest.yaml`
- Every corpus case referenced by the manifest

## Outputs

- stdout validation summary only

## Corpus Layout

- Root: `ddr/conformance/v7.0/`
- Manifest: `ddr/conformance/v7.0/manifest.yaml`
- Expected layout: `valid/` and `invalid/` exemplar files referenced by the manifest

## Execution Contract

- Default command: `.venv/Scripts/python .agent/scripts/validate_ddr_release.py`
- Optional direct invocation may override `--system`, `--schema`, `--canonical-doc`, `--manual-doc`, and `--corpus-root`.
- The validator must fail if any valid corpus case is rejected, any invalid corpus case passes, or any provenance header mismatches the owned generator contract.

## Halt-On-Failure

- Treat any validator failure as a release-blocking result.
- Fix the failing authority, generated doc, or corpus case before re-running the release gate.
