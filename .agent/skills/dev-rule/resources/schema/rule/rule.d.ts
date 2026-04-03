// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR OWNER-MANAGED RULE ASSETS (v1.3.0)
// INSTRUCTION FOR AGENTS: Parse this file to understand the required structure
// for governed rule assets maintained by dev-rule.

/** RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 * Purpose: Defines reusable rule assets that inject bounded constraints and optional verification checks into agent execution contexts.
 */
interface RuleDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** Optional stable rule identifier. Defaults to the filename stem when omitted. */
        name?: string;
        /** Semantic version for tracking rule-asset revisions (for example: "1.0.0"). */
        version: string;
        /** Concise routing summary explaining the rule's purpose, trigger context, and closest exclusions. */
        description: string;
        /** Determines when the rule should be injected into the active agent context. */
        trigger: 'auto' | 'manual' | 'glob' | 'always_on' | '@mention';
        /** Comma-separated wildcard patterns (for example: '*.py, .agent/skills/**'). Required when `trigger` is `glob`. */
        globs?: string;
        /** Relative importance when multiple rules overlap or conflict. */
        priority: 'low' | 'medium' | 'high' | 'critical';
        /** Execution-tier hint for heavy validation or auxiliary processing. Prefer `standard` unless a stronger case is justified. */
        execution_tier?: 'standard' | 'parallel_high_perf';
    };
    body_content: {
        /** Bullet or numbered list of positive and negative constraints. Must be wrapped entirely in `<constraints>`. */
        constraints: string;
        /** Optional verification checks the agent should perform before completion. Must be wrapped in `<verification_step>` when present. */
        verification_step?: string;
    };
}
