// security_policy.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** SECURITY POLICY DEFINITION (Implemented via Rule engine)
 * File Pattern: .agent/rules/SECURITY_GUARDRAILS.md
 * Purpose: Explicit security boundaries protecting the workspace context, injected universally.
 */
interface SecurityPolicyDefinition {
    /** Encoded as standard YAML frontmatter block (---) at the top of the file. */
    frontmatter: {
        name: string;
        /** Schema version for tracking modifications (e.g., "1.1.0"). */
        version: string;
        description: string;
        /** CRITICAL: Security policies must universally apply to all agent contexts. */
        trigger: 'always_on';
        priority: 'critical';
    };
    body_content: {
        /** Array of strictly prohibited actions. Must be wrapped in `<forbidden_actions>`. */
        forbidden_actions: string[];
        /** Authorized external domains for URL fetching. Must be wrapped in `<allowed_domains>`. */
        allowed_domains: string[];
        /** Mandatory self-check before outputting code. Must be wrapped in `<verification_step>`. */
        verification_step: string;
    };
}
