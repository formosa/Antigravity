---
type: tool
name: "validate_tier_compliance"
description: "Validates DDR tag content against tier-specific constraints including technology leaks, numeric requirements, and stub enforcement."
command: ".venv\\Scripts\\python .agent/scripts/validate_tier_compliance.py --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  id:
    description: "Single tag ID"
    required: false
  tier:
    description: "All tags in tier"
    required: false
  all:
    description: "Validate all"
    type: flag
    required: false
---

# Tool: Validate Tier Compliance

## Overview

Validates tag content against tier-specific constraints (technology leaks, numeric requirements, stub enforcement).

## Knowledge Sources

- **BRD Technology Agnostic**: `.agent/knowledge/sources/constraints/brd_technology_agnostic.md`
- **NFR Numeric Constraints**: `.agent/knowledge/sources/constraints/nfr_numeric_constraints.md`
- **ISP Stub Only**: `.agent/knowledge/sources/constraints/isp_stub_only.md`

## Configuration

- **Entry Point**: `.agent/scripts/validate_tier_compliance.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--needs-json`: Optional. Path to needs.json.
    - `--id`: Optional. Single tag.
    - `--tier`: Optional. All in tier.
    - `--all`: Optional flag. All tags.

## Tier Rules

| Tier | Rules |
|:-----|:------|
| BRD | tech_agnostic, measurable, stakeholder_focus |
| NFR | numeric_targets, constraint_language |
| FSD | no_impl, behavioral_language |
| SAD | pattern_reference |
| ICD | schema_definition |
| TDD | class_structure |
| ISP | stub_only, has_docstring |

## Protocol & Validation

### Success Verification
1. Output contains `checked`, `violations`, `details`

### Example Output
```json
{
  "checked": 10,
  "violations": 1,
  "details": [{"id": "BRD-5", "tier": "BRD", "rule": "tech_agnostic"}]
}
```

## Rules
- **Read-Only**: Analysis only
- **Requires needs.json**: Run `rebuild_docs` first
