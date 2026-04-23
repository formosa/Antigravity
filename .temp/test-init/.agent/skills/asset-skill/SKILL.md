---
name: "asset-skill"
version: "1.0.0"
description: "Authors or refines compatible skills with explicit trigger boundaries and standard layouts."
---

<when_to_use>
- Creating a new skill asset.
- Modifying an existing skill asset's core capabilities.
</when_to_use>

<how_to_use>
1. Understand the goal of the new skill.
2. Scaffold a new folder in .agent/skills/<skill-name>.
3. Create the SKILL.md satisfying the canonical schema.
4. Create the README.md to track modification history.
</how_to_use>

<constraints>
- MUST strictly follow skill.d.ts schema.
- MUST define clear, bounded usage guidelines.
</constraints>

<resources_reference>
- .agent/schemas/skill/skill.d.ts (Read to understand skill structure requirements).
</resources_reference>
