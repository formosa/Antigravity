# AGENTS.md

## Mission

Refine and enhance the **DDR System design framework itself** as a normative specification artifact.
Do **not** apply DDR as a process framework to this repository unless a task explicitly asks for that.
Treat this work as **framework architecture and specification engineering**, not ordinary feature delivery.

## Authority Order

1. `.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` is the normative specification.
2. `.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` is the normative schema and structural validator.
3. If any instruction, proposal, patch, note, or comment conflicts with those files, preserve the normative files and report the conflict explicitly.

## Primary Objective

Improve the DDR framework while preserving or increasing:

- logical consistency
- architectural stability
- determinism
- auditability
- traceability
- schema coherence
- validation clarity

## Optimization Priorities

Prefer changes that:

- reduce hallucination surface area
- improve instruction-following reliability
- improve code/spec quality
- eliminate dead rules, dead branches, dead concepts, and redundant structure
- avoid premature optimization
- avoid unnecessary logical complexity
- preserve explicit semantics over implicit inference
- minimize churn outside the smallest correct patch set

## Non-Goals

Do not:

- treat the framework as if it were a project instance
- invent new tiers, operations, edge types, lifecycle states, or extension behavior without a demonstrated gap
- add complexity to anticipate hypothetical future needs
- weaken normative language to avoid making a hard decision
- replace explicit rules with vague guidance
- move advanced analysis into Core when it belongs in Extensions

## Working Method

For any non-trivial change:

1. Identify the exact problem.
2. Locate the authoritative sections affected.
3. Trace cross-impacts across schema, invariants, operations, lifecycle, citations, tiers, and extensions.
4. Prefer the smallest change that fully resolves the issue.
5. Preserve backward compatibility unless incompatibility is necessary and justified.
6. Remove superseded or redundant text created by the change.
7. Verify the resulting model remains internally coherent.

## Required Review Lens

Always check for:

- contradictions between prose, schema, and lifecycle
- duplicate concepts with different names
- hidden pass-through tiers or rules with no independent semantic value
- ambiguous normative wording
- unverifiable requirements posing as structural rules
- semantic rules that should be structural, and structural claims that are actually semantic
- topology changes that break invariants, citation rules, or deterministic validation
- extension/Core boundary violations
- versioning or supersession behavior that can leave partial or unclear state

## Decision Heuristics

Choose the option that best satisfies this order:

1. correctness
2. determinism
3. simplicity
4. explicitness
5. backward-compatible stability
6. authoring usability

When two options are both correct, prefer the one with:

- fewer concepts
- fewer special cases
- fewer cross-tier exceptions
- clearer validation behavior
- lower maintenance burden

## Output Contract

When proposing a change, provide:

- the issue
- root cause
- affected sections
- recommended resolution
- why it is superior to alternatives
- patch-ready replacement text when editing is requested
- explicit note of any tradeoff or compatibility impact

## Completion Criteria

A change is not complete unless it:

- resolves the target issue end-to-end
- introduces no new contradiction or orphaned rule
- remains aligned across `ddr_system_v6.1.yaml` and `ddr_node_schema.yaml`
- preserves the distinction between **system-definition** and **project-instance** semantics
- removes obsolete text made unnecessary by the change
- keeps the framework at least as simple as before, unless added complexity is strictly necessary

## Escalation Rule

If the best fix would require changing normative behavior across multiple sections, do not patch locally in one place only.
Propagate the change through every affected authority surface: specification, schema, lifecycle, operations, invariants, citations, and extension boundaries.
