# Artifact Issue Report Reference

## Scope

This owner skill manages the standalone issue-report artifact family.

- It generates canonical two-option issue reports from a source Issues Tracker.
- It maintains existing issue reports and upgrades legacy reports to the canonical format on first write.
- It validates canonical and legacy reports with the matching validator profile.
- It does not edit the source Issues Tracker.
- It does not patch target DDR/spec/YAML files.

## Mode Guidance

Use these modes intentionally:

- `generate`
  - create a new canonical issue report from one tracker issue
- `maintain`
  - refresh, repair, or migrate an existing issue report while keeping it aligned with the tracker and local evidence
- `validate`
  - validate an issue report read-only and report whether it is canonical or legacy

## Evidence Rules

1. **Local Evidence First:** Prefer the smallest decisive set of local files that can confirm or refute the issue.
2. **Repo-Relative Citations:** Cite local evidence with repo-relative paths and line spans, not absolute machine paths.
3. **Minimal Quotations:** Quote only the minimum text needed to support a finding. Summaries should do the rest.
4. **Tracker-Only Fallback:** If no corroborating project file exists, state that explicitly rather than implying deeper proof than you have.

## Strategy Rules

1. **True A/B Separation:** Option A and Option B must represent meaningfully different design choices, not surface variations of the same fix.
2. **Two Options Only:** Canonical reports always emit exactly two options. Do not generate Option C in standalone reports.
3. **Citation Integrity:** Use 1-2 authoritative primary sources per option when they materially strengthen the recommendation. If none applies, use the exact fallback sentence from the template.
4. **Project-Grounded Insights:** Supporting Insights should connect each option back to the issue's actual contract, schema, code path, or system behavior.

## Maintenance Rules

1. **Canonical Preservation:** Keep canonical reports in the active two-option shape with an explicit Implementation Note.
2. **Legacy Upgrade On Write:** Legacy v4/v5 reports may remain read-only, but once a task modifies them, migrate them to the canonical shape before returning success.
3. **Identity Consistency:** Preserve the issue id, report subject, and tracker alignment. Do not update a report against the wrong tracker issue.
4. **Bounded Scope:** Only update what the tracker and local evidence require. Do not drift into tracker maintenance or implementation work.

## Recommendation Rules

1. **Issue-Relevant Tradeoffs:** Compare on 2-4 dimensions that matter for the specific issue, not generic boilerplate.
2. **Objective Endorsement:** Recommendations should be justified in terms of contract fidelity, blast radius, compatibility, validation strength, and future flexibility.
3. **Self-Contained Output:** The report must stand on its own without forcing the reader back into the tracker.

## Implementation Note Rules

1. **Resolved Issues:** Summarize the implemented change and the validation evidence that confirms the fix.
2. **Unresolved Issues:** State clearly that implementation remains pending and that generating or maintaining the report did not apply a repository patch.
