---
type: tool
name: "extract_citations"
description: "Extracts cited parent tags from a DDR tag's :links: directive."
command: ".venv\\Scripts\\python .agent/scripts/extract_citations.py --id \"${id}\""
runtime: system
confirmation: never
args:
  id:
    description: "Tag ID to extract citations from (e.g., FSD-001)"
    required: true
---

# Tool: Extract Citations

## Overview

Parses the `:links:` directive from a DDR tag to extract all parent citations.
Validates that cited parents exist and identifies orphan status.

## Knowledge Source

- **Citation Required**: `.agent/knowledge/sources/constraints/tag_citation_required.md`

## Configuration

- **Entry Point**: `.agent/scripts/extract_citations.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--id`: Required. Tag ID to analyze.
    - `--needs-json`: Optional. Path to needs.json (default: `docs/_build/json/needs.json`).

## Execution Steps

### 1. Load Needs
- Parse needs.json to access tag data
- Handle missing file gracefully

### 2. Locate Tag
- Find tag by ID in needs dictionary
- Return error if not found

### 3. Extract Links
- Read `links` field from tag
- Normalize to list (may be string or array)

### 4. Validate Parents
For each cited parent:
- Extract tier from ID
- Check if parent exists in needs
- Record existence status

### 5. Determine Orphan Status
- BRD tags: Never orphans (root tier)
- Other tiers: Orphan if no valid parent exists

### 6. Output Result
- JSON with parent list, orphan status, validation

## Protocol & Validation

### Success Verification
1. Confirm output contains `id`, `parents`, `orphan` fields
2. Each parent has `id`, `tier`, `exists` fields
3. Orphan status correctly reflects parent validity

### Example Outputs

**Tag with Valid Parents:**
```json
{
  "success": true,
  "id": "FSD-001",
  "tier": "FSD",
  "title": "User Login Feature",
  "parents": [
    {
      "id": "BRD-001",
      "tier": "BRD",
      "exists": true,
      "title": "User Authentication Requirement"
    }
  ],
  "parent_count": 1,
  "missing_parents": [],
  "orphan": false,
  "orphan_reason": null
}
```

**Orphan Tag:**
```json
{
  "success": true,
  "id": "FSD-999",
  "tier": "FSD",
  "title": "Orphan Feature",
  "parents": [],
  "parent_count": 0,
  "missing_parents": [],
  "orphan": true,
  "orphan_reason": "No valid parent citations"
}
```

## Rules
- **Read-Only**: This tool does not modify any files.
- **BRD Exception**: BRD tags are never considered orphans.
- **Missing Parent**: Parents that don't exist are flagged in `missing_parents`.
