---
type: evaluation
name: "ISP Docstring Completeness"
description: "Ensures all ISP stubs have complete NumPy-style docstrings."
target_agent: "@isp_codegenerator"
threshold: 100
metrics:
  - name: docstring_completeness
    type: percentage
    target: 100
test_cases: "inline"
schedule: "on_demand"
---

# Evaluation: ISP Docstring Completeness

## Test Procedure

1. Parse `needs.json` for ISP-tier tags, extract file paths
2. For each function, extract docstring
3. Verify sections: Summary, Parameters (if args), Returns (if not None), Raises, References
4. Calculate: `completeness = (complete / total) * 100`
5. Pass if `completeness == 100`
