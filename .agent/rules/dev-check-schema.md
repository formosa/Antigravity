---
name: dev-check-schema
description: "Enforces 100% strict compliance for Antigravity asset definitions using standard hardware-aware validation."
version: "1.2.0"
trigger: glob
globs: ".agent/schemas/**/*.md, .agent/rules/**/*.md"
priority: critical
execution_tier: standard
---

<constraints>

# Antigravity Asset Schema Enforcement

- **Frontmatter Integrity:** Every `.md` asset in `.agent/` must include `version: "1.2.0"` and a `description` exceeding 60 characters for semantic routing accuracy.
- **Resource Protection:** Rules MUST utilize `execution_tier: standard` to preserve system stability and IDE responsiveness.
- **No Placeholders:** Usage of `TODO`, `N/A`, or generic descriptions is a schema violation.
- **Strict XML Fencing:** The *entirety* of the body content, including Markdown headers, must be wrapped in XML tags (`<constraints>` and optionally `<verification_step>`).

</constraints>

<verification_step>

1. **Schema Audit:** Cross-reference YAML keys against the `RuleDefinition` interface in `rule.d.ts` to ensure full compliance.
2. **Resource Check:** Verify that the target file does not aggressively request `parallel_high_perf` unless strictly justified by a heavy, non-LLM parallel workload.
3. **Semantic Density Check:** Confirm the `description` provides enough context for Gemini 3.1 Pro's router to differentiate it from global rules.

</verification_step>
