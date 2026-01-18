---
type: evaluation
name: "Orphan Detection"
description: "Validates detection of orphan tags (missing parent citations)."
target_agent: "@traceability_auditor"
threshold: 100
metrics:
  - name: orphan_detection_rate
    type: percentage
    target: 100
test_cases: "test_cases/traceability.json"
schedule: "on_demand"
---

# Evaluation: Orphan Detection

## Test Procedure

1. Load test data with seeded orphans
2. Execute:
   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/generate_traceability_report.py" --needs-json "test_cases/orphan_needs.json" --format json
   ```
3. Extract `orphans[]` from output
4. Calculate: `detection_rate = (detected / seeded) * 100`
5. Pass if `detection_rate == 100`
