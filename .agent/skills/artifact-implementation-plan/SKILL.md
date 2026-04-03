---
name: artifact-implementation-plan
version: 6.0.0
description: Serves as the Artifact-Centric Owner for Antigravity implementation-plan artifacts by creating, refining, auditing, and lifecycle-managing schema-compatible plans optimized for grounded planning, patch-bounded execution batches, task-tracker visibility, and safe executor handoff. Use when the task needs a formal plan artifact before execution begins. Do not use when the requested work is trivial enough to execute directly without a governed plan.
---

<when_to_use>

- The user requests an implementation plan before coding begins.
- The user asks to create, edit, refine, regenerate, enhance, or audit an existing implementation plan artifact.
- The task has non-trivial scope, dependencies, or risk requiring deterministic execution steps.
- A human-approved planning artifact is required before any code or file modifications occur.
- Do not use this skill for trivial one-file changes that can be executed safely without a standalone plan artifact.
- Example prompt: "Draft an implementation plan for refactoring the schema validation pipeline before coding begins."
- Example prompt: "Regenerate this implementation plan artifact to reflect the new governance requirements."

</when_to_use>

<how_to_use>

## Operating mode

- **Planner model:** `gemini-3.1-pro-preview` (high reasoning).
- **Executor model target:** `gemini-3-flash` (high-volume, low-latency implementation steps).
- **IDE target:** Antigravity v1.20.3+.
- **Rules file:** `AGENTS.md` (primary, v1.20.3+); `GEMINI.md` (fallback if `AGENTS.md` absent).
- **Auto-continue:** Enabled by default in v1.20.3+. Plans must be structured to tolerate uninterrupted executor handoff.
- **Owner subtype:** `Artifact-Centric Owner` for the implementation-plan artifact family.

## Contract preservation rules

Preserve compatibility with:

- `.agent/schemas/implementation-plan/implementation-plan.d.ts`
- `.agent/schemas/implementation-plan/example.md`
- `resources/schema/implementation-plan/implementation-plan.d.ts` (read-only vendored mirror for packaging/reference)
- `resources/schema/implementation-plan/example.md` (read-only vendored mirror for packaging/reference)
- `.agent/skills/asset-skill/resources/output-patterns.md`
- the active `artifact-implementation-plan` skill instructions

Historical artifacts under `.agent/plans/processed/` may inform review, but they are not a normative compatibility surface for newly generated plans under this skill version.

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
     - **Blocking ambiguity** -> emit RFQ artifact and halt.
     - **Non-blocking uncertainty** -> capture as a concise assumption, dependency note, or risk note inside the plan.
   - Never infer hidden requirements. Never convert uncertainty into certainty through wording.

4. **Perform focused validation research (only when required)**
   - Use external docs only for API or framework behavior not derivable from local files.
   - Prefer official vendor docs, changelogs, and primary references.
   - If evidence conflicts and cannot be resolved, emit RFQ and halt.
   - Never let external research override explicit local project requirements without calling out the conflict.

5. **Generate the execution plan artifact**
   - Create a standalone Antigravity artifact; do not emit inline conversational markdown.
   - Use `<phases>` by default for non-trivial work.
   - Use the fewest phases only when they provide real orchestration value.
   - Optimize for executor patchability, not minimum step count.
   - Use the smallest atomic steps that remain reviewable, bounded, and locally verifiable.
   - Prefer one primary write surface per atomic step by default.
   - Split a candidate step before plan emission when it spans multiple major surfaces such as canonical schema, owner skill package, downstream consumer migration, routing or index wiring, or documentation, unless incremental verification is impossible and the reason is explicit in the step wording.
   - Apply the **Intent -> Action -> Outcome** pattern to every atomic step:
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
      - A concrete, bounded action executable as one edit batch.
      - A clear dependency order when needed.
      - Side effects contained to in-scope surfaces.
      - A viable local verification path.
      - No hidden coupling to a second major write surface unless the step explicitly justifies why incremental verification is impossible.
   - Apply this validation internally. Do not expose the validation rubric in the artifact.

8. **Attach the verification contract**
   - One verification item per atomic step, numbered identically.
   - Each item must prove the intended post-state, not merely that activity occurred.
   - Treat verification as the stop/go boundary between edit batches; dependent batches must not proceed until the current batch verifies.
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
   - Prevent oversized or cross-surface edit batches through narrower planning scope rather than bundling broad changes into one step.
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

## Atomic step rules -> Intent -> Action -> Outcome

- Each step represents a single bounded responsibility.
- Each step must be executable as a single bounded edit batch with a local verification path.
- State `CREATE`, `MODIFY`, or `DELETE` explicitly when omission risks ambiguity.
- Identify the target file(s), artifact(s), or system surface for every step.
- Prefer repeat-safe wording where feasible.
- Do not combine unrelated edits in a single step.
- Do not combine canonical schema edits, owner-package edits, routing or index rewires, and documentation updates in one atomic step unless incremental verification is impossible and the reason is explicit.
- Do not include speculative alternatives unless explicitly requested.
- High-risk or destructive actions must be explicit, narrowly scoped, and paired with a mitigation in `<risks_and_mitigations>`.

**Task-group format:**

```markdown
#### Group N — [Descriptive Group Name]

- [ ] N. <Step description using Intent -> Action -> Outcome pattern.>
- [ ] N+1. <Step description.>
```

## Verification rules

- Number verification items identically to their corresponding atomic step.
- Verification is the stop/go boundary between atomic edit batches; preserve the 1:1 mapping with `<atomic_steps>` even when groups change.
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
- Do not use processed historical implementation plans to justify legacy frontmatter omissions, section order changes, or tracker omissions in newly generated plans.
- Do not use `gemini-3-pro` or `gemini-3-pro-preview` (discontinued March 26, 2026). Use `gemini-3.1-pro-preview`.

</constraints>

<resources_reference>

- Read `.agent/schemas/implementation-plan/implementation-plan.d.ts` to verify the active canonical implementation-plan contract.
- Read `.agent/schemas/implementation-plan/example.md` to mirror the canonical artifact structure and section ordering.
- Read `resources/schema/implementation-plan/implementation-plan.d.ts` and `resources/schema/implementation-plan/example.md` only as read-only vendored mirrors for packaging/reference after consulting the canonical schema.
- Read `.agent/skills/asset-skill/resources/output-patterns.md` to preserve local output and artifact handoff conventions.
- Read `.agent/plans/` to inspect active plan outputs and avoid naming or placement conflicts.
- Read `.agent/plans/processed/` as historical reference only when prior plans materially inform the new artifact.
- Read `.gemini/antigravity/brain/` as persistent decision memory when that context materially affects the plan.

</resources_reference>
