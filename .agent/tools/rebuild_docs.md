---
type: tool
name: "rebuild_docs"
description: "Rebuilds Sphinx documentation (HTML, needs.json, and LLM context) and logs all warnings."
command: '$runId = Get-Date -Format "yyyyMMdd-HHmmss"; $uuid8 = ([guid]::NewGuid().ToString("N")).Substring(0, 8); $runDir = Join-Path "${workspaceFolder}" ".agent/.temp/$runId-$uuid8-rebuild-docs"; New-Item -ItemType Directory -Force -Path $runDir | Out-Null; & "${workspaceFolder}/.venv/Scripts/python.exe" -m sphinx -b needs docs docs/_build/json -w (Join-Path $runDir "refresh-context.log"); & "${workspaceFolder}/.venv/Scripts/python.exe" -m sphinx -b html docs docs/_build/html -a -w (Join-Path $runDir "refresh-context-html.log")'
runtime: system
confirmation: never
args: {}
---

# Tool: Rebuild Documentation

## Overview
Performs a complete documentation rebuild including:
1. **Needs Export** → `docs/_build/json/needs.json`
2. **HTML Generation** → `docs/_build/html/`
3. **Warning Capture** → `.agent/.temp/<run-dir>/refresh-context*.log`

## Configuration
- **Entry Point**: `.agent/scripts/generate_llm_context.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - "docs/_build/json/needs.json"
    - "docs/llm_export/context_flat.md"

## Execution Steps

### 1. Temp Run Directory Preparation
- **Command Pattern**: Create `.agent/.temp/YYYYMMDD-HHMMSS-<uuid8>-rebuild-docs/`
- **Note**: Keeps Sphinx warning logs inside the managed temp workspace.

### 2. Sphinx Needs Build (JSON Export)
- **Command**: `.venv/Scripts/python -m sphinx -b needs docs docs/_build/json -w <run-dir>/refresh-context.log`
- **Output**: `docs/_build/json/needs.json`
- **Effect**: Generates structured requirements data for LLM context generation.

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
2. **Instruction**: If either file contains any lines starting with `WARNING:`, a total count must be reported in the final conversation summary.

### Success Verification
1. **Needs Build**: Confirm `docs/_build/json/needs.json` exists and is non-empty.
2. **HTML Build**: Confirm `docs/_build/html/index.html` exists.
3. **LLM Context**: Check if `docs/llm_export/context_flat.md` header is intact.

## Rules
- **Artifacts**: Both log files are transient artifacts and must remain inside the generated `.agent/.temp/<run-dir>/` folder.
- **Reporting**: If more than 5 warnings are detected (combined), the agent should suggest a "Documentation Cleanup" follow-up task.
