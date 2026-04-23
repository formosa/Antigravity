---
name: "rules-governance"
description: "Glob-scoped collection governance rule for the .agent/rules/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/rules/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Scope Boundary: This rule governs only assets under .agent/rules/.
2. Rule Frontmatter Contract: Rule assets MUST satisfy the YAML frontmatter requirements (
ame, ersion, description, 	rigger, priority).
3. Rule Body Fencing: Rule assets MUST wrap all body content inside a non-empty <constraints> block and MAY include a <verification_step> block.
</constraints>

<verification_step>
Confirm all rules conform to the basic frontmatter and body fencing requirements.
</verification_step>
