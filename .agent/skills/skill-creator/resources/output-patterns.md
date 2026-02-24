<document_purpose>
This document defines how agent skills must format outputs using the Antigravity v1.18.3 Artifact System.
</document_purpose>

<artifact_generation_rules>
Do not generate generic Markdown reports. All complex workflows must end by generating one of the following Execution State Artifacts:

1. **Implementation_Plan.md:** Used during the Planning phase. Must include `<phases>`, `<atomic_steps>`, and `<verification>` blocks. Requires human approval before the agent modifies code.
2. **Task.md:** Used to track active granular execution. Must include `<pre_check>` and `<rollback_procedure>` blocks.
3. **Walkthrough.md:** Used as proof-of-work upon completion. Must include `<execution_summary>`, `<architectural_changes>`, and explicit terminal commands in `<verification_steps>`.
</artifact_generation_rules>

<xml_fenced_outputs>
When generating localized files like `CHANGELOG.md` or configuration logs, you must isolate the strict formatting rules using localized XML tags to prevent instruction drift.

Example:
**Codebase Modification:** Update the `CHANGELOG.md` adhering strictly to the required formatting guidelines.
<changelog_constraints>

- Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security.
- Use imperative mood in all bullet points.
</changelog_constraints>
</xml_fenced_outputs>
