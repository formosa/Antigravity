// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR GEMINI 3.1 PRO AND ANTIGRAVITY v1.18.3
// SCHEMA VERSION: 2026.02.23-v1.18.3

/** WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 * Purpose: Defines active, user-triggered sequential operations for repetitive engineering tasks.
 */
interface WorkflowDefinition {
    frontmatter: {
        // The shortcut command name (used with a slash command).
        name?: string;
        // A summary of the workflow's purpose.
        description: string;
    };
    body_content: {
        // Numbered sequence of atomic instructions. Each step ends with verification.
        steps: string;
        // Conditions that must be met to consider the workflow successfully completed.
        verification_plan?: string;
    };
}
