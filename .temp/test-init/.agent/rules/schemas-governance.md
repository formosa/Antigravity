---
name: "schemas-governance"
description: "Glob-scoped collection governance rule for the .agent/schemas/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/schemas/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Definition Contract: Schema files MUST be standard valid format (e.g. d.ts, json).
2. Version Bumps: Changes require a version bump in the README.md.
</constraints>

<verification_step>
Verify schema structural validity before concluding tasks.
</verification_step>
