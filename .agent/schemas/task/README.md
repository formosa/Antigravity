# DESIGN_JUSTIFICATION: Antigravity Task Assets v1.21.9

<document_purpose>
This document justifies the schema architecture for Task artifacts, which function as persistent state-tracking execution units for agents operating within Antigravity v1.21.9.
</document_purpose>

<schema_evaluation_and_justification>

- **State Persistence:** Dependencies and execution priority in frontmatter let the runtime queue or defer work without losing the bounded task contract.
- **Fail-Safe Mechanics:** Mandatory `<pre_check>` and `<rollback_procedure>` blocks keep `gemini-3-pro-preview` and `gemini-3-flash-preview` tied to explicit stop/go criteria rather than implicit continuation.
- **Context Boundaries:** `<constraints>` prevents task execution from bleeding into adjacent files or steps that belong in separate plan items.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official guidance for bounded tasks, explicit constraints, and structured prompt sections.
2. [ADK Coding with AI](https://adk.dev/tutorials/coding-with-ai/)
   - Current Antigravity-oriented guidance for planning, execution, and verification flows inside `.agent/` workspaces.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                            |
| :--------- | :------ | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `task.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework.                                                |
| 2026-04-04 | v1.1.1  | Governance     | Updated `primary_owner_skill` from `dev-schema` to `core-schema` so canonical schema stewardship follows the new foundational `core-*` family while leaving the Task schema unchanged. |
| 2026-04-07 | v1.21.9 | Compatibility  | Replaced stale `v1.18.3` and `gemini-3.1-*` compatibility text with the current Antigravity 1.21.9 and Gemini 3 preview task-execution contract.                                      |

</modification_history>

<schema_governance>

```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```

</schema_governance>
