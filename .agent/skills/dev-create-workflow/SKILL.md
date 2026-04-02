---
name: dev-create-workflow
version: 1.0.2
description: Produces deterministic agent Workflow assets that encode repeatable execution steps and verification plans. Use when the task is to create or standardize a reusable workflow under `.agent/workflows/`. Do not use when the task is to create a skill, schema, or ordinary project feature change.
---

<when_to_use>

- The user asks to create a new agent Workflow.
- The user asks to standardize or optimize an existing workflow for Antigravity v1.19+ and Gemini 3.1 Pro.
- Do not use this skill when the request is to create a skill, schema, implementation plan, or ordinary project code change.
- Example prompt: "Create a workflow for reviewing schema changes before merge."
- Example prompt: "Standardize this existing workflow so it has clearer steps and verification."
</when_to_use>

<how_to_use>

1. Confirm scope: Understand the repetitive task, trigger conditions, required scripts, resources, and expected verification plan.
2. Establish the base structure according to the `resources/schema/workflow/workflow.d.ts` schema.
   - You MUST include a standard YAML frontmatter block `---` at the top of the file containing `name`, `version`, and `description`.
   - You MUST include a `body_content` section with `### steps` and optionally `### verification_plan`.
3. Implement workflow instructions:
   - Use precise, numbered atomic instructions inside the `### steps` section.
   - Group related checks and instructions. Use split-step verifications or human-in-the-loop checkpoints where explicit human approval matters for safety.
   - Utilize deterministic logic branches (e.g., IF X THEN Y) to handle different conditions.
   - Isolate strict formatting rules or constraints within descriptive XML-fenced tags (e.g., `<changelog_constraints>`).
   - Ground tasks by referencing known tools or files directly and avoid vague instructions to minimize hallucinations.
4. Add the verification plan: define conditions that must be met under `### verification_plan` to consider the workflow successfully complete.
5. Create the `.md` file in the `.agent/workflows/` directory.

Prefer clear, tightly-scoped instructions. Token efficiency is achieved through direct, unambiguous steps formatted correctly.
</how_to_use>

<constraints>
- Strict adherence to the `workflow.d.ts` schema is REQUIRED.
- Provide explicit instructions. Do NOT leave ambiguous execution verbs (e.g., "improve", "optimize") without measurable criteria.
- Ensure all steps are directly observable or executable by tools.
- Do NOT hallucinate dependencies or scripts; constrain workflows to reference existing tools or validated processes.
- Do NOT be overly verbose; maintain token efficiency by keeping steps bounded and concise.
</constraints>

<resources_reference>

- Read `resources/schema/workflow/workflow.d.ts` to verify the required workflow frontmatter and body contract.
- Read `resources/schema/workflow/example.md` to mirror the canonical workflow structure and verification plan style.
</resources_reference>
