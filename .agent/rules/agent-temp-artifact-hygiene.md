---
name: "AGENT_TEMP_ARTIFACT_HYGIENE"
version: "1.2.0"
description: "Always-on containment and cleanup policy for one-off agent scripts, diagnostics, and transient run artifacts in the Antigravity workspace."
trigger: "always_on"
priority: "high"
execution_tier: "standard"
---

<constraints>

1. Single-Run Artifact Containment: One-off scripts, helper programs, ad hoc JSON or CSV outputs, scratch notes, logs, and transient diagnostics created for a single task MUST live only under `.agent/.temp/<run-dir>/`.
2. Required Run-Directory Naming: Each temp run directory MUST use the format `YYYYMMDD-HHMMSS-<uuid8>-<task-slug>/` where `<uuid8>` is eight lowercase hexadecimal characters and `<task-slug>` is a short lowercase hyphenated label.
3. No Scattered Scratch Files: Agents MUST NOT leave temporary artifacts in the repository root, under `.agent/assets/**`, beside durable source files, or inside any other unmanaged scratch location.
4. Promotion Boundary: If a script becomes reusable, the agent MUST move or rewrite it into `.agent/scripts/` or a relevant skill-local `scripts/` directory before task completion and remove the temp copy.
5. Success Cleanup Requirement: On successful completion, the agent MUST delete its own `.agent/.temp/<run-dir>/` directory before finishing.
6. Failure Retention Boundary: On failure, the agent MAY retain only its own `.agent/.temp/<run-dir>/` directory. Retained failure directories MUST include a `retained-on-failure.txt` marker containing a short reason, and the final report MUST repeat the exact retained path plus that reason.
7. Durable Asset Separation: Temp artifacts MUST NOT be referenced from durable indexes, manifests, plans, schemas, or proposal assets unless the reference points to a promoted durable script outside `.agent/.temp/`.
8. Tool-Managed Exceptions: Durable operator tools MAY create transient outputs only inside `.agent/.temp/`, and any such tool-managed directories MUST still follow the standard run-directory naming convention.

</constraints>

<verification_step>

Before finishing a task, silently verify: every newly created single-run artifact is inside `.agent/.temp/`; any retained failure directory is scoped to one run, correctly named, and contains `retained-on-failure.txt`; no temp artifacts remain in repo root or durable asset locations; and every script worth keeping has been promoted into a durable scripts location and indexed there when applicable.

</verification_step>
