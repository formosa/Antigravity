// implementation_plan.d.ts
// Antigravity Agent Asset Configuration Schema (v1.21.9)
// OPTIMIZED FOR GEMINI 3.1 PRO PREVIEW

/** IMPLEMENTATION PLAN DEFINITION
 * File Pattern: YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md
 * Storage:      .agent/plans/           (active)
 *               .agent/plans/processed/ (completed)
 * Purpose: A technical design artifact generated during PLANNING mode, requiring user
 *          approval before execution. Progress-tracked for complex, long-running, or
 *          high-risk objectives. Relocated to processed/ upon full completion.
 */
interface ImplementationPlanDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** One-sentence measurable objective for the proposed change. */
        task: string;
        /** The model designated for planning. */
        model: 'gemini-3.1-pro-preview' | 'gemini-3.1-pro-preview-customtools';
        /** Schema version for tracking modifications (e.g., "1.0.0"). */
        version: string;
        /**
         * Controls the depth of internal model reasoning before response generation.
         * Use HIGH for architectural planning or novel multi-system coordination.
         * Use MEDIUM for standard bounded engineering tasks (default for most plans).
         * Required — do not omit.
         */
        thinking_level: 'HIGH' | 'MEDIUM' | 'LOW';
    };
    body_content: {
        /** High-level overview of the problem and proposed change. Must be wrapped in `<objective>`. */
        objective: string;
        /** Phased development roadmaps for complex projects. Must be wrapped in `<phases>`. */
        phases?: Array<{
            phase_id: string;
            objectives: string[];
            task_references: string[];
            entry_criteria: string[];
            exit_criteria: string[];
            assigned_model: 'gemini-3.1-pro-preview' | 'gemini-3.1-pro-preview-customtools' | 'gemini-3-flash' | 'gemini-3.1-flash';
        }>;
        /**
         * Array of atomic execution steps representing single responsibilities.
         * Must be wrapped in `<atomic_steps>`.
         *
         * For complex, long-running, or high-risk plans: steps MUST be organized into
         * named sections (### SECTION_NAME) each preceded by progress checkboxes:
         *   - [ ] Step N — <description>   (pending)
         *   - [X] Step N — <description>   (completed)
         *
         * Checkbox update rule: update section checkboxes to [X] immediately after
         * successful section completion. Update on-disk before proceeding.
         */
        atomic_steps: string[];
        /** Array of mapped verification checks. Must be wrapped in `<verification>`. 1:1 mapping with atomic_steps. */
        verification: string[];
        /** Potential failure points and mitigations. Must be wrapped in `<risks_and_mitigations>`. */
        risks_and_mitigations?: string;
        /**
         * Optional large-context anchor comment block at the END of the artifact.
         * Restate the task objective and in-scope file constraints as an HTML comment.
         * Required when total plan input context is expected to exceed 50K tokens.
         * Improves executor attention retention across the full 1M-token context window.
         */
        large_context_anchor?: string;
    };
    lifecycle: {
        /**
         * Filename pattern (generated at creation time):
         *   YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md
         * Example: 20260401-143022-a3f7c12b-IMPLEMENTATION_PLAN.md
         */
        filename: string;
        /** Plan state. Transitions: pending → in_progress → completed. */
        state: 'pending' | 'in_progress' | 'completed';
        /**
         * When state transitions to 'completed' (all checkboxes [X]),
         * the agent MUST move the file:
         *   .agent/plans/<filename> → .agent/plans/processed/<filename>
         * Filename is preserved unchanged.
         */
        active_path: '.agent/plans/';
        processed_path: '.agent/plans/processed/';
    };
}
