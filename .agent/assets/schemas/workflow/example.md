---
name: strict-integration-deploy
description: Orchestrates a highly deterministic deployment pipeline involving static analysis, artifact generation, testing, and conditional merging using Gemini 3.1 Pro.
---

### steps

1. **Context Assimilation & Artifact Creation:** Analyze the staged modifications in the active workspace. Generate a summary document named `Pre_Deployment_Audit.md` detailing all detected changes, affected dependencies, and potential breaking points.
2. **Review Checkpoint:** Pause execution. **Request explicit human approval** of `Pre_Deployment_Audit.md` before proceeding to automated validation.
3. **Static Analysis & Skill Trigger:** Execute the workspace linter and type-checker.
    - If errors are detected, invoke semantic routing for diagnostic and debugging skills to resolve type conflicts automatically, then regenerate the audit artifact.
    - If no errors are detected, proceed to Step 4.
4. **Test Suite Execution (Decision Tree):** Run the comprehensive integration test suite. Use the following decision matrix to handle the output:
    - **IF** the test suite returns a 100% pass rate, **THEN** proceed to Step 5.
    - **IF** the test suite fails on newly implemented logic, **THEN** halt the workflow, capture the failure logs into `Error_Trace.md`, and notify the user.
    - **IF** the test suite fails on legacy, unmodified logic (regression), **THEN** immediately revert the staged changes and request human intervention.
5. **Codebase Modification:** Once tests pass, update the `CHANGELOG.md` artifact to reflect the verified modifications, adhering strictly to the required formatting guidelines.
    <changelog_constraints>
    - Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security.
    - Use imperative mood in all bullet points (e.g., "Add new endpoint", not "Added new endpoint").
    - Do not reference internal issue tracker IDs unless explicitly provided in the user prompt.
    </changelog_constraints>
6. **Final Verification:** Perform a final dry-run of the build process. Output the terminal build results as a final verifiable artifact to conclude the workflow.

### verification_plan

- The `Pre_Deployment_Audit.md` artifact must exist and be approved prior to any testing.
- The `CHANGELOG.md` artifact modification must strictly adhere to the XML-fenced `<changelog_constraints>`.
- The workflow must terminate deterministically based on the decision tree if any test regressions occur.
