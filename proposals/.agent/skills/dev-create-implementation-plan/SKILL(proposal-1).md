---
name: dev-create-implementation-plan
version: 5.0.0
description: Produces a schema-compatible, deterministic Antigravity implementation-plan artifact optimized for grounded planning, token efficiency, task-tracker visibility, and safe executor handoff.
---

<when_to_use>

- The user requests an implementation plan before coding begins.
- The user asks to refine, regenerate, or audit an existing implementation plan artifact.
- The task has non-trivial scope, dependencies, or risk requiring deterministic execution steps.
- A human-approved planning artifact is required before any code or file modifications occur.

</when_to_use>

<how_to_use>

## Operating mode

- **Planner model:** `gemini-3.1-pro-preview` (high reasoning).
- **Executor model target:** `gemini-3-flash` (high-volume, low-latency implementation steps).
- **IDE target:** Antigravity v1.20.3+.
- **Rules file:** `AGENTS.md` (primary, v1.20.3+); `GEMINI.md` (fallback if `AGENTS.md` absent).
- **Auto-continue:** Enabled by default in v1.20.3+. Plans must be structured to tolerate uninterrupted executor handoff.

## Contract preservation rules

Preserve compatibility with:

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `.agent/skills/dev-create-skill/resources/output-patterns.md`
- Accepted implementation-plan artifacts present in `.agent/plans/`

Do not introduce unsupported frontmatter fields, new top-level artifact sections, or contract-breaking structural changes without revising the schema and all companion documentation simultaneously.

## File naming and storage

Every new Implementation Plan artifact **must** comply with the following rules:

| Rule                     | Specification                                                        |
| :----------------------- | :------------------------------------------------------------------- |
| **Output path**          | `.agent/plans/`                                                      |
| **Filename pattern**     | `YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md`                     |
| **`<uuid8>`**            | First 8 hex characters of a newly generated UUID4 (e.g., `a1b2c3d4`) |
| **Example filename**     | `20260401-143022-f3a91b2c-IMPLEMENTATION_PLAN.md`                    |
| **Post-processing path** | `.agent/plans/processed/`                                            |

**Post-processing relocation:** Upon executor confirmation that all atomic steps are complete and all verification checks pass, the executor **must** move the artifact from `.agent/plans/` to `.agent/plans/processed/`. Do not delete the artifact.

## Deterministic protocol

Execute these steps in order. Do not skip or reorder.

1. **Load and prioritize local context**
   - Read user request, referenced files, `AGENTS.md` (or `GEMINI.md`), and `.gemini/antigravity/brain/` decision memory.
   - Verify existence of all referenced and plausibly material files.
   - Do not assume a missing file is irrelevant.
   - Do not halt on missing files unless absence blocks deterministic planning.

2. **Establish scope and execution boundary**
   - Identify: implementation objective, in-scope files, out-of-scope files, touched interfaces.
   - Enforce the narrowest grounded scope. Do not expand scope because adjacent files may exist.

3. **Run ambiguity gate**
   - Classify each uncertainty:
     - **Blocking ambiguity** → emit RFQ artifact and halt.
     - **Non-blocking uncertainty** → capture as a concise assumption, dependency note, or risk note inside the plan.
   - Never infer hidden requirements. Never convert uncertainty into certainty through wording.

4. **Perform focused validation research (only when required)**
   - Use external docs only for API or framework behavior not derivable from local files.
   - Prefer official vendor docs, changelogs, and primary references.
   - If evidence conflicts and cannot be resolved, emit RFQ and halt.
   - Never let external research override explicit local project requirements without calling out the conflict.

5. **Generate the execution plan artifact**
   - Create a standalone Antigravity artifact; do not emit inline conversational markdown.
   - Use `<phases>` by default for non-trivial work.
   - Use the fewest phases and steps that preserves clarity, determinism, and safe executor handoff.
   - Apply the **Intent → Action → Outcome** pattern to every atomic step:
     - *Intent:* why this step exists.
     - *Action:* what exact operation is performed (`CREATE`, `MODIFY`, or `DELETE`).
     - *Outcome:* the bounded, testable post-state.

6. **Apply task-group completion tracking**
   - Organize `<atomic_steps>` into logical named groups using `####` headers.
   - Prefix every step bullet with an unchecked tracker: `- [ ]`.
   - The executor updates completed steps to `- [X]` during execution.
   - Groups must reflect genuine phase or responsibility boundaries, not ceremonial subdivision.
   - The 1:1 mapping between `<atomic_steps>` items and `<verification>` items must be preserved regardless of grouping.

7. **Apply internal step validation before emission**
   - Before finalizing each step, validate that it has:
     - Grounded target files, artifacts, or system surfaces.
     - A concrete, bounded action.
     - A clear dependency order when needed.
     - Side effects contained to in-scope surfaces.
     - A viable verification path.
   - Apply this validation internally. Do not expose the validation rubric in the artifact.

8. **Attach the verification contract**
   - One verification item per atomic step, numbered identically.
   - Each item must prove the intended post-state, not merely that activity occurred.
   - Use the lightest sufficient verification method:
     - command-based validation
     - static or structural inspection
     - type checking
     - test assertions
     - semantic validation
     - precise manual inspection (when command-based is unavailable)
   - Prefer existing project commands. Do not invent commands, tests, or success results.

