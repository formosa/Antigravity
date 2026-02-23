// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR GEMINI 3.1 PRO AND ANTIGRAVITY v1.18.3
// SCHEMA VERSION: 2026.02.23-v1.18.3

/**
 * WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 */
interface WorkflowDefinition {
    frontmatter: {
        name?: string;
        description: string;
    };
    body_content: {
        steps: string;
        verification_plan?: string;
    };
}
