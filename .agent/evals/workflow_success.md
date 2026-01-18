---
type: evaluation
name: "Workflow Success Rate"
description: "Validates complete 9-stage workflow execution."
target_agent: "@ddr_orchestrator"
threshold: 9
metrics:
  - name: stages_completed
    type: count
    target: 9
test_cases: "inline"
schedule: "on_demand"
---

# Evaluation: Workflow Success Rate

## Test Procedure

1. Execute `/complete_feature` with test input
2. Track completion of each stage (1-9)
3. Verify each stage returns valid tag ID
4. Pass if `stages_completed == 9`
