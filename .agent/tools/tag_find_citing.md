---
type: tool
name: "find_tags_citing"
description: "Finds all DDR tags that cite a given tag as a parent."
command: ".venv\\Scripts\\python .agent/scripts/find_tags_citing.py --id \"${id}\""
runtime: system
confirmation: never
args:
  id:
    description: "Tag ID to find citations for (e.g., BRD-001)"
    required: true
---

# Tool: Find Tags Citing

## Overview

Performs downstream impact analysis by finding all DDR tags that cite a given
parent tag. Essential for understanding the propagation effects of modifications.

## Knowledge Source

- **Impact Analysis**: `.agent/knowledge/sources/protocols/impact_analysis.md`

## Configuration

- **Entry Point**: `.agent/scripts/find_tags_citing.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--id`: Required. Parent tag ID to search for.
    - `--needs-json`: Optional. Path to needs.json.
    - `--recursive`: Optional. Include transitive descendants.

## Execution Steps

### 1. Load Needs
- Parse needs.json to access all tags
- Handle missing file gracefully

### 2. Search for Citations
- Iterate through all tags
- Check each tag's `links` field
- Collect tags where target appears in links

### 3. Group by Tier
- Organize results by DDR tier
- Sort in hierarchy order (BRD → ISP)

### 4. Calculate Impact
- Count direct dependents
- Optionally compute transitive closure

### 5. Output Result
- JSON with citations grouped by tier
- Impact summary for modification planning

## Protocol & Validation

### Success Verification
1. Confirm output contains `target_id`, `cited_by`, `count` fields
2. `cited_by_tier` is grouped correctly
3. Impact summary matches count

### Example Output
```json
{
  "success": true,
  "target_id": "BRD-001",
  "target_tier": "BRD",
  "target_title": "Project Purpose",
  "target_exists": true,
  "cited_by": [
    {
      "id": "NFR-001",
      "tier": "NFR",
      "title": "Performance Requirements",
      "link_type": "direct"
    },
    {
      "id": "FSD-001",
      "tier": "FSD",
      "title": "User Login Feature",
      "link_type": "direct"
    }
  ],
  "cited_by_tier": {
    "NFR": [{"id": "NFR-001", "title": "Performance Requirements"}],
    "FSD": [{"id": "FSD-001", "title": "User Login Feature"}]
  },
  "count": 2,
  "impact_summary": "Modifying BRD-001 may affect 2 direct dependents"
}
```

## Use Cases

| Use Case | Command |
|:---------|:--------|
| Pre-update impact check | `find_tags_citing --id BRD-001` |
| Full dependency tree | `find_tags_citing --id BRD-001 --recursive` |
| Deprecation planning | Check all dependents before deprecating |

## Rules
- **Read-Only**: This tool does not modify any files.
- **Hierarchy Aware**: Results ordered by tier precedence.
- **Recursive Option**: Use `--recursive` for full transitive closure.
