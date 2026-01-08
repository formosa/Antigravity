---
type: tool
name: "rebuild_docs"
description: "Rebuilds Sphinx documentation (HTML and Markdown) and logs all warnings."
command: "mkdir -p .agent/tools/temp/ ; .venv\\Scripts\\python -m sphinx -b needs docs docs/_build/json -w .agent/tools/temp/refresh-context.log"
runtime: system
confirmation: never
args: {}
---

# Tool: Refresh Context (with Warning Log)

## Configuration
- **Entry Point**: `.agent/scripts/generate_llm_context.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - "docs/_build/json/needs.json"
    - "docs/llm_export/context_flat.md"

## Pre-Execution Steps
1. **Directory Preparation**:
   - **Command**: `mkdir -p .agent/tools/temp/`
   - **Note**: Ensures the target log location exists to prevent Sphinx build errors.

2. **Sphinx Build with Log Capture**:
   - **Command**: `.venv/Scripts/python -m sphinx -b needs docs docs/_build/json -w .agent/tools/temp/refresh-context.log`
   - **Effect**: Standard error output containing warnings is redirected into the specified `.log` file.

## Protocol & Validation
1. **Warning Audit**:
   - **Action**: The agent must read `.agent/tools/temp/refresh-context.log`.
   - **Instruction**: If the file contains any lines starting with `WARNING:`, a total count of these warnings must be reported in the final conversation summary.
2. **Success Verification**:
   - **Action**: Check if `docs/llm_export/context_flat.md` header is intact.

## Rules
- **Artifact**: The log file `.agent/tools/temp/refresh-context.log` must be treated as a persistent artifact for this session.
- **Reporting**: If more than 5 warnings are detected, the agent should suggest a "Documentation Cleanup" follow-up task.
