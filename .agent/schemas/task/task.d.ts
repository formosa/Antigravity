// task.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** TASK DEFINITION
 * File Pattern: task.md or TASK-XXXXXX.md
 * Purpose: A dynamic checklist governing the atomic execution steps of an approved implementation plan.
 */
interface TaskDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** Globally unique identifier. */
        task_id: string;
        /** Title or brief description. */
        title: string;
        /** Schema version for tracking modifications (e.g., "1.1.0"). */
        version: string;
        /** Execution priority order. */
        priority: 'low' | 'medium' | 'high' | 'critical';
        /** Model designated for execution. */
        target_model: 'gemini-3.1-pro' | 'gemini-3-flash';
        /** Prerequisite task IDs that must complete first. */
        task_dependencies?: string[];
        /** Required files that must exist before execution. */
        file_dependencies?: string[];
    };
    body_content: {
        /** Expected tangible output. Must be wrapped in `<expected_output>`. */
        expected_output: string;
        /** Constraints limiting how the task can be fulfilled. Must be wrapped in `<constraints>`. */
        constraints?: string;
        /** Explicit verification instructions before generation. Must be wrapped in `<pre_check>`. */
        pre_check: string;
        /** Measurable conditions for task completion. Must be wrapped in `<acceptance_criteria>`. */
        acceptance_criteria: string[];
        /** Steps to revert changes if verification fails. Must be wrapped in `<rollback_procedure>`. */
        rollback_procedure: string;
    };
}
