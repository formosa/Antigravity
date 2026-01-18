---
type: tool
name: "abstract_to_business_value"
description: "Converts technology-specific terminology to business-appropriate language for BRD tier compliance."
command: ".venv\\Scripts\\python .agent/scripts/abstract_to_business.py --text \"${text}\""
runtime: system
confirmation: never
args:
  text:
    description: "Text containing technology terms to transform"
    required: true
---

# Tool: Abstract to Business Value

## Overview

Transforms technology-specific terminology into business-agnostic language suitable
for BRD tier content. Used by BRD specialists to ensure compliance with the
technology-agnostic constraint before tag creation.

## Knowledge Source

- **Technology Agnostic Constraint**: `.agent/knowledge/sources/constraints/brd_technology_agnostic.md`

## Configuration

- **Entry Point**: `.agent/scripts/abstract_to_business.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--text`: Required. Text with potential technology terms.

## Execution Steps

### 1. Parse Input
- Accept text string containing potential technology terminology

### 2. Apply Transformations
- Languages/frameworks → `[REMOVE]` (Python, JavaScript, React, etc.)
- Hardware → generic terms (GPU → "hardware acceleration")
- Protocols → generic terms (REST → "service interface")
- Databases → generic terms (PostgreSQL → "relational storage")

### 3. Return Result
- JSON with `original`, `transformed`, `changes`, `warnings` keys

## Protocol & Validation

### Success Verification
1. Output contains `original`, `transformed`, `changes`, `warnings` keys

### Example Output
```json
{
  "original": "Use Python REST API with Redis cache",
  "transformed": "Use service interface with caching layer",
  "changes": ["Removed 'python'", "'rest' -> 'service interface'", "'redis' -> 'caching layer'"],
  "warnings": []
}
```

## Rules
- **Read-Only**: No file modifications
- **Deterministic**: Same input produces same output
