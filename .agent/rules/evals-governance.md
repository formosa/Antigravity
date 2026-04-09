---
name: "evals-governance"
version: "1.0.0"
description: "Glob-scoped collection governance rule for the `.agent/evals/` directory, covering eval case-format consistency, case-ID uniqueness, reference validity against live rules and scripts, and prohibition of deprecated model or stale path references."
trigger: "glob"
globs: ".agent/evals/**"
priority: "high"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/evals/`. It MUST NOT impose governance requirements on `.agent/rules/`, `.agent/scripts/`, or `.agent/tools/`.
2. Eval Case Format: Eval case files MUST follow the established case-format pattern with clearly labeled sections: failure family, original bad command pattern, expected compliant pattern, and expected fallback behavior.
3. Case ID Uniqueness: Eval case IDs within each eval file MUST be unique and sequentially numbered using the `CASE-NNN` convention established in the existing eval surface.
4. Reference Validity: Eval cases MUST reference only rules, tools, or scripts that currently exist under `.agent/rules/`, `.agent/tools/`, or `.agent/scripts/`. Cases referencing removed or renamed assets MUST be updated or annotated in the same task.
5. No Deprecated Model References: Eval cases MUST NOT reference deprecated model IDs from the `deprecated_models` list in `.agent/config/runtime-target.yaml` as expected compliant patterns. Deprecated models MAY appear only in the "original bad command pattern" field to document historical failures.
6. No Stale File Paths: Eval cases MUST NOT reference file paths that no longer exist in the repository as expected compliant patterns.
7. Eval File Naming: Eval files MUST use lowercase underscore-separated naming that clearly identifies the target rule or capability being tested.

</constraints>

<verification_step>

1. If the target file is an eval case file, confirm each case follows the established case-format pattern with all required sections present.
2. Confirm all case IDs within the file are unique, sequential, and use the `CASE-NNN` convention.
3. Confirm all rule, tool, and script references in the eval cases point to assets that currently exist under their respective `.agent/` directories.
4. Confirm no expected compliant pattern uses a deprecated model ID from `runtime-target.yaml`.

</verification_step>
