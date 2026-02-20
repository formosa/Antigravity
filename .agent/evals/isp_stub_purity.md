---
type: evaluation
name: "ISP Stub Purity"
target_agent: "@isp_codegenerator"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan ISP functions for implementation logic"
  - "Verify only pass or raise NotImplementedError"
rubric:
  - "Zero implementation logic allowed"
  - "Only structural definitions and docstrings permitted"
---

# Evaluation: ISP Stub Purity

## Test Procedure

1. Parse `needs.json` for ISP-tier tags, extract file paths
2. For each Python file, parse AST
3. For each function, verify body contains only `raise NotImplementedError` (docstring allowed)
4. Calculate: `purity = (pure / total) * 100`
5. Pass if `purity == 100`