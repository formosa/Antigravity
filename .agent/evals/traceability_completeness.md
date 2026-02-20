---
type: evaluation
name: "Traceability Completeness"
target_agent: "@traceability_auditor"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Audit a dataset with missing parent links"
  - "Audit a fully connected dataset"
rubric:
  - "Report orphan count equals seeded orphans"
  - "Report 100% coverage on clean dataset"
---

# Evaluation: Traceability Completeness

## Test Procedure

1. Load all tags from `docs/_build/json/needs.json`
2. Filter to non-BRD tags
3. For each tag, verify `links` contains valid parent ID
4. Calculate: `coverage = (with_parent / total_non_brd) * 100`
5. Pass if `coverage == 100`
