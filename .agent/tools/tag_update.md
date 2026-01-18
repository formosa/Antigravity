---
type: tool
name: "update_tag"
description: "Updates an existing DDR tag and marks affected children for reconciliation."
command: ".venv\\Scripts\\python .agent/scripts/update_tag.py --id \"${id}\" --field \"${field}\" --value \"${value}\""
runtime: system
confirmation: ask
args:
  id:
    description: "Tag ID to update (e.g., FSD-001)"
    required: true
  field:
    description: "Field to update (title, description, status, content)"
    required: true
  value:
    description: "New value for the field"
    required: true
---

# Tool: Update Tag

## Overview

Prepares an update for an existing DDR tag, generating a semantic diff and
identifying downstream dependents that may require reconciliation.

## Knowledge Source

- **Dirty Flag**: `.agent/knowledge/sources/protocols/reconciliation_dirty_flag.md`
- **ID Immutability**: `.agent/knowledge/sources/constraints/tag_immutability.md`

## Configuration

- **Entry Point**: `.agent/scripts/update_tag.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--id`: Required. Tag ID to update.
    - `--field`: Required. Field to update.
    - `--value`: Required. New value.
    - `--needs-json`: Optional. Path to needs.json.

## Execution Steps

### 1. Validate Input
- Check tag exists in needs.json
- Validate field is updateable

### 2. Load Current State
- Read current field value
- Locate source file and line number

### 3. Find Downstream Dependents
- Search for tags that cite this tag
- These may need reconciliation review

### 4. Generate Update Diff
- Compare old and new values
- Flag if reconciliation is triggered

### 5. Output Instructions
- Source file location
- Specific edit instructions
- Reconciliation requirements

## Protocol & Validation

### Updateable Fields
| Field | Triggers Reconciliation |
|:------|:-----------------------:|
| title | ✅ Yes |
| description | ✅ Yes |
| content | ✅ Yes |
| status | ❌ No |

### Immutable Fields
- `id` - Never changes after creation
- `links` - Use separate link management tools

### Example Output
```json
{
  "success": true,
  "update": {
    "tag_id": "FSD-001",
    "tier": "FSD",
    "field": "title",
    "old_value": "User Login",
    "new_value": "User Authentication",
    "timestamp": "2026-01-17T20:30:00",
    "requires_reconciliation": true,
    "affected_children": [
      {"id": "SAD-001", "tier": "SAD", "title": "Auth Architecture"}
    ],
    "affected_count": 1
  },
  "source_file": "03_fsd/fsd.rst",
  "line_number": 45,
  "instructions": [
    "1. Open 03_fsd/fsd.rst",
    "2. Locate tag FSD-001 at line 45",
    "3. Update title from 'User Login' to 'User Authentication'"
  ],
  "reconciliation_required": true,
  "reconciliation_instructions": [
    "4. Review affected children for semantic consistency:",
    "   - SAD-001 (SAD): Auth Architecture"
  ]
}
```

## Rules
- **ID Immutability**: The `id` field cannot be changed.
- **Reconciliation**: Content changes trigger child review.
- **Read-then-Modify**: Tool reads but agent must apply edits.
