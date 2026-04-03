---
name: example-rule
version: "1.0.0"
description: "Applies a bounded rule to a specific trigger context while keeping the scope narrow and verifiable."
trigger: manual
priority: medium
execution_tier: standard
---
<constraints>

- State the exact files, contexts, or operations the rule governs.
- Prefer concrete positive or negative constraints over broad style guidance.
- Keep the rule focused on one coherent enforcement surface.
- Use repo-relative forward-slash paths when the rule references workspace locations.
</constraints>

<verification_step>

1. Confirm the rule trigger matches the requested scope.
2. Confirm every frontmatter field is valid for the selected trigger mode.
3. Confirm the rule body contains only verifiable constraints that do not exceed the intended boundary.
</verification_step>