9. **Handle review, rollback, and failure**
   - Apply the internal review policy (see below) to determine when human review gates affect execution sequencing.
   - Surface review gates only when they materially affect safety or sequencing.
   - Capture rollback and containment guidance in `<risks_and_mitigations>` when risk justifies it.
   - Plans must assume halt-on-failed-verification behavior for all dependent work.

## Required artifact structure

Emit sections in this exact order:

1. YAML frontmatter
2. `<objective>`
3. `<phases>`
4. `<atomic_steps>` (with task-group headers and `[ ]` completion trackers)
5. `<verification>`
6. `<risks_and_mitigations>` (optional; recommended for non-trivial or high-risk work)

## Frontmatter (required)

```yaml
---
task: "<one-sentence measurable objective>"
model: "gemini-3.1-pro-preview"
version: "1.0.0"
output_path: ".agent/plans/<filename>"
processed_path: ".agent/plans/processed/<filename>"
---
```

> `output_path` and `processed_path` must be populated with the fully resolved filename following the naming convention defined in **File naming and storage** above.

## Objective rules

- State exactly one measurable implementation objective.
- Precise enough that approval or rejection is unambiguous.
- Do not embed secondary work inside broad wording.

## Phase rules

- Use phases to express major execution boundaries, approval boundaries, or dependency boundaries.
- Provide clear `entry_criteria` and `exit_criteria` for each phase.
- Avoid ceremonial over-phasing. Prefer a small number of phases with meaningful orchestration value.
- Assign `gemini-3.1-pro-preview` to architecture and high-complexity phases; assign `gemini-3-flash` to high-volume implementation phases.

## Atomic step rules — Intent → Action → Outcome

- Each step represents a single bounded responsibility.
- State `CREATE`, `MODIFY`, or `DELETE` explicitly when omission risks ambiguity.
- Identify the target file(s), artifact(s), or system surface for every step.
- Prefer repeat-safe wording where feasible.
- Do not combine unrelated edits in a single step.
- Do not include speculative alternatives unless explicitly requested.
- High-risk or destructive actions must be explicit, narrowly scoped, and paired with a mitigation in `<risks_and_mitigations>`.

**Task-group format:**

```markdown
#### Group N — [Descriptive Group Name]

- [ ] N. <Step description using Intent → Action → Outcome pattern.>
- [ ] N+1. <Step description.>
```

## Verification rules

- Number verification items identically to their corresponding atomic step.
- Prove the intended result, not merely that activity occurred.
- Do not invent commands, tests, or success results.
- Manual inspection is acceptable when command-based validation is unavailable and the inspection criterion is precise.

## Internal review policy

Apply this policy silently when composing each step:

| Risk level                   | Conditions                                                                                                                                                                | Behavior                                     |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------- |
| **Always Proceed** (low)     | Isolated internal logic; formatting-only changes; no schema, API, persistence, or cross-system contract impact                                                            | No gate required                             |
| **Agent Decides** (moderate) | Bounded refactors; reversible changes; limited blast radius                                                                                                               | Agent may proceed with documented assumption |
| **Request Review** (high)    | Schema or data migrations; dependency/version changes; public API changes; irreversible side effects; persistence, deployment, security, or cross-system contract changes | Explicit human review gate required          |

Do not downgrade high-risk work through wording.

## RFQ format (hard halt)

Emit this artifact and stop when blocking ambiguity is detected:

```markdown
## RFQ — Request for Clarification

**Triggered by**: <phase/step + blocking condition>

**Blocking items**:
- [ ] <specific missing, conflicting, unreadable, or under-specified item>

**Why this blocks deterministic planning**:
- <concise grounded explanation>

**Resolution required before**: implementation-plan generation

**Do not proceed** until all items above are resolved.
```

## Token-efficiency rules

- Prefer concise bullets over narrative prose when precision is preserved.
- Include only files, modules, and interfaces actually in scope.
- Do not repeat global constraints inside every phase or step unless repetition is safety-critical.
- Avoid decorative explanation, speculative branches, and filler preamble.

## Anti-hallucination rules

- Ground every technical decision in local file evidence or cited external documentation.
- Never invent files, APIs, symbols, commands, tests, migrations, paths, or outcomes.
- Never convert uncertainty into certainty through wording.
- Never claim verification succeeded inside the plan artifact.
- If the plan cannot ground the objective, scope, step sequence, or verification path: halt and emit RFQ.
- You are a strictly grounded planner. Rely only on facts directly present in local context or cited external references.

</how_to_use>

<constraints>

- Do not emit the final plan as generic chat markdown when artifact output is available.
- Do not introduce unsupported frontmatter keys or new top-level sections.
- Do not proceed past unresolved blocking ambiguity.
- Do not modify out-of-scope files in the generated plan.
- Do not assign low-risk treatment to schema, API, dependency, persistence, security, or migration work.
- Do not claim side-effect freedom unless the scope boundary is explicitly defined and preserved.
- Do not invent verification commands or execution results.
- Do not use `gemini-3-pro` or `gemini-3-pro-preview` (discontinued March 26, 2026). Use `gemini-3.1-pro-preview`.

</constraints>

<resources_reference>

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `.agent/skills/dev-create-skill/resources/output-patterns.md`
- `.agent/plans/` (active plan output directory)
- `.agent/plans/processed/` (post-execution archive directory)
- `AGENTS.md` (primary rules file, Antigravity v1.20.3+)
- `GEMINI.md` (fallback rules file)
- `.gemini/antigravity/brain/` (persistent decision memory)

</resources_reference>
