---
type: evaluation
name: "DDR Anti-Pattern Detection"
description: "Validates detection of all known documentation anti-patterns."
target_agent: "@ddr_orchestrator"
threshold: 100
metrics:
  - name: detection_rate
    type: percentage
    target: 100
test_cases: "test_cases/anti_patterns.json"
schedule: "on_demand"
---

# Evaluation: DDR Anti-Pattern Detection

## Test Procedure

1. Load test data from `test_cases/anti_patterns.json`
2. Execute:
   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/detect_anti_patterns.py" --needs-json "test_cases/anti_patterns_needs.json"
   ```
3. Verify each expected pattern appears in output
4. Calculate: `detection_rate = (detected / expected) * 100`
5. Pass if `detection_rate == 100`
