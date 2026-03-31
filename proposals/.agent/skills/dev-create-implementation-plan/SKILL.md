---
name: dev-create-implementation-plan
version: 4.2.0
description: Produces a schema-compatible, deterministic Antigravity implementation-plan artifact optimized for grounded planning, token efficiency, and safe executor handoff.
---

<when_to_use>

- The user asks for an implementation plan before coding.
- The user asks to refine, regenerate, or audit an existing implementation plan artifact.
- The task has non-trivial scope, dependencies, or risk and needs deterministic execution steps.
- The task requires a human-approved planning artifact before any code or file modifications occur.
</when_to_use>

<how_to_use>

## Operating mode

- Planner model: `gemini-3.1-pro` with high reasoning.
- Executor model target: `gemini-3-flash` (or project default execution model).
- IDE target: Antigravity v1.18+.

## Contract preservation rules

- Preserve compatibility with:
  - `.agent/schemas/implementation-plan/implementation-plan.d.ts`
  - `.agent/schemas/implementation-plan/example.md`
  - `.agent/skills/dev-create-skill/resources/output-patterns.md`
  - accepted implementation-plan artifacts already present in the project
- Do not introduce unsupported frontmatter fields.
- Do not introduce new top-level artifact sections.
- Keep the implementation-plan artifact shape stable unless the schema and companion documentation are revised together.

## Deterministic protocol

1. **Load and prioritize local context first**
   - Read the user request, referenced files, and relevant project docs.
   - Read decision memory if present: `.gemini/antigravity/brain/`.
   - Verify existence of referenced files and other files that are plausibly material to correctness.
   - Do not assume a missing file is irrelevant.
   - Do not halt on missing files unless the absence blocks deterministic planning.

2. **Establish scope and execution boundary**
   - Identify the implementation objective, in-scope files, likely out-of-scope files, and interfaces touched.
   - Preserve the narrowest grounded scope.
   - Do not expand scope merely because adjacent files might exist.

3. **Run ambiguity gate**
   - If required inputs are missing, conflicting, unreadable, or materially under-specified, output an RFQ artifact and stop.
   - Distinguish between:
     - **blocking ambiguity** -> RFQ and halt
     - **non-blocking uncertainty** -> capture as a concise assumption, dependency note, or risk note in the plan
   - Never infer hidden requirements.

4. **Perform focused validation research (only if needed)**
   - Use external docs only for API/framework behavior not derivable from local files.
   - Prefer official vendor docs, changelogs, standards, and primary references.
   - If evidence conflicts and cannot be resolved confidently, output RFQ and stop.
   - Never let external research override explicit local project requirements without calling out the conflict.

5. **Generate the execution plan artifact**
   - Create a standalone Antigravity artifact, not inline conversational prose, when artifact output is available.
   - Because this skill is for non-trivial planning work, include `<phases>` by default.
   - Use the smallest number of phases and steps that preserves clarity, determinism, and safe handoff.
   - Keep every emitted step scoped, testable, and ordered.

6. **Apply internal step validation before emission**
   - Before finalizing each step, validate internally that it has:
     - grounded target files or artifacts
     - a concrete action
     - a bounded intended outcome
     - a clear dependency order when needed
     - side effects contained to in-scope surfaces
     - a viable verification path
   - Use this validation internally.
   - Do not add hidden rubric sections to the artifact unless the project contract is formally expanded.

7. **Attach the verification contract**
   - Add one verification item per atomic step.
   - Maintain a 1:1 mapping between `<atomic_steps>` and `<verification>`.
   - Use the lightest verification method that still proves the intended post-state.
   - If no grounded verification path exists, output RFQ and stop.

8. **Handle review, rollback, and failure deterministically**
   - Use review policy internally to decide when explicit human review is required.
   - Surface human review gates only when they materially affect execution sequencing or safety.
   - Capture rollback or containment guidance inside `<risks_and_mitigations>` when risk justifies it.
   - Plans must assume halt-on-failed-verification behavior for dependent work.
   - Do not add a separate failure-contract section unless the schema is formally revised.

## Required artifact structure

Use this exact order:

1. YAML frontmatter
2. `<objective>`
3. `<phases>`
4. `<atomic_steps>`
5. `<verification>`
6. `<risks_and_mitigations>` (optional but recommended for non-trivial tasks)

## Frontmatter (required)

```yaml
---
task: "<one-sentence measurable objective>"
model: "gemini-3.1-pro"
version: "1.0.0"
---
```

## Objective rules

- State one measurable implementation objective.
- Do not hide secondary work inside broad wording.
- Keep it precise enough that approval or rejection is straightforward.

## Phase rules

- Use phases to express major execution boundaries, approval boundaries, or dependency boundaries.
- Each phase should have a stable purpose and clear entry/exit conditions.
- Avoid ceremonial over-phasing.
- Prefer a small number of phases with meaningful orchestration value.

## Atomic step rules

- Emit concise numbered steps.
- Each step must represent a single bounded responsibility.
- Each step must identify the target file(s), artifact(s), or system surface when applicable.
- State `CREATE`, `MODIFY`, or `DELETE` behavior explicitly when omission could cause ambiguity.
- Prefer repeat-safe wording where feasible.
- Avoid combining unrelated edits in a single step.
- Do not include speculative alternatives unless explicitly requested.
- High-risk or destructive actions must be explicit, narrowly scoped, and paired with mitigation in `<risks_and_mitigations>`.

## Verification rules

- Every verification item must map to the step with the same number.
- Verification must prove the intended result, not merely that activity occurred.
- Acceptable verification approaches include:
  - command-based validation
  - static inspection
  - type checking
  - test assertions
  - structural validation
  - semantic validation
- Prefer existing project commands and checks.
- Do not invent commands, tests, or success results.
- Manual inspection is acceptable when command-based validation is unavailable and the inspection criterion is precise.

## Internal review policy mapping

Use this policy internally while composing the plan:

- **Always Proceed (low risk):**
  - isolated internal logic
  - formatting-only changes
  - local private implementation adjustments
  - no schema, migration, public API, persistence, dependency, or cross-system contract changes

- **Agent Decides (moderate):**
  - bounded refactors
  - moderate internal restructuring
  - reversible implementation changes with limited blast radius

- **Request Review (high):**
  - schema or data migrations
  - dependency or version changes
  - public API changes
  - irreversible side effects
  - persistence, deployment, security, or cross-system contract changes

Do not downgrade high-risk work through wording.

## RFQ format (hard halt output)

```markdown
## RFQ — Request for Clarification

**Triggered by**: <phase/step + blocking condition>

**Blocking items**:
- [ ] <specific missing, conflicting, unreadable, or ambiguous item>

**Why this blocks deterministic planning**:
- <brief grounded explanation>

**Resolution required before**: implementation-plan generation

**Do not proceed** until all items are resolved.
```

## Token-efficiency rules

- Prefer concise bullets over narrative when precision is preserved.
- Be concise, but never omit determinism-critical detail.
- Include only files, modules, and interfaces that are actually in scope.
- Do not repeat global constraints inside every phase or step unless repetition is necessary for safety.
- Avoid decorative explanation and speculative branches.

## Anti-hallucination rules

- Ground every technical decision in local file evidence or cited external docs when external validation is required.
- Never invent files, APIs, symbols, commands, tests, migrations, or outcomes.
- Never convert uncertainty into certainty through wording.
- Never claim verification succeeded inside the plan artifact.
- If the plan cannot ground the objective, scope, step sequence, or verification path, halt and emit RFQ.

</how_to_use>

<constraints>

- Do not output the final plan as generic chat markdown when artifact output is available.
- Do not introduce unsupported frontmatter keys or new top-level sections.
- Do not proceed past unresolved blocking ambiguity.
- Do not modify out-of-scope files in the generated plan.
- Do not assign low-risk treatment to schema, API, dependency, persistence, security, or migration work.
- Do not claim side-effect freedom unless the scope boundary is explicitly defined and preserved.
- Do not invent verification commands or execution results.

</constraints>

<resources_reference>

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `.agent/skills/dev-create-skill/resources/output-patterns.md`
- `.gemini/antigravity/brain/`

</resources_reference>
