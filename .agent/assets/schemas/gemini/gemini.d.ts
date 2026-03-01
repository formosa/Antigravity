// gemini.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO AND GEMINI 3 FLASH

/** 1. GEMINI CONFIGURATION DEFINITION
 * File Pattern: ~/.gemini/GEMINI.md or .agent/GEMINI.md
 * Purpose: Replaces legacy Persona schemas. Defines the absolute constraints, operational mandates, and cognitive parameters for the Gemini 3 series global/workspace agents.
 */
interface GeminiMdConfiguration {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        /** High-level summary of the workspace purpose, scope, and objectives. Used for routing. */
        description: string;
        /** Allowed models for this workspace. Restricts operations to specified Gemini 3 variants. Includes fallbacks. */
        models: Array<'gemini-3.1-pro' | 'gemini-3.1-pro-preview' | 'gemini-3-pro' | 'gemini-3-flash'>;
        /** Schema version for compatibility checks and tracking modifications (e.g., "20260222_v118", "1.0.0"). */
        version: string;
        /** Global applies everywhere; workspace overrides global settings. */
        scope: 'global' | 'workspace';
        /** Primary dial for trading latency against cognitive depth. 'minimal' for Flash; 'medium' for optimal 3.1 Pro software engineering. */
        thinking_level?: 'minimal' | 'low' | 'medium' | 'high';
        /** Determinism slider (e.g., 0.1 for strict code generation). Range: 0.0 to 1.0 */
        temperature?: number;
    };
    body_content: {
        /** Establishes primary environment and tech stack. Heavy context should be placed here (first in prompt). Wrapped in `<workspace_context>`. */
        workspace_context: string;
        /** Sets reasoning parameters, silent reasoning preferences, and structured output schemas. Wrapped in `<cognitive_directives>`. */
        cognitive_directives: string;
        /** Strict negative constraints, prohibited operations, and boundary validation rules. Wrapped in `<security_and_execution_guardrails>`. */
        security_and_execution_guardrails: string;
        /** Strict mandate requiring the circulation of encrypted reasoning states for multi-turn coherence. Wrapped in `<thought_signature_protocol>`. */
        thought_signature_protocol: string;
        /** How the configuration is triggered (e.g., 'always-on', '@mention'). Wrapped in `<activation_rules>`. */
        activation_rules?: string;
    };
}
