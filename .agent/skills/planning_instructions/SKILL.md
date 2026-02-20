---
type: skill
name: "Implementation Planning (v3.0 - Native Antigravity 1.16.5 / Gemini 3.1 Pro)"
activation: auto
triggers:
  - "@Implementation_Plan"
priority: 100
severity: mandatory
description: >
  Generates a deterministic, hallucination-resistant Implementation Plan Artifact for
  zero-ambiguity execution within Google Antigravity IDE v1.16.5, optimized for the
  Gemini 3.1 Pro planning agent and Gemini 3 Flash execution agent. Applies
  instruction-after-context placement, explicit-abstention grounding, and minimal
  prompt scaffolding per Google's official Gemini 3 prompt design guidance (2026-02-12).
  Integrates native Antigravity Review Policy binding (Strict Mode), high-risk rollback
  procedures, and mandatory post-execution Knowledge Base persistence to ensure rigorous,
  project-agnostic, self-improving execution.
research_citations:
  - "Google Gemini 3.1 Pro announcement — blog.google — 2026-02-19"
  - "Gemini 3.1 Pro Model Card — deepmind.google — 2026-02-19"
  - "Google Antigravity v1.16.5 changelog (Strict Mode rename) — changelogs.directory — 2026-02-03"
  - "Antigravity launch announcement & Artifact transparency model — developers.googleblog.com — 2025-11-20"
  - "Prompt design strategies (Gemini API official docs) — ai.google.dev — 2026-02-12"
  - "Gemini 3 Prompting Playbook — promptbuilder.cc — 2025-11-15"
  - "Reduce Gemini 3 hallucinations via grounding and abstention — zilliz.com — 2025-01-13"
  - "Gemini 3 Flash thinking_level parameter — docs.cloud.google.com — 2026-02-19"
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

Read the target task definition and every explicitly referenced design document.
Sync with Antigravity's persistent Knowledge / Decision Records at
`.gemini/antigravity/brain/` (or the project-equivalent path). Prior decision
records **OVERRIDE** all defaults. Confirm directory existence with a file-system
read — do not assume absence.

### 1.2 — Entropy Audit

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

Retain only: target source code, current environment constraints (runtime versions,
`requirements.txt`, `package.json`, lock files), and immediate task parameters.
Discard irrelevant conversation history to maximize signal-to-noise.

**Grounding anchor (anti-hallucination):** All subsequent reasoning must reference
either a verified local file read or a cited external source. If a fact cannot be
traced to either, treat it as unknown and apply the RFQ rule below.

### 1.4 — Explicit Abstention (RFQ — Hard Halt)

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

Execute web searches for every framework, library, or API required by the task.

