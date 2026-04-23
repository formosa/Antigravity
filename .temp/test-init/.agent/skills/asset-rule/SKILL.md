---
name: "asset-rule"
version: "1.0.0"
description: "Authors or refines compatible rule assets with explicit trigger boundaries."
---

<when_to_use>
- Creating a new governance rule.
- Modifying an existing rule.
</when_to_use>

<how_to_use>
1. Identify the need for the rule.
2. Create the file in .agent/rules/<rule-name>.md.
3. Fill out the YAML frontmatter and <constraints>.
</how_to_use>

<constraints>
- MUST strictly follow ule.d.ts schema.
</constraints>

<resources_reference>
- .agent/schemas/rule/rule.d.ts (Read to understand rule structure requirements).
</resources_reference>
