---
type: tool
name: "create_tag"
description: "Generates a new DDR tag with Sequential ID, validates tier, and enforces parent citation."
command: ".venv\\Scripts\\python .agent/scripts/create_tag.py --tier \"${tier}\" --title \"${title}\" --parent \"${parent}\""
runtime: system
confirmation: ask
args:
  tier:
    description: "DDR tier code (BRD, NFR, FSD, SAD, ICD, TDD, ISP)"
    required: true
  title:
    description: "Human-readable tag title"
    required: true
  parent:
    description: "Parent tag ID for :links: directive (required for all tiers except BRD)"
    required: false
---

# Tool: Create Tag

## Overview

Generates a new DDR tag with a **Sequential Integer ID** (e.g., `FSD-12`), proper tier prefix, and validated parent citation. Outputs an RST directive ready for insertion into documentation.

## Knowledge Sources

- **Tag Syntax**: `.agent/knowledge/sources/patterns/tag-syntax.md`
- **ID Immutability**: `.agent/knowledge/sources/constraints/tag-immutability.md`
- **Citation Required**: `.agent/knowledge/sources/constraints/tag-citation-required.md`

## Configuration

- **Entry Point**: `.agent/scripts/create_tag.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--tier`: Required. DDR tier code.
    - `--title`: Required. Human-readable title.
    - `--parent`: Optional for BRD, required for other tiers.
    - `--description`: Optional. Tag content.
    - `--needs-json`: Optional. Path to needs.json for ID logic.
    - `--json-only`: Optional. Output JSON instead of RST.

## Execution Steps

### 1. Validate Tier
- Accept tier code (case-insensitive)
- Reject invalid tiers

### 2. Validate Parent Citation
- BRD: No parent required
- NFR: Parent must be BRD
- FSD: Parent must be BRD or NFR
- SAD: Parent must be FSD or NFR
- ICD: Parent must be SAD
- TDD: Parent must be ICD
- ISP: Parent must be TDD

### 3. Generate Sequential ID
- **Scan** `needs.json` for highest ID in tier (e.g., `max=10`).
- **Generate** next integer ID (e.g., `FSD-11`).
- **Fail Check**: If `needs.json` is missing/corrupt, exit with error.

### 4. Build RST Directive
```rst
.. fsd:: User Login Feature
   :id: FSD-11
   :links: BRD-1

   Description content here.
```

### 5. Output Result
- RST directive for documentation insertion
- Metadata for tracking

## Protocol & Validation

### Success Verification
1. Confirm output contains valid RST directive
2. Confirm ID format matches `{TIER}-{Number}` (Regex: `^[A-Z]{3}-\d+$`)
3. Confirm parent citation follows hierarchy rules

### Example Output
```rst
.. fsd:: User Login Feature
   :id: FSD-12
   :links: BRD-1

---
# Tag ID: FSD-12
# Tier: Feature Specification Document
# Reminder: Rebuild docs (make json) to update the index before generating the next tag.
# Parent: BRD-1
```

## Rules
- **ID Immutability**: Once generated, IDs must never change.
- **Parent Citation**: All non-BRD tiers require parent links.
- **Collision Detection**: Enforced via scan of `needs.json`. **Rebuild index between tag generations.**