---
type: evaluation
name: "Workflow Success Rate"
target_agent: "@ddr_orchestrator"
judge_model: "gemini-3.1-pro"
pass_threshold: 90
scenarios:
  - "Execute /complete_feature for a new 'Voice Activation' feature"
  - "Execute /complete_feature for a complex 'Data Persistence' module"
rubric:
  - "All 9 stages (BRD to Validate) must be completed in order"
  - "Each stage must produce the required rst artifacts"
  - "Traceability links must be correctly generated between tiers"
---

# Evaluation: Workflow Success Rate

## Test Procedure

1. Execute `/complete_feature` with test input.
2. Track completion of each stage (1-9).
3. Verify output artifacts exist in `docs/`.

## Success Criteria

- All 9 stages documented.
- Valid traceability chain from ISP to BRD.
- No orphan tags created during the process.