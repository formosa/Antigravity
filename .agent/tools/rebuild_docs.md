---
type: tool
name: "rebuild_docs"
description: "Rebuilds Sphinx documentation outputs with managed-temp warning capture and failure retention."
command: '& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/rebuild_docs.py"'
runtime: system
confirmation: never
args: {}
---

# Tool: Rebuild Documentation

## Overview

Performs a complete documentation rebuild including:

1. **Needs Export** → `docs/_build/json/needs.json`
2. **HTML Generation** → `docs/_build/html/`
3. **Failure Logs** → `.agent/.temp/<run-dir>/refresh-context*.log` only when the rebuild or post-build validation fails

## Configuration

- **Entry Point**: `.agent/scripts/rebuild_docs.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**: none

## Execution Steps

### 1. Temp Run Directory Preparation

- **Command Pattern**: Create `.agent/.temp/YYYYMMDD-HHMMSS-rebuild-docs/`
- **Collision Handling**: If that directory already exists, append `-01`, `-02`, and so on until a free path is found.
- **Note**: Temporary logs live only inside the managed temp workspace and are deleted on success.

### 2. Sphinx Needs Build (JSON Export)

- **Command**: `.venv/Scripts/python -m sphinx -b needs docs docs/_build/json -w <run-dir>/refresh-context.log`
- **Output**: `docs/_build/json/needs.json`
- **Effect**: Generates the Sphinx needs export used by local documentation tooling.

### 3. Sphinx HTML Build

- **Command**: `.venv/Scripts/python -m sphinx -b html docs docs/_build/html -a -w <run-dir>/refresh-context-html.log`
- **Output**: `docs/_build/html/`
- **Flags**:
  - `-a`: Rebuild all files (not just changed ones)
- **Effect**: Generates human-readable HTML documentation.

## Protocol & Validation

### Warning Audit

1. **Action**: The agent must read both log files:
   - `.agent/.temp/<run-dir>/refresh-context.log` (needs build)
   - `.agent/.temp/<run-dir>/refresh-context-html.log` (HTML build)
2. **Instruction**: If either file contains any lines starting with `WARNING:`, a total count must be reported before the successful run directory is deleted.

### Success Verification

1. **Needs Build**: Confirm `docs/_build/json/needs.json` exists and is non-empty.
2. **HTML Build**: Confirm `docs/_build/html/index.html` exists.
3. **Temp Hygiene**: Confirm the managed temp run directory is deleted after a successful rebuild.

## Rules

- **Artifacts**: Both log files are transient artifacts and must remain inside the generated `.agent/.temp/<run-dir>/` folder.
- **Retention**: Keep the run directory only on failure, and write `retained-on-failure.txt` with the failure reason.
- **Reporting**: If more than 5 warnings are detected (combined), the agent should suggest a "Documentation Cleanup" follow-up task.
