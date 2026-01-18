---
type: tool
name: "create_tag"
description: "Generates a new DDR tag with UUID, validates tier, and enforces parent citation."
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

Generates a new DDR tag with a unique ID, proper tier prefix, and validated
parent citation. Outputs an RST directive ready for insertion into documentation.

## Knowledge Sources

- **Tag Syntax**: `.agent/knowledge/sources/patterns/tag_syntax.md`
- **ID Immutability**: `.agent/knowledge/sources/constraints/tag_immutability.md`
- **Citation Required**: `.agent/knowledge/sources/constraints/tag_citation_required.md`

## Configuration

- **Entry Point**: `.agent/scripts/create_tag.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--tier`: Required. DDR tier code.
    - `--title`: Required. Human-readable title.
    - `--parent`: Optional for BRD, required for other tiers.
    - `--description`: Optional. Tag content.
    - `--needs-json`: Optional. Path to needs.json for ID collision check.
    - `--json-only`: Optional. Output JSON instead of RST.

## Execution Steps

### 1. Validate Tier
- Accept tier code (case-insensitive)
- Reject invalid tiers

### 2. Validate Parent Citation
- BRD: No parent required
- NFR: Parent must be BRD
- FSD: Parent must be BRD or NFR
- SAD: Parent must be FSD
- ICD: Parent must be SAD
- TDD: Parent must be ICD
- ISP: Parent must be TDD

### 3. Generate Unique ID
- Create 8-character UUID hex
- Format: `{TIER}-{uuid8}` (e.g., `FSD-a1b2c3d4`)
- Check for collision with existing needs

### 4. Build RST Directive
```rst
.. fsd:: User Login Feature
   :id: FSD-a1b2c3d4
   :links: BRD-001

   Description content here.
```

### 5. Output Result
- RST directive for documentation insertion
- Metadata for tracking

## Protocol & Validation

### Success Verification
1. Confirm output contains valid RST directive
2. Confirm ID format matches `{TIER}-{8chars}`
3. Confirm parent citation follows hierarchy rules

### Example Output
```rst
.. fsd:: User Login Feature
   :id: FSD-a1b2c3d4
   :links: BRD-001

---
# Tag ID: FSD-a1b2c3d4
# Tier: Feature Specification Document
# Parent: BRD-001
```

## Tier Hierarchy

```
BRD (root)
 └── NFR
 └── FSD
      └── SAD
           └── ICD
                └── TDD
                     └── ISP
```

## Rules
- **ID Immutability**: Once generated, IDs must never change.
- **Parent Citation**: All non-BRD tiers require parent links.
- **Collision Detection**: IDs are checked against needs.json.
