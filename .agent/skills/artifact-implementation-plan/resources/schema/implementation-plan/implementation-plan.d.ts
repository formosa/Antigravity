// implementation_plan.d.ts
// Antigravity Agent Asset Configuration Schema (v1.20.6)
// OPTIMIZED FOR GEMINI 3.1 PRO PREVIEW
// NOTE: gemini-3-pro-preview is DISCONTINUED as of 2026-03-26.
//       Use 'gemini-3.1-pro-preview' for all new and existing plan generation.

/** IMPLEMENTATION PLAN DEFINITION
 * File Pattern: `.agent/plans/YYYYMMDD-HHMMSS[-NN]-IMPLEMENTATION_PLAN.md`
 * Archive Pattern: `.agent/plans/processed/YYYYMMDD-HHMMSS[-NN]-IMPLEMENTATION_PLAN.md`
 * Purpose: A technical design artifact generated during PLANNING mode.
 *          Requires human approval before executor initiates any file modifications.
 *          Upon full executor verification, must be relocated to `.agent/plans/processed/`.
 *          Historical artifacts already present in `.agent/plans/processed/` may predate this contract and remain reference-only.
 */
interface ImplementationPlanDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** One-sentence measurable objective. Precise enough for unambiguous approval or rejection. */
        task: string;
        /** The model designated for planning. Constrained decoding.
         *  Use 'gemini-3.1-pro-preview' (current active model string as of 2026-03-26).
         *  'gemini-3.1-pro' remains an accepted alias in the schema contract.
         */
        model: 'gemini-3.1-pro-preview' | 'gemini-3.1-pro';
        /** Schema version for tracking modifications (e.g., "1.0.0", "1.1.0"). */
        version: string;
        /** Fully resolved output path including filename.
         *  Pattern: `.agent/plans/YYYYMMDD-HHMMSS[-NN]-IMPLEMENTATION_PLAN.md`
         */
        output_path: string;
        /** Fully resolved post-execution archive path including filename.
         *  Pattern: `.agent/plans/processed/YYYYMMDD-HHMMSS[-NN]-IMPLEMENTATION_PLAN.md`
         */
        processed_path: string;
    };
    body_content: {
        /** One measurable implementation objective. Must be wrapped in `<objective>`. */
        objective: string;

        /** Phased execution roadmap for complex projects. Must be wrapped in `<phases>`.
         *  Each phase must have clear entry_criteria and exit_criteria.
         *  Assign 'gemini-3.1-pro-preview' for architecture/high-complexity phases.
         *  Assign 'gemini-3-flash' for high-volume, low-latency implementation phases.
         */
        phases?: Array<{
            phase_id: string;
            objectives: string[];
            task_references: string[];
            entry_criteria: string[];
            exit_criteria: string[];
            assigned_model: 'gemini-3.1-pro-preview' | 'gemini-3.1-pro' | 'gemini-3-flash';
        }>;

        /** Grouped atomic execution steps with completion trackers.
         *  Must be wrapped in `<atomic_steps>`.
         *
         *  Format requirements:
         *  - Organize steps into named logical groups using #### headers.
         *  - Prefix every step with `- [ ]` (unchecked tracker).
         *  - Executor updates completed steps to `- [X]` during execution.
         *  - Each step must use the Intent -> Action -> Outcome pattern.
         *  - State CREATE, MODIFY, or DELETE explicitly when ambiguity is possible.
         *  - Maintain 1:1 step number correspondence with <verification> items.
         *
         *  Example group format:
         *  #### Group 1 — Setup
         *  - [ ] 1. CREATE `path/to/file.py` to establish ...
         *  - [ ] 2. MODIFY `path/to/config.yaml` to configure ...
         */
        atomic_steps: string[];

        /** Verification checks mapped 1:1 to atomic_steps by number.
         *  Must be wrapped in `<verification>`.
         *  Must prove intended post-state; not merely that activity occurred.
         *  Prefer existing project commands. Do not invent commands or results.
         */
        verification: string[];

        /** Potential failure points and containment/rollback guidance.
         *  Must be wrapped in `<risks_and_mitigations>`.
         *  Required for any step classified as Request Review (high risk).
         */
        risks_and_mitigations?: string;
    };
}
