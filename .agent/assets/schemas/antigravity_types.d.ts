// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR GEMINI 3.1 PRO AND ANTIGRAVITY v1.18.3
// SCHEMA VERSION: 2026.02.23-v1.18.3

/**
 * 1. GEMINI CONFIGURATION DEFINITION
 * File Pattern: ~/.gemini/GEMINI.md or .agent/GEMINI.md
 * Single source of truth for agent behavior and strict security guardrails.
 */
interface GeminiMdConfiguration {
    frontmatter: {
        schema_version: string;
        description: string;
        // Restricts operations to current available Gemini 3 variants.
        models: Array<'gemini-3.1-pro-preview' | 'gemini-3-flash'>;
        scope: 'global' | 'workspace';
        // 'high' for 3.1 Pro complex reasoning; 'minimal' for Flash speed.
        thinking_level?: 'minimal' | 'low' | 'medium' | 'high';
        include_thoughts?: boolean;
        temperature?: number;
    };
    body_content: {
        workspace_context: string;
        cognitive_directives: string;
        // Security is now merged directly into the core configuration.
        security_and_execution_guardrails: string;
        thought_signature_protocol: string;
        activation_rules?: string;
    };
}

/**
 * 2. RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 */
interface RuleDefinition {
    type: 'rule';
    name: string;
    activation: 'always_on' | 'model_decision' | '@mention' | 'glob';
    priority: 'low' | 'medium' | 'high' | 'critical';
    globs?: string;
    scope?: 'workspace' | 'global';
    description: string;
    constraints?: string[];
    verification_step?: string;
}

/**
 * 3. SKILL DEFINITION
 * File Pattern: .agent/skills/<skill-name>/SKILL.md
 * Note: No type discriminator. Relies on semantic description matching.
 */
interface SkillDefinition {
    frontmatter: {
        name?: string;
        description: string;
        scope?: 'workspace' | 'global';
    };
    body_content: {
        overview: string;
        when_to_use: string;
        instructions: string;
        examples?: string;
    };
}

/**
 * 4. WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 */
interface WorkflowDefinition {
    frontmatter: {
        name: string;
        description: string;
        trigger?: string;
    };
    body_content: {
        steps: string;
        verification_plan?: string;
    };
}

/**
 * 5. IMPLEMENTATION PLAN DEFINITION
 * File Pattern: implementation_plan.md or .agent/plans/*.md
 */
interface ImplementationPlanDefinition {
    frontmatter?: {
        task?: string;
        model?: 'gemini-3.1-pro-preview' | 'gemini-3-flash';
    };
    body_content: {
        objective: string;
        atomic_steps: string[];
        verification: string[];
        risks_and_mitigations?: string;
    };
}

/**
 * 6. TASK EXECUTION STATE DEFINITION
 * File Pattern: task.md or TASK-XXXXXX.md
 */
interface TaskExecutionState {
    task_metadata: {
        task_id: string;
        title: string;
        priority: 'low' | 'medium' | 'high' | 'critical';
        plan_reference: string;
        target_model?: 'gemini-3.1-pro-preview' | 'gemini-3-flash';
    };
    status: 'uncompleted' | 'in_progress' | 'completed';
    dependencies?: {
        task_dependencies?: string[];
        file_dependencies?: string[];
    };
    expected_output?: string;
    constraints?: string;
    verification?: {
        pre_check?: string;
        acceptance_criteria?: string[];
        rollback_procedure?: string;
    };
}

/**
 * 7. WALKTHROUGH DEFINITION
 * File Pattern: walkthrough.md
 */
interface WalkthroughDefinition {
    execution_summary: string;
    architectural_changes: string;
    artifacts_generated?: string[];
    verification_steps: string;
}
