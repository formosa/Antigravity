---
type: tool
name: "rebuild_docs"
description: "Rebuilds Sphinx documentation (HTML, needs.json, and LLM context) and logs all warnings."
command: "mkdir -p .agent/tools/temp/ ; .venv\\Scripts\\python -m sphinx -b needs docs docs/_build/json -w .agent/tools/temp/refresh-context.log ; .venv\\Scripts\\python -m sphinx -b html docs docs/_build/html -a -w .agent/tools/temp/refresh-context-html.log"
runtime: system
confirmation: never
args: {}
---

# Tool: Rebuild Documentation

## Overview
Performs a complete documentation rebuild including:
1. **Needs Export** → `docs/_build/json/needs.json`
2. **HTML Generation** → `docs/_build/html/`
3. **Warning Capture** → `.agent/tools/temp/*.log`

## Configuration
- **Entry Point**: `.agent/scripts/generate_llm_context.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - "docs/_build/json/needs.json"
    - "docs/llm_export/context_flat.md"

## Execution Steps

### 1. Directory Preparation
- **Command**: `mkdir -p .agent/tools/temp/`
- **Note**: Ensures the target log location exists to prevent Sphinx build errors.

### 2. Sphinx Needs Build (JSON Export)
- **Command**: `.venv/Scripts/python -m sphinx -b needs docs docs/_build/json -w .agent/tools/temp/refresh-context.log`
- **Output**: `docs/_build/json/needs.json`
- **Effect**: Generates structured requirements data for LLM context generation.

### 3. Sphinx HTML Build
- **Command**: `.venv/Scripts/python -m sphinx -b html docs docs/_build/html -a -w .agent/tools/temp/refresh-context-html.log`
- **Output**: `docs/_build/html/`
- **Flags**:
    - `-a`: Rebuild all files (not just changed ones)
- **Effect**: Generates human-readable HTML documentation.

## Protocol & Validation

### Warning Audit
1. **Action**: The agent must read both log files:
   - `.agent/tools/temp/refresh-context.log` (needs build)
   - `.agent/tools/temp/refresh-context-html.log` (HTML build)
2. **Instruction**: If either file contains any lines starting with `WARNING:`, a total count must be reported in the final conversation summary.

### Success Verification
1. **Needs Build**: Confirm `docs/_build/json/needs.json` exists and is non-empty.
2. **HTML Build**: Confirm `docs/_build/html/index.html` exists.
3. **LLM Context**: Check if `docs/llm_export/context_flat.md` header is intact.

## Rules
- **Artifacts**: Both log files must be treated as persistent artifacts for this session.
- **Reporting**: If more than 5 warnings are detected (combined), the agent should suggest a "Documentation Cleanup" follow-up task.
