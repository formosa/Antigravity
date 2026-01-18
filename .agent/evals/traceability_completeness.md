---
type: evaluation
name: "Traceability Completeness"
description: "Ensures all non-BRD tags have valid parent citations."
target_agent: "@traceability_auditor"
threshold: 100
metrics:
  - name: citation_coverage
    type: percentage
    target: 100
test_cases: "needs.json"
schedule: "on_demand"
---

# Evaluation: Traceability Completeness

## Test Procedure

1. Load all tags from `docs/_build/json/needs.json`
2. Filter to non-BRD tags
3. For each tag, verify `links` contains valid parent ID
4. Calculate: `coverage = (with_parent / total_non_brd) * 100`
5. Pass if `coverage == 100`
