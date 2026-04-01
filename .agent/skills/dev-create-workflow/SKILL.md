---
name: dev-create-workflow
version: 1.0.0
description: Produces Antigravity v1.19+ optimized agent Workflows implementing proven techniques to reduce hallucinations, improve instruction following, and maximize token efficiency during agentic processing by Gemini 3.1 Pro.
---

<when_to_use>

- The user asks to create a new agent Workflow.
- The user asks to standardize or optimize an existing workflow for Antigravity v1.19+ and Gemini 3.1 Pro.
</when_to_use>

<how_to_use>

1. Confirm scope: Understand the repetitive task, trigger conditions, required scripts, resources, and expected verification plan.
2. Establish the base structure according to the `.agent/schemas/workflow/workflow.d.ts` schema.
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

- `.agent/schemas/workflow/workflow.d.ts`
- `.agent/schemas/workflow/example.md`
</resources_reference>
