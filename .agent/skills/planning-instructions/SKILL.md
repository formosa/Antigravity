---
name: planning-instructions
description: Generates a deterministic, hallucination-resistant Implementation Plan Artifact for zero-ambiguity execution within Google Antigravity IDE v1.16.5.
---

# SKILL: IMPLEMENTATION PLANNING (v3.0)

> **Model context (as of 2026-02-19)**
> — **Planning agent**: Gemini 3.1 Pro (Plan Mode, `thinking_level: high`)
> — **Execution agent**: Gemini 3 Flash (Fast Mode, `thinking_level: low` per step; `high` for
> pre/post-condition evaluation)
> — **IDE**: Google Antigravity v1.16.5 (Strict Mode available; formerly "Secure Mode" — renamed
> in this release)
> — **Grounding principle**: All factual assertions must trace to local context or cited external
> research. If a required input is missing or ambiguous, output an RFQ and halt — do not infer,
> assume, or hallucinate missing details.

---

## Gemini 3 Prompting Principles Applied in This Skill

The following model-specific behaviors govern how this skill authors its output artifact.
Gemini 3.1 Pro rewards concise, direct directives placed **after** context blocks. Over-engineering
with repeated constraints, exhaustive step lists for obvious work, or verbose format instructions
degrades output quality relative to Gemini 2.x behavior.

| Principle                            | Application in This Skill                                             |
| :----------------------------------- | :-------------------------------------------------------------------- |
| Instruction-after-context placement  | Directives appear at the end of each section block                    |
| Explicit abstention mandate          | Every phase includes a "if unknown, halt" instruction                 |
| Single-pass structured output        | TASK / CONTEXT / OUTPUT schema used throughout §2                     |
| Grounding anchor                     | Phase 2 mandates citation ≤ 3 months old for all external decisions   |
| Temperature: default                 | No temperature override; Gemini 3 reasoning degrades under adjustment |
| `thinking_level: high` for planning  | Applied during Phase 1–4 artifact authoring                           |
| Concise constraints                  | Rules stated once; not repeated per step                              |

---

## PHASE 1 — OMNISCIENCE GUARD, GROUNDING & ENTROPY AUDIT

### 1.1 — Load Context

> Notify the user, "(1.1 — Load Context):  I am studying the project in preparation for planning."

Read the target task definition and every explicitly referenced design document.
Sync with Antigravity's persistent Knowledge / Decision Records at
`.gemini/antigravity/brain/` (or the project-equivalent path). Prior decision
records **OVERRIDE** all defaults. Confirm directory existence with a file-system
read — do not assume absence.

### 1.2 — Entropy Audit

> Notify the user, "(1.2 — Entropy Audit):  I am now auditing the project to ensure a clean foundation for the new implementation."

Before drafting any plan, audit the affected scope for existing technical debt that
would undermine the new implementation if left unaddressed.

Scan for and record:

- Unused imports and dead code within files in scope.
- Deprecated API patterns or library calls relevant to the task domain.
- Schema drift between the codebase and declared contracts (type hints, OpenAPI
  specs, lock file versions).
- Redundant logic that duplicates functionality already available in the project.

Report findings in `§1 Overview — Entropy Status`. Propose targeted cleanup only
when it directly aligns with task intent. Do not expand scope.

### 1.3 — Contextual Purity

> Notify the user, "(1.3 — Contextual Purity):  I am now focusing in on the relevant details for this plan..."

Retain only: target source code, current environment constraints (runtime versions,
`requirements.txt`, `package.json`, lock files), and immediate task parameters.
Discard irrelevant conversation history to maximize signal-to-noise.

**Grounding anchor (anti-hallucination):** All subsequent reasoning must reference
either a verified local file read or a cited external source. If a fact cannot be
traced to either, treat it as unknown and apply the RFQ rule below.

### 1.4 — Explicit Abstention (RFQ — Hard Halt)

