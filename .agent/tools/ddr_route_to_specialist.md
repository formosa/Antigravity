---
type: tool
name: "route_to_specialist"
description: "Returns the specialist persona handle for a given DDR tier."
command: ".venv\\Scripts\\python .agent/scripts/route_to_specialist.py --tier \"${tier}\""
runtime: system
confirmation: never
args:
  tier:
    description: "DDR tier code (BRD, NFR, FSD, SAD, ICD, TDD, ISP)"
    required: true
---

# Tool: Route to Specialist

## Overview

Maps a DDR tier to its corresponding specialist agent persona. This tool is used
by the orchestrator (`@ddr_orchestrator`) to delegate tier-specific documentation
tasks to the appropriate specialist agent.

## Configuration

- **Entry Point**: `.agent/scripts/route_to_specialist.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--tier`: Required. The DDR tier code (case-insensitive).
    - `--list`: Optional. List all tier-to-specialist mappings.

## Execution Steps

### 1. Validate Tier Input
- Accept tier code (BRD, NFR, FSD, SAD, ICD, TDD, ISP)
- Normalize to uppercase
- Return error if tier is invalid

### 2. Lookup Specialist
- Query internal mapping table
- Return specialist handle, persona path, and description

### 3. Output Result
- JSON object with routing information

## Protocol & Validation

### Success Verification
1. Confirm output contains `tier`, `handle`, `persona_path` fields
2. Confirm `handle` starts with `@`
3. Confirm `persona_path` points to existing `.mdc` file

### Example Output
```json
{
  "tier": "FSD",
  "handle": "@fsd_analyst",
  "persona_path": ".agent/personas/fsd_analyst.mdc",
  "description": "Feature Specification Analyst"
}
```

## Tier-Specialist Mapping

| Tier | Handle | Persona |
|:-----|:-------|:--------|
| BRD | `@brd_strategist` | Business Requirements Specialist |
| NFR | `@nfr_enforcer` | Non-Functional Requirements Enforcer |
| FSD | `@fsd_analyst` | Feature Specification Analyst |
| SAD | `@sad_architect` | System Architecture Designer |
| ICD | `@icd_dataengineer` | Interface Contract Data Engineer |
| TDD | `@tdd_designer` | Technical Design Document Designer |
| ISP | `@isp_codegenerator` | Implementation Stub Producer |

## Rules
- **No External Dependencies**: Uses only Python standard library.
- **Deterministic Output**: Same tier always returns same specialist.
- **Case Insensitive**: Tier input is normalized to uppercase.
