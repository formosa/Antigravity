// Antigravity Agent Asset Configuration Schema (v1.13+)
// AUTHORITATIVE REFERENCE for LLM Context
// NOTE: Use YAML frontmatter for all agent asset definition Markdown files matching these interfaces.

/** * 1. PERSONA DEFINITION
 * File Pattern: .agent/personas/*.mdc
 */
interface PersonaDefinition {
    // Human-readable display name (Max ~25 chars).
    name: string;
    // Unique identifier for summoning/delegation.
    handle: `@${string}`;
    // One sentence summary of role for Router/User.
    description: string;
    // Specific backend. Use high-reasoning models for Architects/QAs.
    model: 'gemini-3-pro-high' | 'gemini-3-pro-low' | 'gemini-3-flash' | 'claude-sonnet-4.5' | 'claude-sonnet-4.5-thinking' | 'claude-opus-4.5-thinking' | 'gpt-oss-120b-medium';
    // 0.0 (code/linting) to 1.0 (creative/design).
    temperature: number;
    // UI visual accent (Hex Code or Color Name).
    color: string;
    // Avatar icon (Phosphor/Material name or relative SVG path).
    icon: string;
    // Allowlist of executable capabilities. Restrict dangerous tools for "Advisor" agents.
    tools: string[];
    // Files automatically loaded into context. Use sparingly. Provide [] if none.
    context_globs: string[];
}

/** * 2. RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 */
interface RuleDefinition {
    // Must be the first property.
    type: 'rule';
    // Display name for "Active Rules" status.
    name: string;
    // File patterns triggering this rule. If omitted, rule is global.
    globs?: string[];
    // Conflict resolution rank (High > Low). Default: 1. Critical Safety: >50.
    priority: number;
    // Keywords activating rule regardless of file type (e.g., "refactor").
    trigger?: string[];
    // 'mandatory' forces rejection of violations.
    severity: 'mandatory' | 'guideline' | 'suggestion';
    // Precise instruction prompt injected into system context.
    description: string;
}

/** * 3. TOOL DEFINITION
 * File Pattern: .agent/tools/*.md
 * Script Location: .agent/scripts/
 */
interface ToolDefinition {
    type: 'tool';
    // Function identifier used by LLM (snake_case). Unique.
    name: string;
    // Prompt explaining when/how to use the tool. Critical for selection.
    description: string;
    // Shell command. Supports {{args.x}} templating. Runs in project root.
    command: string;
    // Execution environment. 'system' uses default shell (PowerShell/Bash).
    runtime: 'system' | 'node' | 'python' | 'docker';
    // User permission requirement. Use 'never' only for safe read-ops.
    confirmation: 'always' | 'never';
    // Schema definition for required inputs to prevent hallucinations.
    args: Record<string, {
        type: 'string' | 'number' | 'boolean';
        description: string;
        required?: boolean;
    }>;
}

/** * 4. WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 */
interface WorkflowDefinition {
    type: 'workflow';
    // Action-oriented display title.
    name: string;
    // Slash command trigger (e.g., "/spec").
    slug: `/${string}`;
    // Summary for Router to suggest this workflow.
    description: string;
    // 'interactive' pauses for user approval after every step.
    mode: 'interactive' | 'autonomous';
    // Resources to preload (Globs or Agent Handles).
    context: string[];
    // Post-execution action string (e.g., "suggest_followup: /scaffold").
    on_finish: string;
    // Variables required from user before starting. Creates Form UI.
    inputs: Array<{
        name: string;
        type: 'text' | 'string' | 'boolean' | 'file_path';
        description?: string;
        default?: any;
        required?: boolean; // Default: true
    }>;
}

/** * 5. KNOWLEDGE DEFINITION
 * File Pattern: .agent/knowledge/*.md
 * Purpose: RAG Indexing Configuration.
 */
interface KnowledgeDefinition {
    // Unique identifier (snake_case).
    name: string;
    // Data sources (URLs or File Paths). Supports scraping and binaries.
    sources: string[];
    // Re-indexing frequency. 'always' runs on every build.
    refresh_schedule: 'always' | 'daily' | 'weekly' | 'manual';
    // Chunking strategy. Use 'code' for repos, 'prose' for docs.
    strategy: 'code' | 'prose' | 'mixed';
    // Permission scope (Agent Handles) or visibility level.
    access: string[] | 'public' | 'private';
}

/** * 6. EVALUATION DEFINITION
 * File Pattern: .agent/evals/*.md
 * Purpose: Automated QA/Testing for Agents.
 */
interface EvaluationDefinition {
    // Name of test suite.
    name: string;
    // The agent handle being tested.
    target_agent: `@${string}`;
    // Judge LLM. Should be stronger than target.
    judge_model: 'claude-opus-4.5-thinking' | 'gemini-3-pro-high';
    // Minimum pass score (0-100). Strict: 90+.
    pass_threshold: number;
    // Input prompts/scenarios to feed the agent.
    scenarios: string[];
    // Grading criteria for the Judge.
    rubric: string[];
}
