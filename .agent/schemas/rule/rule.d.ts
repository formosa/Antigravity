// Antigravity Agent Asset Configuration Schema
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict schema requirements for generating valid YAML frontmatter and XML-delimited body content in .md agent Rule assets.

/** RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 * Purpose: Defines conditional, file-specific guidelines and negative constraints injected dynamically.
 */
interface RuleDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** The human-readable display name for the rule. Optional; defaults to file name if omitted. */
        name?: string;
        /** Schema version for tracking modifications (e.g., "1.2.0"). */
        version: "1.2.0";
        /** Semantic metadata explaining the rule's purpose. CRITICAL: Strictly required for the IDE semantic router. */
        description: string;
        /** Dictates when the IDE routing engine must inject this rule into the LLM context. */
        trigger: 'auto' | 'manual' | 'glob' | 'always_on' | '@mention';
        /** Comma-separated wildcard patterns (e.g., '*.py, ui/**\/*.qml'). Required if trigger is set to 'glob'. */
        globs?: string;
        /** The importance weight of this rule when conflicts occur. */
        priority: 'low' | 'medium' | 'high' | 'critical';
        /** Directs the IDE to utilize specific CPU thread-pools. Strongly recommend 'standard' to prevent OS-level thread starvation during agentic tasks. */
        execution_tier?: 'standard' | 'parallel_high_perf';
    };
    body_content: {
        /** Bullet or numbered list of NEGATIVE and POSITIVE constraints. Must be wrapped entirely in XML tags. */
        constraints: string;
        /** Specific verification checks the agent MUST perform. Should focus on high-level reasoning rather than deterministic static analysis. */
        verification_step?: string;
    };
}
