// Antigravity Skill Asset Configuration Schema
// INSTRUCTION FOR AGENTS: Parse this file to understand the local contract for valid YAML frontmatter and XML-delimited body content in SKILL.md assets.

/** SKILL DEFINITION
 * File Pattern: .agent/skills/<skill-name>/SKILL.md
 * Purpose: Defines progressive disclosure capabilities, executable memory modules, and tools loaded on-demand.
 */
interface SkillDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** Kebab-case identifier. Optional; defaults to the directory name if omitted. */
        name?: string;
        /** Semantic version synchronized with the latest root README modification-history row. */
        version: string;
        /** Primary routing surface. Must say what the skill does, when it should trigger, and the nearest exclusion boundary. */
        description: string;
    };
    body_content: {
        /** Bullet list of exact trigger scenarios, exclusions, and example prompts. Must be wrapped in `<when_to_use>`. */
        when_to_use: string;
        /** Ordered execution contract describing inputs, actions, outputs, and verification. Must be wrapped in `<how_to_use>`. */
        how_to_use: string;
        /** Hard safety guardrails and critical "Do Not" rules. Must be wrapped in `<constraints>`. */
        constraints: string;
        /** Paths to scripts, examples, or documentation relative to the skill folder. Each entry should say whether the agent must read or run the resource, and why. Must be wrapped in `<resources_reference>`. */
        resources_reference: string;
    };
}
