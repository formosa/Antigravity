---
name: skill-creator
description: Generates Antigravity v1.18.3 compliant skills optimized for Gemini 3.1 Pro via progressive disclosure.
# HUMAN CONTEXT: This creator skill generates specialized toolchains utilizing the
# progressive disclosure architecture. It enforces strict XML fencing and Artifact
# generation to maintain the 1M-token context window economy and prevent
# instruction dilution during autonomous execution.
---

<when_to_use>

- The developer requests the creation, scaffolding, or initialization of a new custom skill.
- The active task involves extending the agent's capabilities with domain-specific workflows or tool integrations.
</when_to_use>

<how_to_use>

1. **Context Verification (Silent):** Confirm the user's requirements for the new skill (e.g., target domain, required scripts, necessary reference materials).
2. **Initialization:** Execute `python scripts/init_skill.py <skill-name> --path <output-directory>` to scaffold the deterministic directory structure.
3. **Content Generation:** Modify the newly generated `SKILL.md` file to implement the requested logic. You MUST use `<when_to_use>`, `<how_to_use>`, and `<constraints>` XML tags. Do NOT use legacy Markdown headings for core logic.
4. **Resource Population:** Populate the `scripts/` or `resources/` directories with any required auxiliary files. Ensure all references are mapped in the `<resources_reference>` block of the `SKILL.md`.
5. **Verification Artifact:** Output an `implementation_plan.md` artifact detailing the newly created skill's trigger conditions and capabilities for the human developer to review and approve.
</how_to_use>

<constraints>
- Never generate legacy frontmatter tags such as `type`, `scope`, or `priority` for Skills.
- Never use generic Markdown headers for execution steps. All operational directives must reside within XML fenced blocks.
- Do not include explanatory conversational text outside of the XML blocks.
</constraints>

<resources_reference>

- `scripts/init_skill.py`
- `scripts/package_skill.py`
- `scripts/quick_validate.py`
- `resources/workflows.md`
- `resources/output-patterns.md`
</resources_reference>
