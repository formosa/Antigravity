# AGENTS.md

# DDR System v4.0 — Agent Behavioral Contract

# Scope: All modifications to .agent\assets\proposals\active\ddr_system_v4.0.yaml

# Issue scope: ISSUE-009 (ARE Confidence Score Scoring Profile)

## Project Identity

This repository contains the DDR System v4.0 Specification: `.agent\assets\proposals\active\`

The PRIMARY modification target is: `.agent\assets\proposals\active\ddr_system_v4.0.yaml`

The REFERENCE specification is: `.agent\assets\proposals\active\DDR System(Opus_v4).md`

The ACTIVE issue report is: `.agent\assets\proposals\active\DDR_v4_Issue-009.md`

`.agent\assets\proposals\active\ddr_system_v4.0.yaml` IS the DDR System specification represented

as its own DAG. Every field in this file carries normative weight.

No field may be renamed, relocated, or removed unless the issue

report explicitly authorizes it.

---

## Foundational Axioms (MUST NEVER BE VIOLATED)

You must never produce output that violates any of the following axioms.

Check every modification against each axiom before finalizing:

- AX-1 (Traceability): Every non-root node must cite ≥1 parent via a typed edge.

- AX-2 (Abstraction Ordering): Tiers above CL must contain no implementation refs.

- AX-3 (Determinism): Identical inputs produce unambiguous, mechanically verifiable outputs.

→ Any scoring rubric you define MUST enumerate discrete, verifiable input signals.

→ "Source evidence quality" is the defect — do NOT reproduce it.

- AX-4 (Universality): No domain-specific assumptions in any Core tier.

- AX-5 (Extensibility): Advanced capabilities delivered via Extensions only.

- AX-6 (Declarative Integrity): All inference is Extension-only. Core is strictly declarative.

- AX-7 (DAG Acyclicity): No citation chain may produce a cycle.

---

## Extension System Invariants (MUST NEVER BE VIOLATED)

- EXT-R1: Extensions must declare contract version compatible with DDR-Core-4.x.

- EXT-R2: Extensions must declare which Core tiers they read and annotate.

- EXT-R3: Annotations must be namespaced by Extension ID (e.g., ARE::confidence_score).

- EXT-R4: Extensions update the reconciliation manifest; annotation counts tracked.

- EXT-R5: Disabling an Extension leaves Core CLEAN/DIRTY status unchanged.

- EXT-R6: Extension-internal derived artifact graphs must maintain acyclicity.

- EXT-R7: Extension advisories do not mutate Core node status.

---

## ARE Extension Invariants (E5 — DO NOT BREAK)

- ARE-R1: All inferred nodes placed in the Extension Candidate Pool (§8.2).

Automatic promotion is PROHIBITED.

- ARE-R2 (DEFECTIVE — this is the target of ISSUE-009): Currently reads:

"Each candidate carries ARE::confidence_score (0.0–1.0) derived from source

evidence quality." This phrase is semantically opaque and must be REPLACED,

not supplemented, with a normative scoring profile reference.

- ARE-R3: Promotion into Core DAG requires INSERT with full atomic ruleset validation.

- ARE-R4: ARE must never autonomously create XPD or GPCL nodes.

- ARE-R5 (NEW — to be added): Every ARE deployment must declare a scoring_profile

in its Extension contract. The declared profile must be either a standard profile

(standard_v1, conservative_v1) or a custom profile that explicitly declares all

constituent fields (signals, weights, bands, minimum_surfacing_threshold).

---

## ISSUE-009 Resolution Strategy (Option B — MANDATORY)

You MUST implement Option B exclusively from .agent\assets\proposals\active\DDR_v4_Issue-009.md.

Option A is NOT to be implemented.

Option B requires the following changes to .agent\assets\proposals\active\ddr_system_v4.0.yaml:

CHANGE-1: Add a new top-level section `are_scoring_profiles` defining:

- standard_v1 profile (signals, weights, score_bands, minimum_surfacing_threshold: 0.35)

- conservative_v1 profile (stricter thresholds for regulated environments)

- custom profile schema (declaration requirements only; no default values)

CHANGE-2: Replace ARE-R2 statement to reference scoring_profile declaration

instead of the bare "source evidence quality" phrase.

CHANGE-3: Add ARE-R5 to the E5 extension_catalog entry requiring scoring_profile

declaration in the Extension contract.

CHANGE-4: Add `scoring_profile` field to the E5 entry in extension_catalog,

with default value: standard_v1.

CHANGE-5: Extend `candidate_pool.promotion_mechanism` in §8.2 to enforce the

declared profile's minimum_surfacing_threshold. Candidates below this threshold

must carry an explicit `override_flag: true` with a human-authored rationale

to be eligible for INSERT.

CHANGE-6: Update `compliance_checklist.extension_validation` in §11 to add:

"ARE scoring_profile is declared in the E5 contract and is either a standard

profile or a validated custom profile with all fields present."

---

## Hard Constraints (NEVER VIOLATE)

- Do NOT rename or relocate any existing YAML keys.

- Do NOT change any existing ARE rules (ARE-R1, ARE-R3, ARE-R4) — only ARE-R2

is to be replaced; ARE-R5 is to be added.

- Do NOT modify the `candidate_pool.candidate_status_value`,

`visibility_rule`, `effect_on_core_status`, or `discard_trigger` fields.

- Do NOT introduce new edge types.

- Do NOT modify any Core node IDs.

- Do NOT auto-commit. Every stage requires explicit human review before proceeding.

- Do NOT invent YAML keys that do not appear in the existing schema pattern.

Follow the existing EXT-Rn rule list pattern for ARE-R5.

- Do NOT write explanatory prose inside YAML values unless the existing file

uses the YAML block scalar (`>`) pattern for that field. Follow the existing

formatting convention precisely.

- All new YAML identifiers must use snake_case.

- All score_band labels must use snake_case.

- The `minimum_surfacing_threshold` for standard_v1 must be 0.35.

---

## Permissions

### Allowed without approval

- Read any file in the repository.

- Write to `.agent\assets\proposals\active\ddr_system_v4.0.yaml` on the `issue-009-are-scoring-profile` branch only.

- Write to `AGENTS.md` on the `issue-009-are-scoring-profile` branch only.

- YAML lint validation (e.g., `yamllint .agent\assets\proposals\active\ddr_system_v4.0.yaml` if available).

### Require explicit human approval before proceeding

- Any git commit.

- Any git push.

- Any modification to `.agent\assets\proposals\active\DDR System(Opus_v4).md`.

- Any modification outside `.agent\assets\proposals\active\ddr_system_v4.0.yaml` and `AGENTS.md`.

- Proceeding past any stage where a validation check reports a failure.

---

## Output Format Requirements

- When producing YAML modifications, output a FULL diff (unified diff format).

- Do NOT produce explanations mixed inline with diff output.

- Separate explanation prose from YAML diff output into clearly labeled sections.

- Label each section of output: ANALYSIS, YAML_DIFF, VALIDATION_RESULT,

REGRESSION_RESULT.