> Notify the user, "(1.4 — Explicit Abstention): I am now determining if I require any addition details necessary for designing an accurate and precise Implementation Plan."

If **any** of the following conditions are met, output an **RFQ Artifact** and
**halt immediately**. Do not proceed to Phase 2. Do not guess or fill gaps.

RFQ trigger conditions:

- A required file, dependency version, or schema is missing or unreadable.
- An architectural constraint is ambiguous or contradicts the Knowledge Base.
- The task scope boundary cannot be unambiguously determined from available context.
- Phase 2 research returns conflicting authoritative results with no clear resolution.

**RFQ Artifact format:**

```markdown
## RFQ — Request for Clarification

**Triggered by**: [Phase and specific condition that caused halt]

**Blocking items**:
- [ ] [Exact missing or ambiguous item #1 — be specific]
- [ ] [Exact missing or ambiguous item #N]

**Resolution required before**: Phase 2 / Build Manifest generation

**Do not proceed** until all items above are resolved and confirmed.
```

---

## PHASE 2 — RESEARCH & DESIGN VALIDATION

### 2.1 — Targeted Search

> Notify the user, "(2.1 — Targeted Search): I am now conducting research to ensure the best and most up-to-date approach for this Implementation Plan."

Execute web searches for every framework, library, or API required by the task.

