// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR OWNER-MANAGED WORKFLOW ASSETS (v1.2.0)
// INSTRUCTION FOR AGENTS: Parse this file to understand the required structure
// for governed workflow assets maintained by dev-workflow.

/** WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 * Purpose: Defines active, user-triggered sequential operations for repetitive engineering tasks.
 */
interface WorkflowDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** Optional shortcut or stable workflow identifier. Defaults to the filename stem when omitted. */
        name?: string;
        /** Schema version for tracking modifications (e.g., "1.1.0"). */
        version: string;
        /** A concise summary of the workflow's purpose and intended trigger context. */
        description: string;
    };
    body_content: {
        /** Numbered sequence of atomic instructions encoded under the Markdown heading `### steps`. */
        steps: string;
        /** Optional completion criteria encoded under the Markdown heading `### verification_plan`. */
        verification_plan?: string;
    };
}
