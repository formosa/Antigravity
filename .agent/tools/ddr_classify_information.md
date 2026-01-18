---
type: tool
name: "classify_information"
description: "Classifies information fragments into DDR tiers using the decision tree algorithm."
command: ".venv\\Scripts\\python .agent/scripts/classify_information.py --input \"${input}\""
runtime: system
confirmation: never
args:
  input:
    description: "Information fragment to classify"
    required: true
---

# Tool: Classify Information

## Overview

Applies the DDR classification decision tree to determine which tier owns an
unclassified information fragment. This is the primary classification tool used
by the orchestrator to route new documentation content.

## Knowledge Sources

- **Decision Tree**: `.agent/knowledge/sources/protocols/classification_decision_tree.md`
- **Scoring Matrix**: `.agent/knowledge/sources/protocols/classification_scoring.md`

## Configuration

- **Entry Point**: `.agent/scripts/classify_information.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--input`: Required. The information fragment text to classify.
    - `--verbose`: Optional. Include detailed scoring breakdown.

## Execution Steps

### 1. Parse Input
- Accept unstructured text fragment
- Validate non-empty input

### 2. Apply Decision Tree (Q1 → Q6)
```
Q1: WHY? (Business value, ROI, market) → BRD
Q2: LIMITS? (Performance, SLAs, constraints) → NFR
Q3: WHAT? (Features, capabilities) → FSD
Q4: HOW? (Patterns, topology) → SAD
Q5: SCHEMA? (Data formats, contracts) → ICD
Q6: CLASS? (Methods, dependencies) → TDD
Default: → ISP
```

### 3. Calculate Confidence
- Score based on keyword matches and pattern detection
- Identify ambiguity when multiple tiers have similar scores

### 4. Output Result
- JSON object with tier, confidence, rationale

## Protocol & Validation

### Success Verification
1. Confirm output contains `tier`, `confidence`, `rationale` fields
2. Confirm `tier` is valid (BRD, NFR, FSD, SAD, ICD, TDD, ISP)
3. If `ambiguous: true`, confirm `candidates` array is present

### Example Outputs

**Clear Classification:**
```json
{
  "tier": "NFR",
  "confidence": 0.8,
  "rationale": "Matched: Does it define LIMITS? Terms: keyword:latency, keyword:milliseconds",
  "ambiguous": false
}
```

**Ambiguous Classification:**
```json
{
  "tier": "FSD",
  "confidence": 0.45,
  "rationale": "Ambiguous: close scores between FSD, SAD. Apply scoring_matrix for resolution.",
  "ambiguous": true,
  "candidates": ["FSD", "SAD"],
  "next_step": "Use scoring_matrix tool to resolve ambiguity"
}
```

## Classification Criteria

| Question | Tier | Key Indicators |
|:---------|:-----|:---------------|
| Q1: WHY? | BRD | business value, ROI, stakeholder, strategic |
| Q2: LIMITS? | NFR | latency, SLA, performance, constraint, threshold |
| Q3: WHAT? | FSD | user shall, feature, capability, use case |
| Q4: HOW? | SAD | architecture, component, pattern, topology |
| Q5: SCHEMA? | ICD | API, schema, JSON, request/response, contract |
| Q6: CLASS? | TDD | class, method, signature, inheritance |

## Rules
- **Threshold**: Minimum 0.3 score to accept a tier match
- **Ambiguity**: Detected when top two scores differ by < 0.1
- **Tie-Breaking**: Higher abstraction tier wins (favor BRD over ISP)
