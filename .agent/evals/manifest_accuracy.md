---
type: evaluation
name: "Manifest Accuracy"
description: "Validates manifest reflects actual DDR tag inventory."
target_agent: "@manifest_manager"
threshold: 100
metrics:
  - name: manifest_accuracy
    type: percentage
    target: 100
test_cases: "inline"
schedule: "on_demand"
---

# Evaluation: Manifest Accuracy

## Test Procedure

1. Execute:
   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/check_manifest_integrity.py" --needs-json "docs/_build/json/needs.json"
   ```
2. Parse output for `in_manifest_not_in_needs` and `in_needs_not_in_manifest`
3. Calculate: `accuracy = (matching / total) * 100`
4. Pass if `accuracy == 100` and both mismatch counts are 0
