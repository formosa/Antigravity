# DESIGN_JUSTIFICATION: Antigravity Security Policy Assets v1.21.9

<document_purpose>
This document establishes the verified architectural pattern for implementing Security Policies as high-priority Rule assets within the Antigravity IDE v1.21.9 ecosystem.
</document_purpose>

<schema_evaluation_and_justification>

- **Routing Engine Alignment:** Encoding Security Policies as Rule assets preserves `priority: critical` and `trigger: always_on` semantics so security constraints remain ahead of lower-priority style or convenience rules.
- **Context Anchoring:** Always-on rule placement ensures `gemini-3-pro-preview` and `gemini-3-flash-preview` inherit the same hard security boundary during agentic execution.
- **Deterministic Prevention:** The explicit `<verification_step>` forces a silent preflight check before the model leaks credentials, touches forbidden paths, or overreaches network access.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [ADK Coding with AI](https://adk.dev/tutorials/coding-with-ai/)
   - Current Google-authored guidance for rule-driven Antigravity coding workflows and `.agent/` contract surfaces.
2. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official guidance for isolating strict negative constraints so security rules resist instruction drift.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                                       |
| :--------- | :------ | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `security-policy.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework.                                                |
| 2026-04-04 | v1.1.1  | Governance     | Updated `primary_owner_skill` from `dev-schema` to `core-schema` so canonical schema stewardship follows the new foundational `core-*` family while leaving the Security Policy schema unchanged. |
| 2026-04-07 | v1.21.9 | Compatibility  | Replaced the stale `v1.18.3` runtime claim and refreshed the design basis around the current Antigravity rule surface and Gemini 3 preview execution context.                                      |

</modification_history>

<schema_governance>

```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```

</schema_governance>
