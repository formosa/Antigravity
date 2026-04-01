---
name: dev-create-implementation-plan
version: 5.0.0
description: Produces a schema-compatible, deterministic Antigravity implementation-plan artifact optimized for grounded planning, token efficiency, safe executor handoff, and progress-tracked lifecycle management.
---

<when_to_use>

- The user asks for an implementation plan before coding.
- The user asks to refine, regenerate, or audit an existing implementation plan artifact.
- The task has non-trivial scope, dependencies, or risk and needs deterministic execution steps.
- The task requires a human-approved planning artifact before any code or file modifications occur.
</when_to_use>

<how_to_use>

## Operating mode

- Planner model: `gemini-3.1-pro-preview` with `thinking_level: HIGH` for architectural planning; use `thinking_level: MEDIUM` for standard or bounded engineering tasks to optimize cost and latency.
- Executor model target: `gemini-3-flash` (or `gemini-3.1-flash` if available in the active project environment).
- Custom-tool workflows: prefer `gemini-3.1-pro-preview-customtools` endpoint when the plan involves structured tool orchestration (view_file, search_code, bash).
- IDE target: Antigravity v1.20.3+ (AGENTS.md rules loaded automatically alongside GEMINI.md; auto-continue enabled by default).

## Contract preservation rules

- Preserve compatibility with:
  - `.agent/schemas/implementation-plan/implementation-plan.d.ts`
  - `.agent/schemas/implementation-plan/example.md`
  - `.agent/skills/dev-create-skill/resources/output-patterns.md`
  - accepted implementation-plan artifacts already present in `.agent/plans/`
- Do not introduce unsupported frontmatter fields.
- Do not introduce new top-level artifact sections.
- Keep the implementation-plan artifact shape stable unless the schema and companion documentation are revised together.

## Plan naming, storage, and lifecycle

### Naming scheme
Every new plan artifact MUST use the following filename format, generated at creation time:
```
YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md
```

- `YYYYMMDD` — ISO date, local system date at creation (e.g., `20260401`)
- `HHMMSS`   — 24-hour local time at creation (e.g., `143022`)
- `<uuid8>`  — First 8 characters of a newly generated UUID v4 (e.g., `a3f7c12b`)
- Suffix is always `-IMPLEMENTATION_PLAN.md` (uppercase, hyphen-separated)

Example: `20260401-143022-a3f7c12b-IMPLEMENTATION_PLAN.md`

### Storage paths
- **Active plans:** `.agent/plans/`
- **Completed plans:** `.agent/plans/processed/`

### Lifecycle rule
Upon COMPLETE and SUCCESSFUL execution of ALL steps in the plan (every progress checkbox marked `[X]`), the agent MUST relocate the artifact:
```
MOVE .agent/plans/<filename> → .agent/plans/processed/<filename>
```

Do not modify the filename during relocation. Do not relocate partially completed plans.

## Progress tracking

For plans classified as **long-running**, **complex**, or **high-risk** (see internal review policy below), atomic steps MUST be organized into named sections with progress tracking checkboxes:
```markdown
### <SECTION_NAME>

- [ ] Step N — <description>
- [ ] Step N+1 — <description>
```

Checkbox update rule: immediately after each section's successful completion during agentic execution, update every checkbox in that section from `[ ]` to `[X]`. Do not batch updates across sections. Update the on-disk artifact before proceeding to the next section.

For **simple, low-risk plans**, progress tracking checkboxes are optional but permitted.

## Deterministic protocol

1. **Load and prioritize local context first**
   - Read the user request, referenced files, and relevant project docs.
   - Read decision memory if present: `.gemini/antigravity/brain/`.
   - Verify existence of referenced files and other files plausibly material to correctness.
   - Do not assume a missing file is irrelevant.
   - Do not halt on missing files unless the absence blocks deterministic planning.

2. **Establish scope and execution boundary**
   - Identify the implementation objective, in-scope files, likely out-of-scope files, and interfaces touched.
   - Preserve the narrowest grounded scope.
   - Do not expand scope merely because adjacent files might exist.

3. **Run ambiguity gate**
   - If required inputs are missing, conflicting, unreadable, or materially under-specified, output an RFQ artifact and stop.
   - Distinguish between:
     - **blocking ambiguity** → RFQ and halt
     - **non-blocking uncertainty** → capture as a concise assumption, dependency note, or risk note in the plan
   - Never infer hidden requirements.

