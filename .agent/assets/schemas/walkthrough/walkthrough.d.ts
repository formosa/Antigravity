// walkthrough.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** WALKTHROUGH DEFINITION
 * File Pattern: walkthrough.md
 * Purpose: Post-execution summary and manual verification guide serving as definitive proof of work.
 */
interface WalkthroughDefinition {
    // Note: Walkthroughs generally do not require frontmatter as they are static output artifacts.
    body_content: {
        // Brief recap of the solved objective. Must be wrapped in <execution_summary>.
        execution_summary: string;
        // Highlight of major file modifications and structural updates. Must be wrapped in <architectural_changes>.
        architectural_changes: string;
        // Explicit commands or UI interactions the user must perform to validate the feature. Must be wrapped in <verification_steps>.
        verification_steps: string;
    };
}
