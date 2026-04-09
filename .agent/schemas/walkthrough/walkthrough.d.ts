// walkthrough.d.ts
// Antigravity Agent Asset Configuration Schema (v1.21.9)
// OPTIMIZED FOR GEMINI 3 PRO PREVIEW

/** WALKTHROUGH DEFINITION
 * File Pattern: walkthrough.md
 * Purpose: Post-execution summary and manual verification guide serving as definitive proof of work.
 */
interface WalkthroughDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** Schema version for tracking modifications (e.g., "1.1.0"). */
        version: string;
    };
    body_content: {
        /** Brief recap of the solved objective. Must be wrapped in `<execution_summary>`. */
        execution_summary: string;
        /** Highlight of major file modifications and structural updates. Must be wrapped in `<architectural_changes>`. */
        architectural_changes: string;
        /** Explicit commands or UI interactions the user must perform to validate the feature. Must be wrapped in `<verification_steps>`. */
        verification_steps: string;
    };
}