4. **Perform focused validation research (only if needed)**
   - Use external docs only for API/framework behavior not derivable from local files.
   - Prefer official vendor docs, changelogs, standards, and primary references.
   - If evidence conflicts and cannot be resolved confidently, output RFQ and stop.
   - Never let external research override explicit local project requirements without calling out the conflict.

5. **Generate the execution plan artifact**
   - Create a standalone Antigravity artifact saved to `.agent/plans/` using the required naming scheme.
   - Do not emit the plan as inline conversational prose.
   - Because this skill is for non-trivial planning work, include `<phases>` by default.
   - Use the smallest number of phases and steps that preserves clarity, determinism, and safe handoff.
   - For long-running, complex, or high-risk plans: organize `<atomic_steps>` into named sections with progress tracking checkboxes.
   - Keep every emitted step scoped, testable, and ordered.

6. **Apply internal step validation before emission**
   - Before finalizing each step, validate internally that it has:
     - grounded target files or artifacts
     - a concrete action
     - a bounded intended outcome
     - a clear dependency order when needed
     - side effects contained to in-scope surfaces
     - a viable verification path
   - Use this validation internally; do not add hidden rubric sections to the artifact.

7. **Attach the verification contract**
   - Add one verification item per atomic step.
   - Maintain a 1:1 mapping between `<atomic_steps>` and `<verification>`.
   - Use the lightest verification method that still proves the intended post-state.
   - If no grounded verification path exists, output RFQ and stop.

8. **Handle review, rollback, and failure deterministically**
   - Surface human review gates only when they materially affect execution sequencing or safety.
   - Capture rollback or containment guidance inside `<risks_and_mitigations>` when risk justifies it.
   - Plans must assume halt-on-failed-verification behavior for dependent work.
   - Do not add a separate failure-contract section unless the schema is formally revised.

## Required artifact structure

Use this exact order:

1. YAML frontmatter
2. `<objective>`
3. `<phases>`
4. `<atomic_steps>` (with progress-tracking sections for complex/long-running/high-risk plans)
5. `<verification>`
6. `<risks_and_mitigations>` (optional but recommended for non-trivial tasks)

## Frontmatter (required)
```yaml
---
task: "<one-sentence measurable objective>"
model: "gemini-3.1-pro-preview"
version: "1.0.0"
thinking_level: "MEDIUM"
---
```

> Use `thinking_level: HIGH` for architectural planning, novel algorithm design, or multi-system coordination. Use `thinking_level: MEDIUM` for bounded implementation work. Never omit `thinking_level`.

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
- For complex/long-running/high-risk plans, group steps into named sections with progress checkboxes (see Progress tracking above).

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
- For plans with large context inputs (>50K tokens): restate the objective and critical constraints at the END of the artifact to anchor executor attention across the full context window.

## Anti-hallucination rules

- Ground every technical decision in local file evidence or cited external docs when external validation is required.
- Never invent files, APIs, symbols, commands, tests, migrations, or outcomes.
- Never convert uncertainty into certainty through wording.
- Never claim verification succeeded inside the plan artifact.
- If the plan cannot ground the objective, scope, step sequence, or verification path, halt and emit RFQ.

</how_to_use>

<constraints>

- Do not output the final plan as generic chat markdown; always write to `.agent/plans/` using the required naming scheme.
- Do not introduce unsupported frontmatter keys or new top-level sections.
- Do not proceed past unresolved blocking ambiguity.
- Do not modify out-of-scope files in the generated plan.
- Do not assign low-risk treatment to schema, API, dependency, persistence, security, or migration work.
- Do not claim side-effect freedom unless the scope boundary is explicitly defined and preserved.
- Do not invent verification commands or execution results.
- Do not relocate a plan to `.agent/plans/processed/` until ALL progress checkboxes are marked `[X]`.
- Do not omit `thinking_level` from the frontmatter.
</constraints>

<resources_reference>

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `.agent/skills/dev-create-skill/resources/output-patterns.md`
- `.agent/plans/` (active plans)
- `.agent/plans/processed/` (completed plans)
- `.gemini/antigravity/brain/`
</resources_reference>
