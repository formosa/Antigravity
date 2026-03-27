<document_purpose>
This reference file captures the durable quality rules for Resolution Reports produced by
`agent-create-issue-report`.
</document_purpose>

<report_rules>

## Evidence Rules

1. **Local Evidence First:** Prefer the smallest decisive set of local files that can confirm or refute the issue.
2. **Repo-Relative Citations:** Cite local evidence with repo-relative paths and line spans, not absolute machine paths.
3. **Minimal Quotations:** Quote only the minimum text needed to support a finding. Summaries should do the rest.
4. **Tracker-Only Fallback:** If no corroborating project file exists, state that explicitly rather than implying deeper proof than you have.

## Strategy Rules

1. **True A/B Separation:** Option A and Option B must represent meaningfully different design choices, not surface variations of the same fix.
2. **Two Options Only:** New reports always emit exactly two options. Do not generate Option C.
3. **Citation Integrity:** Use 1-2 authoritative primary sources per option when they materially strengthen the recommendation. If none applies, use the exact fallback sentence from the template.
4. **Project-Grounded Insights:** Supporting Insights should connect the option back to the issue's actual contract, schema, code path, or system behavior.

## Recommendation Rules

1. **Issue-Relevant Tradeoffs:** Compare on 2-4 dimensions that matter for the specific issue, not generic boilerplate.
2. **Objective Endorsement:** Recommendations should be justified in terms of contract fidelity, blast radius, compatibility, validation strength, and future flexibility.
3. **Self-Contained Output:** The report must stand on its own without forcing the reader back into the tracker.

## Implementation Note Rules

1. **Resolved Issues:** Summarize the implemented change and the validation evidence that confirms the fix.
2. **Unresolved Issues:** State clearly that implementation remains pending and that generating the report did not apply a repository patch.

</report_rules>
