---
type: evaluation
name: "ISP Docstring Completeness"
target_agent: "@isp_codegenerator"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan ISP functions for NumPy style docstrings"
  - "Check for missing Implements/Requirements sections"
rubric:
  - "All functions must have a docstring"
  - "Docstrings must follow NumPy format"
  - "Must include traceability links"
---

# Evaluation: ISP Docstring Completeness

## Test Procedure

1. Parse `needs.json` for ISP-tier tags, extract file paths
2. For each function, extract docstring
3. Verify sections: Summary, Parameters (if args), Returns (if not None), Raises, References
4. Calculate: `completeness = (complete / total) * 100`
5. Pass if `completeness == 100`
