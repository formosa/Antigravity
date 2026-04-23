---
name: "workflows-governance"
description: "Glob-scoped collection governance rule for the .agent/workflows/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/workflows/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Workflow format: MUST be markdown based with clear numbered steps.
2. Step triggers: Steps that can be auto-executed should be marked with // turbo if safe.
</constraints>

<verification_step>
Verify that workflows use clear explicit directives.
</verification_step>
