// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO AND GEMINI 3 FLASH
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict schema requirements for generating valid YAML frontmatter and XML-delimited body content in .md asset files.

/** RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 * Purpose: Defines conditional, file-specific guidelines and negative constraints injected dynamically.
 */
interface RuleDefinition {
    frontmatter: {
        // The human-readable display name for the rule. Optional; defaults to file name if omitted.
        name?: string;
        // Semantic metadata explaining the rule's purpose. CRITICAL: Strictly required for the IDE semantic router.
        description: string;
        // Dictates when the IDE routing engine must inject this rule into the LLM context.
        trigger: 'auto' | 'manual' | 'glob' | 'always_on' | 'model_decision' | '@mention';
        // Comma-separated wildcard patterns (e.g., '*.py, ui/**/*.qml'). Required if trigger is set to 'glob'.
        globs?: string;
        // The importance weight of this rule when conflicts occur.
        priority: 'low' | 'medium' | 'high' | 'critical';
    };
    body_content: {
        // Bullet or numbered list of NEGATIVE and POSITIVE constraints. Must be wrapped in XML tags (e.g., <constraints>).
        constraints: string;
        // Specific silent verification checks the agent MUST perform before final output. Must be wrapped in XML tags.
        verification_step?: string;
    };
}
