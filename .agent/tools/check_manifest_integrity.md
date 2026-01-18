---
type: tool
name: "check_manifest_integrity"
description: "Validates reconciliation manifest blocks against DDR structure requirements including field presence and tag inventory consistency."
command: ".venv\\Scripts\\python .agent/scripts/check_manifest_integrity.py --manifest-dir \"${manifest_dir}\" --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  manifest_dir:
    description: "Directory to scan (default: docs/)"
    required: false
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
---

# Tool: Check Manifest Integrity

## Overview

Validates `reconciliation_manifest.rst` files against DDR requirements.
Detects missing fields, invalid status values, and count/inventory mismatches.

## Knowledge Sources

- **Manifest Structure**: `.agent/knowledge/sources/patterns/manifest_structure.md`
- **Dirty Flag Protocol**: `.agent/knowledge/sources/protocols/reconciliation_dirty_flag.md`

## Configuration

- **Entry Point**: `.agent/scripts/check_manifest_integrity.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--manifest-dir`: Optional. Directory to scan.
    - `--needs-json`: Optional. Path to needs.json.

## Execution Steps

### 1. Load Needs
- Parse needs.json for tag validation

### 2. Find Manifests
- Search for `reconciliation_manifest.rst` files

### 3. Validate Each Manifest
- Required fields: `:section_id:`, `:integrity_status:`, `:timestamp:`, `:tag_count:`, `:tag_inventory:`, `:pending_items:`
- Status must be CLEAN or DIRTY
- Count must match inventory length

## Protocol & Validation

### Success Verification
1. Output contains `manifests_checked`, `issues`, `by_type`, `details`

### Example Output
```json
{
  "manifests_checked": 3,
  "issues": 1,
  "by_type": {"COUNT_MISMATCH": 1},
  "details": [{"manifest": "docs/02_nfr/reconciliation_manifest.rst", "type": "COUNT_MISMATCH", "severity": "ERROR"}]
}
```

## Rules
- **Read-Only**: Analysis only
- **Requires needs.json**: Run `rebuild_docs` first
