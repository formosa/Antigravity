---
name: "skills-governance"
description: "Glob-scoped collection governance rule for the .agent/skills/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/skills/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Root README Update Required: When any file under .agent/skills/<skill-name>/ changes, update that skill's root README.md.
2. Version Synchronization: The changed skill's SKILL.md version MUST be incremented in the same task.
3. Schema Ownership: Skill-local schema mirrors are read-only.
</constraints>

<verification_step>
Before finishing any task that changes files under .agent/skills/, verify the updated root README.md and semantic version matches.
</verification_step>
