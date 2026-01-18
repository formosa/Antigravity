---
type: tool
name: "build_dependency_graph"
description: "Constructs DDR citation dependency graph from needs.json with orphan detection and cycle detection."
command: ".venv\\Scripts\\python .agent/scripts/build_dependency_graph.py --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  output:
    description: "Output file path (default: stdout)"
    required: false
  include_orphans:
    description: "Include orphan nodes"
    type: flag
    required: false
---

# Tool: Build Dependency Graph

## Overview

Constructs complete citation dependency graph from needs.json with orphan and cycle detection.

## Knowledge Source

- **Traceability Chain**: `.agent/knowledge/sources/protocols/traceability_chain.md`

## Configuration

- **Entry Point**: `.agent/scripts/build_dependency_graph.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--needs-json`: Optional. Path to needs.json.
    - `--output`: Optional. Output file path.
    - `--include-orphans`: Optional flag.

## Protocol & Validation

### Success Verification
1. Output contains `nodes`, `edges`, `stats`, `tiers_summary`
2. `stats` includes `has_cycles`, `orphan_count`

### Example Output
```json
{
  "stats": {"total_nodes": 10, "orphan_count": 1, "has_cycles": false},
  "tiers_summary": {"BRD": 2, "NFR": 3, "FSD": 5}
}
```

## Rules
- **Read-Only**: Analysis only
- **Requires needs.json**: Run `rebuild_docs` first