**Research freshness constraint**: Only cite sources published within the **last
3 months** (relative to today's date). Gemini models and the Antigravity platform
evolve rapidly; older sources may describe deprecated APIs or superseded behavior.
If no source within the freshness window is found, this is an RFQ-triggering condition.

### 2.2 — Validation

> Notify the user, "(2.2 — Validation): I am now validating the research to ensure it is accurate and up-to-date."

Confirm that intended syntax, endpoints, and design patterns align with authoritative
documentation within the freshness window. Cross-reference against local project
context (version pins, lock files) to detect drift between upstream docs and pinned
versions.

### 2.3 — Grounding

> Notify the user, "(2.3 — Grounding): I am now grounding the Implementation Plan in the project's current context and research."

Every technical decision in the Build Manifest must be directly traceable to either:

- **Local project context** (file read, schema inspection, lock file), or
- **Validated external research** (cited source URL + publication date ≤ 3 months old).

No decision may rest on untraceable assumptions. If a decision cannot be grounded,
state "I do not have sufficient information to make this decision" and issue an RFQ.

---

## PHASE 3 — NATIVE REVIEW POLICY BINDING

> Notify the user, "(3.1 — Native Review Policy Binding): I am now assigning Review Policies to each step to ensure the highest quality and accuracy."

Assign Antigravity's native Review Policies to each atomic step using the risk matrix
below. Rely on the user's existing IDE settings for Terminal and Strict Mode
enforcement. Do not attempt to manage these system-level policies.

> **v1.16.5 note**: "Secure Mode" was renamed **Strict Mode** in Antigravity v1.16.5
> (2026-02-03). All references to Secure Mode in prior skill versions or project
> documentation should be read as Strict Mode.

| Review Policy      | Risk Level | Qualifying Conditions                                                                                                                                                 |
| :----------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Always Proceed** | LOW        | Isolated function-local logic; standard library only; no disk/network I/O; no schema change.                                                                          |
| **Agent Decides**  | MODERATE   | Standard refactoring; internal module restructuring; read-only I/O. Proceed only if internal confidence is absolute; otherwise escalate to Request Review.            |
| **Request Review** | HIGH       | Schema changes; external dependency additions or version bumps; non-sandboxed disk/network I/O; public API or contract modifications; any irreversible state change.  |

For every **HIGH** risk item: a rollback procedure is **mandatory** (see `§5 — Rollback
Procedures`). The executing agent MUST surface the rollback block and obtain explicit
written approval before proceeding.

---

## PHASE 4 — OUTPUT: IMPLEMENTATION PLAN ARTIFACT

> Notify the user, "(4.1 — Output: Implementation Plan Artifact): I am now generating the Implementation Plan based on the research and validation I have conducted."

Output the Implementation Plan as an **Antigravity Artifact** conforming to the
`ImplementationPlanDefinition` schema defined in
`.agent/assets/schemas/implementation-plan/implementation-plan.d.ts`.

**Critical**: The artifact MUST be created using the `write_to_file` tool with
`IsArtifact: true` and `ArtifactType: "implementation_plan"`. Do NOT output the
plan as inline markdown in the conversation. The plan is a standalone artifact file.

Omit all conversational filler. Gemini 3.1 Pro is the authoring agent; Gemini 3 Flash
is the executing agent. Reference
`.agent/assets/schemas/implementation-plan/example.md` for the canonical output template.

---

### 4.1 — YAML Frontmatter (Required)

The artifact file MUST begin with valid YAML frontmatter containing exactly these keys:

```yaml
---
task: "[One-sentence target objective with measurable success condition]"
model: "gemini-3.1-pro"
---
```

---

### 4.2 — Body Content (Required XML Isolation Blocks)

All body content MUST use the following XML isolation blocks, in order. Each block
anchors the model's attention mechanism to verifiable, structured output.

---

#### `<objective>` (Required)

One-paragraph summary consolidating:

- The target objective and measurable success condition.
- Design justification summarizing technical decisions from Phase 2 (include source
  URLs and publication dates). Justify why this is the maximally optimized solution,
  not merely the most expedient.
- Scope: exhaustive list of files and modules affected.
- Out of Scope: exhaustive list of files and modules that MUST NOT be touched.
- Entropy Status from Phase 1.2 (`CLEAN` or findings formatted as
  `file:line — issue description`).
- Knowledge Base Alignment (`NONE` or list of prior Decision Records consulted and
  any conflicts resolved).

> **If Context State = RFQ Triggered**, halt generation here. Output the RFQ Artifact
> from Phase 1.4 instead. Do not generate the remaining blocks.

---

#### `<phases>` (Required for multi-phase plans; omit for single-phase work)

Each phase entry MUST include:

- `phase_id`: Unique identifier (e.g., `PHASE_1_SCAFFOLD`).
- `objectives`: Array of objectives for this phase.
- `task_references`: Array of related task IDs.
- `entry_criteria`: Array of conditions that must be true before this phase begins.
- `exit_criteria`: Array of conditions that must be true for this phase to be complete.
- `assigned_model`: `"gemini-3.1-pro"` or `"gemini-3-flash"` per the risk matrix in
  Phase 3.

---

#### `<atomic_steps>` (Required)

Numbered list of deterministic, single-responsibility execution steps. Execute steps
in numbered order unless a step is explicitly marked `[PARALLEL-SAFE]`.

> **`[PARALLEL-SAFE]` definition**: A step has no read/write dependency on any other
> step and may be executed concurrently with other `[PARALLEL-SAFE]` steps. Steps
> without this marker are strictly sequential. When in doubt, treat as sequential.

Each step MUST encode:

1. **Target File**: `[relative/path/to/file.ext]`
2. **Component**: `[Exact Class / Function / Module name and full type-annotated signature]`
3. **Operation**: `CREATE | MODIFY | DELETE`
4. **Review Policy**: `Always Proceed | Agent Decides | Request Review`
   (from Phase 3 risk matrix)
5. **PRE-Condition**: `[Exact verifiable assertion that MUST be true before acting.]`
6. **Logic Definition**: Deterministic, step-by-step logic referencing exact existing
   variable and function names. No pronouns. No inference. Every branch and edge case
   explicitly handled. If a required detail is unknown, insert:
   `UNKNOWN — RFQ required`.
7. **PROHIBIT**: `[What MUST NOT happen during this step.]`
8. **POST-Condition**: `[Exact verifiable assertion that MUST be true after acting.]`
9. **DEPENDS**: `[N/A | Step #X]`

---

#### `<verification>` (Required)

Numbered list mapping 1:1 to each atomic step. Each entry specifies:

- The specific terminal command, pytest invocation, or IDE validation step to confirm
  correctness before advancing to the next step.
- For `Request Review` steps: the exact rollback procedure (`git restore` commands)
  that the executing agent MUST surface and obtain explicit written approval for
  before proceeding.

> **Required for every HIGH risk step.** If the plan contains zero HIGH risk items,
> state that explicitly.

---

#### `<risks_and_mitigations>` (Optional)

Potential failure points and mitigation strategies. Include the Justification &
Research Citations table:

| Decision                             | Rationale (why chosen over alternatives) | Citation (URL + date, ≤ 3 months old) |
| :----------------------------------- | :--------------------------------------- | :------------------------------------ |
| \[Non-obvious architectural choice\] | \[Explicit justification\]               | \[URL — YYYY-MM-DD\]                  |

> If a decision cannot be cited within the freshness window, treat it as an
> RFQ-triggering gap.

---

### 4.3 — Post-Artifact Directives

These directives are NOT part of the artifact body. They are operational instructions
bound to the executing agent after the artifact has been approved by the user.

---

#### Post-Execution Knowledge Base Update

Upon **full verification success** (all POST-conditions met, all verification checks
passing), the executing agent MUST write or update the Antigravity persistent Decision
Record at `.gemini/antigravity/brain/<TASK_NAME>.md`.

If the file already exists, append a new dated entry below existing content.
Do not overwrite prior records.

```markdown
# Decision Record: [TASK_NAME]

**Date**: [ISO 8601 — YYYY-MM-DDThh:mm:ssZ]
**Implemented by**: Gemini 3 Flash (Fast Mode, thinking_level: low) via
  Implementation Planning Skill v3.0
**Planned by**: Gemini 3.1 Pro (Plan Mode, thinking_level: high) via
  Implementation Planning Skill v3.0
**Objective**: [One-sentence restatement of goal]

## Decision Summary

[What was implemented and why — include the maximal optimization rationale and the
alternatives that were considered and rejected.]

## Constraints Established

[Any new rules, patterns, or prohibitions that future planning or executing agents
MUST respect in this project.]

## Files Modified

- [relative/path/to/file.ext — operation performed]

## Research Citations Used

- [title — URL — publication date — summary of relevant content]

## Verification Artifacts

- [Test output summary | Antigravity diff link | Screenshot reference]

## Rollback Reference

- [Git commit hash at pre-execution state]
```

---

#### Execution Contract

> This section is addressed directly to the **executing agent** (Gemini 3 Flash,
> Fast Mode). Read it in full before acting on any directive in `<atomic_steps>`.

You are the **executing** agent. You did not author this plan.

**You WILL**:

- Confirm every PRE-Condition before acting on a step, using `thinking_level: high`
  for condition evaluation even when operating in Fast Mode.
- Confirm every POST-Condition after acting on a step.
- Run the mapped `<verification>` check before advancing to the next step.
- Halt immediately and notify the user on any failed PRE-Condition, POST-Condition,
  or scope boundary violation.
- Execute the rollback procedure for any `Request Review` step that fails its
  POST-Condition, before notifying the user.
- Write the Knowledge Base Decision Record upon successful completion.

**You WILL NOT**:

- Touch any file listed in the objective's "Out of Scope."
- Interpret, infer, or add anything not explicitly stated in `<atomic_steps>`.
- Proceed past any `Request Review` step without explicit written user approval.
- Fill in gaps or make assumptions when a PRE-Condition or logic detail is marked
  `UNKNOWN — RFQ required`. Halt and surface the gap to the user instead.
- Override the Review Policy classification assigned to any step.

**Anti-hallucination directive**: You operate under strict grounding. If a step's
Logic Definition references a variable, function, or file that does not exist in the
codebase as stated in the PRE-Condition, you MUST halt and report the discrepancy.
You MUST NOT invent plausible-looking implementations to fill the gap.