**Research freshness constraint**: Only cite sources published within the **last
3 months** (relative to today's date). Gemini models and the Antigravity platform
evolve rapidly; older sources may describe deprecated APIs or superseded behavior.
If no source within the freshness window is found, this is an RFQ-triggering condition.

### 2.2 — Validation

Confirm that intended syntax, endpoints, and design patterns align with authoritative
documentation within the freshness window. Cross-reference against local project
context (version pins, lock files) to detect drift between upstream docs and pinned
versions.

### 2.3 — Grounding

Every technical decision in the Build Manifest must be directly traceable to either:

- **Local project context** (file read, schema inspection, lock file), or
- **Validated external research** (cited source URL + publication date ≤ 3 months old).

No decision may rest on untraceable assumptions. If a decision cannot be grounded,
state "I do not have sufficient information to make this decision" and issue an RFQ.

---

## PHASE 3 — NATIVE REVIEW POLICY BINDING

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

Output strictly using the schema below. Omit all conversational filler. Gemini 3.1 Pro
is the authoring agent; Gemini 3 Flash is the executing agent. Each section is addressed
to the appropriate agent.

Sections `§1–§7` are canonical and **must all appear, in order**, in every generated plan.

---

### §1 — Overview

- **Target Objective**: One-sentence goal. Include a measurable success condition.
- **Design Justification**: Summary of technical decisions from Phase 2. Include source
  URLs and publication dates. Justify why this is the maximally optimized solution, not
  merely the most expedient.
- **Scope**: Exhaustive list of files and modules affected.
- **Out of Scope**: Exhaustive list of files and modules that MUST NOT be touched.
- **Entropy Status**: `CLEAN` or findings formatted as `file:line — issue description`,
  with proposed cleanup steps where applicable.
- **Knowledge Base Alignment**: `NONE` or list of prior Decision Records consulted and
  any conflicts resolved.
- **Context State**: `Verified` or `RFQ Triggered: [list of missing or ambiguous items]`

> **If Context State = RFQ Triggered**, halt generation here. Output the RFQ Artifact
> from Phase 1.4. Do not generate §2 or beyond.

---

### §2 — Build Manifest

Execute task groups in the order listed. Within a group, execute steps in numbered order
unless a step is explicitly marked `[PARALLEL-SAFE]`.

> **`[PARALLEL-SAFE]` definition**: A step has no read/write dependency on any other
> step in the same group and may be executed concurrently with other `[PARALLEL-SAFE]`
> steps. Steps without this marker are strictly sequential. When in doubt, treat a step
> as sequential.

---

**Task Group**: `[Logical Group Name]`
**Target File**: `[relative/path/to/file.ext]`

1. **Component**: `[Exact Class / Function / Module name and full type-annotated signature]`
2. **Operation**: `CREATE | MODIFY | DELETE`
3. **Review Policy**: `Always Proceed | Agent Decides | Request Review`
4. **PRE-Condition**: `[Exact verifiable assertion that MUST be true before acting.
   Example: "src/auth/login.py exists and contains class AuthManager".]`
5. **Logic Definition**:

   ```plaintext
   [Deterministic, step-by-step logic referencing exact existing variable and function
   names from the codebase. No pronouns. No inference. Every branch and edge case
   explicitly handled. If a required detail is unknown, insert: UNKNOWN — RFQ required.]
   ```

6. **PROHIBIT**: `[What MUST NOT happen. Example: "Do NOT alter the constructor
   signature or error handling in AuthManager.__init__".]`
7. **POST-Condition**: `[Exact verifiable assertion that MUST be true after acting.
   Example: "Function accepts oauth_token: str; unit test test_oauth_flow passes".]`
8. **DEPENDS**: `[N/A | Step #X in Task Group Y]`
9. **Verification Gate**: `[Specific terminal command, pytest invocation, or IDE
   validation step to confirm correctness before advancing to the next step.]`

> Repeat task group blocks as necessary.

---

### §3 — Justification & Research Citations

| Decision                             | Rationale (why chosen over alternatives) | Citation (URL + publication date, ≤ 3 months old) |
|--------------------------------------|------------------------------------------|---------------------------------------------------|
| \[Non-obvious architectural choice\] | \[Explicit justification\]               | \[URL — YYYY-MM-DD\]                              |

> If a decision cannot be cited within the freshness window, it must not appear here.
> Treat uncitable decisions as RFQ-triggering gaps.

---

### §4 — Verification Strategy

#### Automated Tests

```bash
# Happy path
pytest -k "test_successful_<feature>" -v --tb=short

# Failure / edge-case path
pytest -k "test_invalid_<input_or_error>" -v --tb=short

# Full regression guard
pytest --tb=no -q
```

#### Manual / Artifact Checklist

- [ ] **VERIFY**: Observable outcome. Specify expected Antigravity Artifact
  (screenshot, diff, browser recording) if applicable.
- [ ] **REGRESSION**: Confirm unaffected functionality. Name the specific paths,
  endpoints, or behaviors that must remain unchanged.

---

### §5 — Rollback Procedures

> **Required for every HIGH risk step.** If the entire Build Manifest contains zero
> HIGH risk items, state that explicitly and omit the rollback blocks below.

For each HIGH risk step, provide a numbered, exact rollback sequence covering every
file modified by that step. One rollback block per HIGH risk step.

```bash
# Rollback: [Task Group Name — Step #N]
git restore --source=HEAD~1 relative/path/to/affected/file1.ext
git restore --source=HEAD~1 relative/path/to/affected/file2.ext
# [Additional commands if schema migration, dependency install, or DB state change occurred]
```

**High-Risk Human Intervention Gate**: Before executing any step classified
`Request Review`, the executing agent MUST pause, surface this rollback block to the
user, and wait for explicit written approval before proceeding.

---

### §6 — Post-Execution Knowledge Base Update

Upon **full verification success** (all POST-conditions met, all tests passing, all
manual checklist items confirmed), the executing agent MUST write or update the
Antigravity persistent Decision Record at `.gemini/antigravity/brain/<TASK_NAME>.md`.

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

- [URL — publication date]

## Verification Artifacts

- [Test output summary | Antigravity diff link | Screenshot reference]

## Rollback Reference

- [Git commit hash at pre-execution state]
```

---

### §7 — Execution Contract

> This section is addressed directly to the **executing agent** (Gemini 3 Flash,
> Fast Mode). Read it in full before acting on any directive in §2.

You are the **executing** agent. You did not author this plan.

**You WILL**:

- Confirm every PRE-Condition before acting on a step, using `thinking_level: high`
  for condition evaluation even when operating in Fast Mode.
- Confirm every POST-Condition after acting on a step.
- Run the Verification Gate before advancing to the next step.
- Halt immediately and notify the user on any failed PRE-Condition, POST-Condition,
  or scope boundary violation.
- Execute the §5 Rollback Procedure for any HIGH risk step that fails its
  POST-Condition, before notifying the user.
- Write the §6 Decision Record upon successful completion of the full Build Manifest.

**You WILL NOT**:

- Touch any file listed in §1 "Out of Scope."
- Interpret, infer, or add anything not explicitly stated in §2.
- Proceed past any `Request Review` step without explicit written user approval.
- Fill in gaps or make assumptions when a PRE-Condition or logic detail is marked
  `UNKNOWN — RFQ required`. Halt and surface the gap to the user instead.
- Override the Review Policy classification assigned to any step.

**Anti-hallucination directive**: You operate under strict grounding. If a step's
Logic Definition references a variable, function, or file that does not exist in the
codebase as stated in the PRE-Condition, you MUST halt and report the discrepancy.
You MUST NOT invent plausible-looking implementations to fill the gap.
