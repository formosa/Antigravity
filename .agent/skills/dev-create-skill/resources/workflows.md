<document_purpose>
This document defines observable workflow patterns for authoring deterministic Antigravity skills without relying on unverifiable claims about internal reasoning.
</document_purpose>

<decision_tree_patterns>
For branching logic, write explicit IF/THEN choices grounded in observable state so the agent can justify each branch with a file check, command result, or user-provided fact.

Example implementation inside a `<how_to_use>` block:

1. Check whether the required tool or file exists.
2. **IF** the dependency is missing and the skill permits installation, **THEN** run the documented install step and capture the result.
3. **IF** the dependency is missing and installation requires approval, **THEN** ask for approval and halt further execution.
4. **IF** the dependency is present, **THEN** continue to the next step.
</decision_tree_patterns>

<validation_loop_patterns>
Prefer observable planning and validation loops over directions such as "silently reason" or "silently self-correct."

Example implementation:

1. Produce an intermediate artifact such as `changes.json`, `plan.md`, or a generated file draft.
2. Run a validator or structural check against that artifact.
3. **IF** validation fails, revise the artifact using the reported error and rerun validation.
4. **IF** validation passes, apply or emit the final result and run the final verification step.

This pattern keeps failure handling machine-verifiable and auditable.
</validation_loop_patterns>

<instruction_structuring_patterns>
Use explicit structural boundaries so the skill separates routing, execution, and constraints cleanly.

- Put trigger boundaries in `description` and `<when_to_use>`.
- Put hard safety and scope boundaries in `<constraints>`.
- Put ordered actions, inputs, outputs, and verification in `<how_to_use>`.
- Reference detailed files directly from `<resources_reference>` so the agent can decide whether to read or run them.
</instruction_structuring_patterns>
