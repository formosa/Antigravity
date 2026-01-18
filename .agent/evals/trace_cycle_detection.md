---
type: evaluation
name: "Cycle Detection"
description: "Validates detection of circular citation chains."
target_agent: "@traceability_auditor"
threshold: 100
metrics:
  - name: cycle_detection_rate
    type: percentage
    target: 100
test_cases: "test_cases/traceability.json"
schedule: "on_demand"
---

# Evaluation: Cycle Detection

## Test Procedure

1. Load test data with seeded cycles
2. Execute:
   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/build_dependency_graph.py" --needs-json "test_cases/cycle_needs.json"
   ```
3. Extract `cycles[]` from output
4. Calculate: `detection_rate = (detected / seeded) * 100`
5. Pass if `detection_rate == 100`
