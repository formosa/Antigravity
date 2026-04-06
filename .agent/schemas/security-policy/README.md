# DESIGN_JUSTIFICATION: Antigravity Security Policy Assets v1.18.3

<document_purpose>
This document establishes the verified architectural pattern for implementing Security Policies as high-priority Rule assets within the Antigravity IDE v1.18.3 ecosystem.
</document_purpose>

<schema_evaluation_and_justification>

- **Routing Engine Alignment:** By structuring the Security Policy as a Rule rather than an untethered Markdown file, developers leverage the IDE's native `priority: critical` and `trigger: always_on` mechanics. This guarantees the security context is permanently injected and overrides lower-priority stylistic rules.
- **Context Anchoring:** The IDE's routing engine automatically places always-on rules at the optimal position within Gemini 3.1 Pro's context window, ensuring the model's attention mechanism heavily weights the `<forbidden_actions>` during generation.
- **Deterministic Prevention:** The explicit `<verification_step>` forces a silent reasoning loop, stopping the model from leaking credentials or executing unauthorized web calls before the payload is ever returned to the user interface.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Rules / Workflows - Google Antigravity Documentation](https://antigravity.google/docs/rules-workflows)
   - Confirms that Rule assets require YAML frontmatter for trigger definitions, allowing global injection of constraints like security policies.
2. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official documentation confirming the necessity of isolating strict negative constraints to prevent instruction drift in deep-reasoning models.
</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                                       |
| :--------- | :------ | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `security-policy.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework.                                                |
| 2026-04-04 | v1.1.1  | Governance     | Updated `primary_owner_skill` from `dev-schema` to `core-schema` so canonical schema stewardship follows the new foundational `core-*` family while leaving the Security Policy schema unchanged. |

</modification_history>

<schema_governance>
```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>