---
type: tool
name: "generate_traceability_report"
description: "Analyzes DDR citation chains and generates violation reports with configurable format and severity filtering."
command: ".venv\\Scripts\\python .agent/scripts/generate_traceability_report.py --format \"${format}\""
runtime: system
confirmation: never
args:
  format:
    description: "Output format: json, markdown, summary"
    required: true
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  severity:
    description: "Filter: ERROR, WARNING, ALL"
    required: false
---

# Tool: Generate Traceability Report

## Overview

Analyzes citation chains and generates violation reports with format/severity options.

## Knowledge Source

- **Traceability Chain**: `.agent/knowledge/sources/protocols/traceability_chain.md`

## Configuration

- **Entry Point**: `.agent/scripts/generate_traceability_report.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--format`: Required. json/markdown/summary.
    - `--needs-json`: Optional. Path to needs.json.
    - `--severity`: Optional. ERROR/WARNING/ALL.

## Violation Types

| Type | Severity |
|:-----|:---------|
| ORPHAN | ERROR |
| MISSING_PARENT | ERROR |
| SIBLING_CITATION | WARNING |
| FORWARD_REFERENCE | ERROR |

## Protocol & Validation

### Success Verification
1. Output matches requested format

### Example Output (summary)
```
Analyzed: 45
Violations: 2
  ORPHAN: 2
```

## Rules
- **Read-Only**: Analysis only
- **Requires needs.json**: Run `rebuild_docs` first
