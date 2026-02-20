---
type: skill
name: "Implementation Planning (v2.0 - Native Antigravity 1.16.5)"
activation: auto
triggers:
  - "@Implementation_Plan"
priority: critical
severity: mandatory
description: "Generates a deterministic, hallucination-resistant Implementation Plan Artifact. Utilizes targeted internet research, explicit uncertainty handling (RFQ), and IDE-native Review Policies to ensure rigorous, project-agnostic execution."
---

# SKILL: IMPLEMENTATION PLANNING (v2.0)

## 1. PHASE ONE: OMNISCIENCE GUARD & GROUNDING (ANTI-HALLUCINATION)

1. **Load Context**: Read the target task definition and explicitly referenced design documents.
2. **Contextual Purity**: Drop irrelevant conversation history. Retain only the target source code, current environment constraints, and immediate task parameters to maximize the signal-to-noise ratio.
3. **Explicit Abstention (RFQ)**: If any critical dependency, file, parameter, or architectural constraint is missing, ambiguous, or unverifiable, you MUST output a Request for Clarification (RFQ) Artifact and halt. Do not guess, assume, or hallucinate details.

## 2. PHASE TWO: RESEARCH & DESIGN VALIDATION

1. **Targeted Search**: Execute web searches to research the specific frameworks, libraries, or APIs required by the task.
2. **Validation**: Validate that intended syntax, endpoints, and design patterns align with authoritative documentation published within the last 6 months.
3. **Grounding**: Ensure every technical decision in the Build Manifest is directly backed by either the local project context or your validated research.

## 3. PHASE THREE: NATIVE REVIEW POLICY BINDING

Assign Antigravity’s native Review Policies to each atomic step. Rely on the user's existing IDE settings for Terminal and Secure Mode enforcement; do not attempt to manage these system-level policies yourself.

* **Always Proceed**: LOW risk (e.g., isolated function-local logic, standard library usage).
* **Agent Decides**: MODERATE risk (e.g., standard refactoring). Proceed only if internal confidence is absolute.
* **Request Review**: HIGH risk (e.g., schema changes, external dependency additions, non-sandboxed disk/network I/O).

## 4. OUTPUT: IMPLEMENTATION PLAN ARTIFACT

Output strictly using the schema below. Omit all conversational filler.

### ARTIFACT: Implementation Plan

#### Overview

* **Target Objective**: [One-sentence goal + measurable success condition]
* **Design Justification**: [Brief summary of technical decisions based on Phase 2 Research, including source links]
* **Context State**: [Verified | RFQ Triggered: list of missing/ambiguous items]

> *(If Context State = RFQ Triggered, halt generation here. Do not guess the Build Manifest.)*

### Build Manifest

**Task Group**: `[Logical Group Name]`
**Target File**: `[filepath]`

1. **Component**: `[Exact Class/Function/Module signature]`
2. **Operation**: `CREATE | MODIFY | DELETE`
3. **Review Policy**: `Always Proceed | Agent Decides | Request Review`
4. **Logic Definition**: `[Deterministic, step-by-step logic. Explicit constraints. No pronouns.]`
5. **Verification Gate**: `[Specific terminal command, test, or IDE validation step to rigorously verify accuracy before proceeding to the next group]`

> *(Repeat blocks as necessary)*
