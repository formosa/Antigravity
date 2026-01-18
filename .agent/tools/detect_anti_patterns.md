---
type: tool
name: "detect_anti_patterns"
description: "Scans DDR tags for structural and content anti-patterns including orphans, sibling citations, forward references, and technology leaks."
command: ".venv\\Scripts\\python .agent/scripts/detect_anti_patterns.py --needs-json \"${needs_json}\" --patterns \"${patterns}\""
runtime: system
confirmation: never
args:
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  patterns:
    description: "Comma-separated pattern IDs (e.g., AP001,AP002). Default: all"
    required: false
---

# Tool: Detect Anti-Patterns

## Overview

Identifies structural and content violations across DDR tags.
Used by antipattern_scanner for documentation quality validation.

## Knowledge Sources

- **Sibling Prohibition**: `.agent/knowledge/sources/constraints/sibling_prohibition.md`
- **Traceability Chain**: `.agent/knowledge/sources/protocols/traceability_chain.md`

## Configuration

- **Entry Point**: `.agent/scripts/detect_anti_patterns.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--needs-json`: Optional. Path to needs.json.
    - `--patterns`: Optional. Pattern IDs to filter.

## Anti-Pattern Definitions

| ID | Name |
|:---|:-----|
| AP001 | Vertical Pollution (code in upper tiers) |
| AP002 | Orphan Tag (no parent) |
| AP003 | Sibling Citation (same-tier link) |
| AP004 | Forward Reference (lower-tier citation) |
| AP005 | Missing Title |
| AP006 | Dangling ISP (no TDD parent) |
| AP007 | ID Format Violation |
| AP008 | Technology Leak in BRD |
| AP009 | Empty Content |

## Protocol & Validation

### Success Verification
1. Output contains `scanned`, `violations`, `by_pattern`, `details`

### Example Output
```json
{
  "scanned": 45,
  "violations": 2,
  "by_pattern": {"AP002": 2},
  "details": [{"id": "FSD-999", "pattern": "AP002", "name": "Orphan Tag"}]
}
```

## Rules
- **Read-Only**: Analysis only
- **Requires needs.json**: Run `rebuild_docs` first
