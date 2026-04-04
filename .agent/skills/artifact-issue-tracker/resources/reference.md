# Agent Update Issues Tracker Reference

## Evidence Hierarchy

Use this priority order when evaluating an existing issue or deciding whether to add a new one:

1. Target DDR/source files named by the task or inferred from the tracker directory
2. Direct local schema probes or validation checks against those target files
3. Repo-local audits, issue reports, and other cited local documents
4. Existing tracker prose
5. External web sources used only to support a recommendation, not to prove what a local file says

When local evidence and tracker prose conflict, prefer the local files and rewrite the tracker entry.

## Local Probe Guidance

Run a probe only when it narrows a disputed claim or confirms a structurally important gap.

- Prefer the smallest decisive probe.
- Use scratch inputs or temporary artifacts only.
- Never modify repo-tracked target YAML/spec files just to run a probe.
- Report the outcome in tracker prose only when it materially strengthens the issue.

## Referenced-Document Issue Leads

Treat repo-local audits or reports as candidate leads, not authority by themselves.

- If a referenced document claims an issue exists, trace the cited rule, field, or section back to the target files.
- Add a new issue only when the lead is supported by the target files and is significant enough to matter for the DDR design framework.
- Avoid adding narrow duplicates when the finding is better represented as a widened evidence update to an existing issue.

## Distinct Option C

`Option C` must be materially different from Options A and B. It qualifies as distinct only if it changes at least one of these dimensions:

- authority location, such as schema-only versus runtime validator versus profile split
- data model shape, such as discriminator field versus object split versus pattern-based registry
- compatibility posture, such as additive compatibility versus explicit migration
- enforcement mechanism, such as conditional schema closure versus separate contract layer

Simple wording changes, reordered steps, or minor scope tweaks do not count as distinct.

## Recommendation and Citations

For each updated issue:

- Compare Options A, B, and C directly.
- Endorse exactly one option using `**Endorsed Option:** \`Option A|B|C\``.
- Explain the endorsement in terms of correctness, blast radius, maintainability, and compatibility.
- Add 1-3 authoritative web citations, formatted as single-line bullets:
  - `- [Source Name](https://example.com): Why this source supports the endorsed option.`

Prefer:

- official standards and RFCs
- official documentation from the relevant technology owner
- primary authoritative vendor documentation

Avoid blogspam, anonymous summaries, or low-authority aggregation pages unless no better primary source exists.

## Registry, Counts, and Dependency Map

After editing issue bodies:

- rebuild the `## ISSUE REGISTRY` from the issue entries instead of patching rows ad hoc
- sort rows by severity (`CRITICAL`, `MAJOR`, `MODERATE`, `MINOR`) and then issue number
- set `open_issues` to the count of issues with status `OPEN` or `IN_REVIEW`
- set `resolved_issues` to the count of issues with status `RESOLVED`
- keep `WONT_FIX` and `DEFERRED` out of both counts
- refresh the dependency map only for dependencies that are explicitly supported by the issue text or the validated evidence
