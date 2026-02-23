// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO AND GEMINI 3 FLASH
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict schema requirements for generating valid YAML frontmatter and XML-delimited body content in .md asset files.

/** SKILL DEFINITION
 * File Pattern: .agent/skills/<skill-name>/SKILL.md
 * Purpose: Defines progressive disclosure capabilities, executable memory modules, and tools loaded on-demand.
 */
interface SkillDefinition {
    frontmatter: {
        // Kebab-case identifier. Optional; defaults to the directory name if omitted.
        name?: string;
        // CRITICAL: Functions as the primary "trigger condition". Must be highly precise for the semantic router to discover the skill.
        description: string;
    };
    body_content: {
        // Bullet list of exact scenarios where the agent should use this skill. Must be wrapped in XML tags (e.g., <when_to_use>).
        when_to_use: string;
        // Step-by-step silent reasoning, verification checklist, and expected output format. Must be wrapped in XML tags (e.g., <how_to_use>).
        how_to_use: string;
        // Hard safety guardrails and critical "Do Not" rules. Must be wrapped in XML tags (e.g., <constraints>).
        constraints?: string;
        // Paths to scripts, examples, or documentation relative to the skill folder. Must be wrapped in XML tags (e.g., <resources_reference>).
        resources_reference?: string;
    };
}
