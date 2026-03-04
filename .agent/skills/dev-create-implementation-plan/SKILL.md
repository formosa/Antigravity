---
name: dev-create-implementation-plan
version: 4.0.0
description: Produces a deterministic Antigravity implementation-plan artifact for Gemini 3.1 Pro planning and Gemini execution agents.
---

<when_to_use>

- The user asks for an implementation plan before coding.
- The user asks to refine or regenerate an existing implementation plan artifact.
- The task has non-trivial scope, dependencies, or risk and needs deterministic execution steps.
</when_to_use>

<how_to_use>

## Operating mode

- Planner model: `gemini-3.1-pro` with high reasoning.
- Executor model target: `gemini-3-flash` (or project default execution model).
- IDE target: Antigravity v1.18+.

## Deterministic protocol

1. **Load local context only first**
   - Read user request, referenced files, and relevant project docs.
   - Read decision memory if present: `.gemini/antigravity/brain/`.
   - Do not assume missing files are irrelevant; verify existence explicitly.
2. **Run ambiguity gate (hard halt)**
   - If required inputs are missing, conflicting, or unreadable, output an RFQ artifact and stop.
   - Never infer hidden requirements.
3. **Perform focused validation research (only if needed)**
   - Use external docs only for APIs/framework behavior not derivable from local files.
   - Prefer official vendor docs and changelogs.
   - If evidence conflicts and cannot be resolved, output RFQ and stop.
4. **Generate execution plan artifact**
   - Create a standalone Antigravity artifact (not inline conversational prose).
   - Structure content so each step is atomic, testable, and reversible.
   - Map each step to a review policy based on risk.
5. **Attach verification contract**
   - Add one verification command/check per atomic step.
   - Require rollback procedure for high-risk steps.

## Required artifact structure

Use this exact order:

1. YAML frontmatter
2. `<objective>`
3. `<phases>` (omit only for truly single-phase work)
4. `<atomic_steps>`
5. `<verification>`
6. `<risks_and_mitigations>` (optional but recommended for non-trivial tasks)

## Frontmatter (required)

```yaml
---
task: "<one-sentence measurable objective>"
model: "gemini-3.1-pro"
---
```

## Atomic step contract (required fields)

For each step include:

- Step number
- Target file(s)
- Component/function/class signature
- Operation (`CREATE|MODIFY|DELETE`)
- Review policy (`Always Proceed|Agent Decides|Request Review`)
- PRE-condition (verifiable)
- Deterministic logic definition
- PROHIBIT clause
- POST-condition (verifiable)
- Dependency (`N/A` or step reference)

If any field cannot be grounded in project evidence, write `UNKNOWN — RFQ required` and halt.

## Review policy mapping

- **Always Proceed (low risk):** isolated internal logic, no schema/API surface changes.
- **Agent Decides (moderate):** refactors or internal structure changes with bounded risk.
- **Request Review (high):** schema/data migrations, public API changes, dependency/version changes, irreversible side effects.

## RFQ format (hard halt output)

```markdown
## RFQ — Request for Clarification

**Triggered by**: <phase + blocking condition>

**Blocking items**:
- [ ] <specific missing/ambiguous item>

**Resolution required before**: implementation-plan generation

**Do not proceed** until all items are resolved.
```

## Token-efficiency rules

- Prefer concise bullet points over narrative.
- Do not repeat constraints in every section.
- Avoid speculative alternatives unless explicitly requested.
- Include only files/modules in-scope for this task.

## Anti-hallucination rules

- Ground every technical decision in either local file evidence or cited external docs.
- Never invent files, APIs, symbols, terminal commands, or test results.
- If PRE/POST conditions cannot be verified, halt and emit RFQ.
</how_to_use>

<constraints>
- Do not output the final plan as chat markdown when artifact output is available.
- Do not proceed past unresolved ambiguity.
- Do not assign `Always Proceed` to high-risk operations.
- Do not modify out-of-scope files in the generated plan.
</constraints>

<resources_reference>

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `.gemini/antigravity/brain/`
</resources_reference>
