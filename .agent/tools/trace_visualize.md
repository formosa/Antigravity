---
type: tool
name: "visualize_traceability"
description: "Generates Mermaid flowchart diagram of DDR traceability graph with tier-based subgraphs and color coding."
command: ".venv\\Scripts\\python .agent/scripts/visualize_traceability.py --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  root:
    description: "Root tag ID for focused view"
    required: false
  depth:
    description: "Traversal depth (default: 3)"
    required: false
  direction:
    description: "up, down, or both"
    required: false
---

# Tool: Visualize Traceability

## Overview

Generates Mermaid flowcharts with tier-based subgraphs and color coding.

## Knowledge Source

- **Tier Hierarchy**: `.agent/knowledge/sources/concepts/tier_hierarchy.md`

## Configuration

- **Entry Point**: `.agent/scripts/visualize_traceability.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--needs-json`: Optional. Path to needs.json.
    - `--root`: Optional. Root tag for focused view.
    - `--depth`: Optional. Traversal depth.
    - `--direction`: Optional. up/down/both.

## Protocol & Validation

### Success Verification
1. Output starts with `flowchart TD`
2. Contains tier subgraphs

### Example Output
```mermaid
flowchart TD
    subgraph BRD["BRD"]
        BRD_1["BRD-1: Purpose"]
    end
    NFR_1 -->|cites| BRD_1
```

## Rules
- **Read-Only**: Generates output only
- **Requires needs.json**: Run `rebuild_docs` first
