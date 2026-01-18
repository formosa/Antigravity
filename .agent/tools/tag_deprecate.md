---
type: tool
name: "deprecate_tag"
description: "Marks a DDR tag as deprecated and optionally specifies a replacement."
command: ".venv\\Scripts\\python .agent/scripts/deprecate_tag.py --id \"${id}\" --replacement \"${replacement}\""
runtime: system
confirmation: ask
args:
  id:
    description: "Tag ID to deprecate"
    required: true
  replacement:
    description: "Replacement tag ID (optional)"
    required: false
---

# Tool: Deprecate Tag

## Overview

Marks a DDR tag as deprecated while preserving its ID (immutability constraint).
Identifies dependent tags that need migration and provides update instructions.

## Knowledge Source

- **ID Immutability**: `.agent/knowledge/sources/constraints/tag_immutability.md`

## Configuration

- **Entry Point**: `.agent/scripts/deprecate_tag.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--id`: Required. Tag ID to deprecate.
    - `--replacement`: Optional. Replacement tag ID.
    - `--needs-json`: Optional. Path to needs.json.

## Execution Steps

### 1. Validate Tag
- Check tag exists in needs.json
- Verify not already deprecated

### 2. Validate Replacement
If replacement provided:
- Check replacement exists (warning if not)
- Check replacement is same tier (warning if not)

### 3. Find Dependents
- Search for tags citing this tag
- These need migration to replacement

### 4. Generate Deprecation Notice
- Create dated deprecation message
- Include replacement reference if available

### 5. Output Instructions
- RST modification example
- Migration instructions for dependents

## Protocol & Validation

### Deprecation Workflow
1. Add `:status: deprecated` to directive
2. Add deprecation warning to content
3. Preserve original content below warning
4. Update dependent tags to cite replacement

### Example Output
```json
{
  "success": true,
  "deprecation": {
    "tag_id": "FSD-001",
    "tier": "FSD",
    "title": "User Login",
    "deprecated_at": "2026-01-17T20:30:00",
    "replacement": "FSD-002",
    "replacement_valid": true,
    "replacement_info": {
      "id": "FSD-002",
      "exists": true,
      "tier": "FSD",
      "title": "User Authentication"
    }
  },
  "affected_children": [
    {"id": "SAD-001", "tier": "SAD", "title": "Auth Architecture"}
  ],
  "affected_count": 1,
  "rst_modification": "..."
}
```

### RST Modification Example
```rst
.. fsd:: User Login
   :id: FSD-001
   :status: deprecated

   .. warning::
      DEPRECATED: This tag is deprecated as of 2026-01-17. Use FSD-002 instead.

   [Original content preserved below...]
```

## Rules
- **ID Preservation**: Never delete or reassign deprecated IDs.
- **Content Preservation**: Original content must remain visible.
- **Migration Required**: All dependent tags should migrate to replacement.
- **Same-Tier Replacement**: Replacement should be from same tier.
