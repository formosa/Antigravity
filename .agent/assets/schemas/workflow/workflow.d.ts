// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR GEMINI 3.1 PRO AND ANTIGRAVITY v1.18.3
// SCHEMA VERSION: 2026.02.23-v1.18.3

/** WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 * Purpose: Defines active, user-triggered sequential operations for repetitive engineering tasks.
 */
interface WorkflowDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** The shortcut command name (used with a slash command). */
        name?: string;
        /** Schema version for tracking modifications (e.g., "1.1.0"). */
        version: string;
        /** A summary of the workflow's purpose. */
        description: string;
    };
    body_content: {
        /** Numbered sequence of atomic instructions. Each step ends with verification. Must be wrapped in `<steps>`. */
        steps: string;
        /** Conditions that must be met to consider the workflow successfully completed. Must be wrapped in `<verification_plan>`. */
        verification_plan?: string;
    };
}
