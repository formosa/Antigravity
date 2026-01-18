---
type: tool
name: "add_implementation_hints"
description: "Enriches ISP stub files with implementation guidance extracted from TDD/ICD tag references."
command: ".venv\\Scripts\\python .agent/scripts/add_implementation_hints.py --isp-file \"${isp_file}\" --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  isp_file:
    description: "Python file to annotate"
    required: true
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  dry_run:
    description: "Print without writing"
    type: flag
    required: false
---

# Tool: Add Implementation Hints

## Overview

Parses ISP Python files for `|TAG-ID|` references and injects implementation
hint comments. Creates a `.hints.py` file without modifying the original.

## Knowledge Source

- **Numpy Docstrings**: `.agent/knowledge/sources/constraints/isp_numpy_docstrings.md`

## Configuration

- **Entry Point**: `.agent/scripts/add_implementation_hints.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--isp-file`: Required. Path to ISP Python file.
    - `--needs-json`: Optional. Path to needs.json.
    - `--dry-run`: Optional flag. Print instead of write.

## Execution Steps

### 1. Scan ISP File
- Find `|TAG-ID|` references

### 2. Extract Hints
- Format as `# IMPL: From TAG-ID: {content}`

### 3. Output
- Write to `{original}.hints.py`

## Protocol & Validation

### Success Verification
1. New `.hints.py` file created
2. Original file unchanged

## Rules
- **Non-Destructive**: Creates new file only
- **Requires needs.json**: Tags must exist
