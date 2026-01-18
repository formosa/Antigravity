---
type: evaluation
name: "ISP Stub Purity"
description: "Ensures ISP stubs contain only NotImplementedError, no logic."
target_agent: "@isp_codegenerator"
threshold: 100
metrics:
  - name: stub_purity
    type: percentage
    target: 100
test_cases: "inline"
schedule: "on_demand"
---

# Evaluation: ISP Stub Purity

## Test Procedure

1. Parse `needs.json` for ISP-tier tags, extract file paths
2. For each Python file, parse AST
3. For each function, verify body contains only `raise NotImplementedError` (docstring allowed)
4. Calculate: `purity = (pure / total) * 100`
5. Pass if `purity == 100`
