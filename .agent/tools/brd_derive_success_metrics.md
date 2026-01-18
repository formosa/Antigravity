---
type: tool
name: "derive_success_metrics"
description: "Generates quantifiable success metrics from business objectives based on DDR measurable metrics constraint."
command: ".venv\\Scripts\\python .agent/scripts/derive_success_metrics.py --objective \"${objective}\""
runtime: system
confirmation: never
args:
  objective:
    description: "Business objective text to analyze"
    required: true
---

# Tool: Derive Success Metrics

## Overview

Analyzes vague business objectives and suggests specific, quantifiable KPIs.
Used by BRD specialists to transform unmeasurable requirements into DDR-compliant metrics.

## Knowledge Source

- **Measurable Metrics Constraint**: `.agent/knowledge/sources/constraints/brd_measurable_metrics.md`

## Configuration

- **Entry Point**: `.agent/scripts/derive_success_metrics.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--objective`: Required. Business objective text.

## Execution Steps

### 1. Parse Objective
- Accept business objective text

### 2. Detect Categories
- Match keywords: performance, reliability, usability, scalability, security, maintainability

### 3. Generate Suggested Metrics
- Template metrics with placeholder "X" values

## Protocol & Validation

### Success Verification
1. Output contains `objective`, `detected_categories`, `suggested_metrics`

### Example Output
```json
{
  "objective": "System must be fast and reliable",
  "detected_categories": ["performance", "reliability"],
  "suggested_metrics": ["Response time < X seconds", "Availability > 99.X%"]
}
```

## Rules
- **Suggestive**: Metrics are templates; user must replace X
- **Read-Only**: No file modifications
