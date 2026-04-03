---
name: asset-workflow
version: 2.0.0
description: Authors or refines Antigravity-compatible workflow assets with explicit trigger boundaries, scaffold and validation tooling, and deterministic workflow-index synchronization. Use when the task is to create or standardize a reusable workflow under `.agent/workflows/`. Do not use when the task is to create a skill, schema, implementation plan, or ordinary project feature change.
---

<when_to_use>

- Use when the user asks to create, scaffold, standardize, or harden a workflow in `.agent/workflows/`.
- Use when the task is to improve workflow trigger wording, execution-step determinism, verification plans, or workflow-index hygiene.
- Do not use when the request is to create a skill, schema, implementation plan, or ordinary project code change.
- Example prompt: "Create a workflow for reviewing schema changes before merge."
- Example prompt: "Standardize this existing workflow so it has clearer steps and verification."
</when_to_use>

<how_to_use>

1. Gather 2-3 concrete requests the target workflow must handle. Extract the repetitive trigger, required inputs, expected outputs, and adjacent tasks the workflow must reject.
2. Decide whether to scaffold or refine:
   - Run `python .agent/skills/asset-workflow/scripts/init_workflow.py <workflow-name> [--path <output-directory>]` when creating a new workflow.
   - Open the existing `.agent/workflows/<workflow-name>.md` when standardizing or tightening a live workflow.
3. Author the workflow against the `workflow` schema:
   - include YAML frontmatter with `version` and `description`, plus `name` when it improves routing clarity
   - encode the execution body under `### steps`
   - add `### verification_plan` when completion checks are material to safe reuse
   - use precise, numbered actions, deterministic IF/THEN branches, and XML-fenced constraints only when they reduce ambiguity
4. Keep the workflow lightweight:
   - reference only existing tools, skills, files, or validated processes
   - do not invent packaging behavior, sidecar reports, or extra artifact sections unless the workflow itself requires them
5. Validate with `python .agent/skills/asset-workflow/scripts/quick_validate.py <workflow-path>`. Resolve structural failures before proceeding.
6. Update the workflow directory index with `python .agent/skills/asset-workflow/scripts/update_index.py` so `.agent/workflows/index.md` stays aligned with the live workflow set.
7. Trigger-test the finished workflow with at least one prompt that should invoke it and one adjacent prompt that should not. Refine the description or boundary wording until routing is predictable.
</how_to_use>

<constraints>
- Strict adherence to the `workflow.d.ts` schema is REQUIRED.
- Provide explicit instructions. Do NOT leave ambiguous execution verbs (e.g., "improve", "optimize") without measurable criteria.
- Ensure all steps are directly observable or executable by tools.
- Do NOT hallucinate dependencies or scripts; constrain workflows to reference existing tools or validated processes.
- Do NOT hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/`.
- Keep workflow-local paths repo-relative and written with forward slashes.
- Do NOT be overly verbose; maintain token efficiency by keeping steps bounded and concise.
</constraints>

<resources_reference>

- Run `.agent/skills/asset-workflow/scripts/init_workflow.py` to scaffold a new workflow from the canonical example structure.
- Run `.agent/skills/asset-workflow/scripts/quick_validate.py` to detect structural workflow errors before handoff.
- Run `.agent/skills/asset-workflow/scripts/update_index.py` to rebuild `.agent/workflows/index.md` after workflow changes.
- Read `.agent/skills/asset-skill/resources/owner-skill-pattern.md` to preserve the shared owner-skill lifecycle and governance model while keeping workflow responsibilities role-appropriate.
- Read `resources/schema/workflow/workflow.d.ts` to verify the required workflow frontmatter and body contract.
- Read `resources/schema/workflow/example.md` to mirror the canonical workflow structure and verification-plan style.
- Read `resources/schema/index/index.d.ts` to preserve the full-form workflow-index contract used by `.agent/workflows/index.md`.
- Read `resources/schema/index/example.md` to preserve section order, manifest shape, and authority-boundary wording in the workflow index.
</resources_reference>
