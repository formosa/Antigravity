// implementation_plan.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** IMPLEMENTATION PLAN DEFINITION
 * File Pattern: implementation_plan.md or .agent/plans/*.md
 * Purpose: A technical design artifact generated during PLANNING mode, requiring user approval before execution.
 */
interface ImplementationPlanDefinition {
    frontmatter: {
        // High-level overview of the proposed change.
        task: string;
        // The model designated for planning.
        model: 'gemini-3.1-pro' | 'gemini-3.1-pro-preview';
    };
    body_content: {
        // High-level overview of the problem and the proposed change. Must be wrapped in <objective>.
        objective: string;
        // Phased development roadmaps for complex projects. Must be wrapped in <phases>.
        phases?: Array<{
            phase_id: string;
            objectives: string[];
            task_references: string[];
            entry_criteria: string[];
            exit_criteria: string[];
            assigned_model: 'gemini-3.1-pro' | 'gemini-3-flash';
        }>;
        // Array of atomic execution steps representing single responsibilities. Must be wrapped in <atomic_steps>.
        atomic_steps: string[];
        // Array of mapped verification checks for each atomic step. Must be wrapped in <verification>.
        verification: string[];
        // Potential failure points and how they will be addressed. Must be wrapped in <risks_and_mitigations>.
        risks_and_mitigations?: string;
    };
}
