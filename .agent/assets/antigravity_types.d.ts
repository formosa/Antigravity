// Antigravity Agent Asset Configuration Schema (v1.16.5)
// OPTIMIZED FOR AGENTIC CONSUMPTION AND LLM CONTEXT WINDOWS
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict schema requirements for generating valid YAML frontmatter in .md/.mdc asset files.

/** * 1. PERSONA DEFINITION
 * File Pattern: .agent/personas/*.mdc
 * Purpose: Defines the core identity, model backend, and base capabilities of an AI actor.
 */
interface PersonaDefinition {
    // The human-readable display name of the agent. Constraint: Max 25 characters.
    name: string;
    // The unique identifier used by the routing system or user to summon this specific agent. Must start with '@'.
    handle: `@${string}`;
    // A highly concise, one-sentence summary of the agent's primary function. Used by the semantic router for delegation.
    description: string;
    // The LLM backend to utilize. Instruction: Select 'gemini-3.1-pro' or 'claude-opus-4.6-thinking' for complex reasoning, architecture, or Python coding tasks. Use 'gemini-3-flash' for rapid, simple text processing.
    model: 'gemini-3.1-pro' | 'gemini-3-pro-high' | 'gemini-3-pro-low' | 'gemini-3-flash' | 'claude-sonnet-4.5' | 'claude-sonnet-4.5-thinking' | 'claude-opus-4.6-thinking' | 'gpt-oss-120b-medium';
    // Creativity slider. Constraint: Float between 0.0 (deterministic/code) and 1.0 (creative/prose).
    temperature: number;
    // The visual accent color for the agent's UI elements. Constraint: Must be a valid Hex Code (e.g., '#FF5733') or standard CSS color name.
    color: string;
    // The avatar icon identifier. Constraint: Must be a valid Phosphor icon name, Material icon name, or a relative path to an SVG file.
    icon: string;
    // An array of specific tool names (from ToolDefinition) this agent is authorized to execute. Leave empty [] if no tools are needed.
    tools: string[];
    // An array of Model Context Protocol (MCP) server names (e.g., 'postgres_local', 'bigquery_prod') the agent can query for dynamic data context. Optional.
    mcp_servers?: string[];
    // An array of file glob patterns (e.g., ['src/**/*.py', 'docs/*.md']) automatically injected into the agent's context window upon initialization. Use sparingly to save tokens.
    context_globs: string[];
}

/** * 2. RULE DEFINITION
 * File Pattern: .agent/rules/*.md
 * Purpose: Injects strict behavioral guidelines, coding standards, or domain-specific constraints into the agent's system prompt.
 */
interface RuleDefinition {
    // Identifies this asset as a rule. Constraint: Must always be the exact string 'rule'.
    type: 'rule';
    // The human-readable display name for the rule shown in the "Active Rules" UI.
    name: string;
    // Dictates when the LLM must process this rule. 'always_on' injects globally. 'glob' triggers on file match. 'model_decision' relies on semantic relevance. 'manual' requires user invocation.
    activation?: 'always_on' | 'model_decision' | 'glob' | 'manual';
    // The file patterns that trigger this rule if activation is set to 'glob' (e.g., ['*.py']). Optional.
    globs?: string[];
    // The importance weight of this rule when conflicts occur. Constraint: Integer. Higher number = higher priority. Critical safety constraints should be > 50.
    priority: number;
    // An array of specific words or phrases that, if detected in the user prompt, will activate this rule. Optional.
    trigger?: string[];
    // The strictness level. 'mandatory' means the agent must refuse requests that violate the rule.
    severity: 'mandatory' | 'guideline' | 'suggestion';
    // The actual system prompt instructions injected into the LLM context. Must be highly precise and unambiguous.
    description: string;
}

/** * 3. TOOL DEFINITION
 * File Pattern: .agent/tools/*.md
 * Purpose: Defines custom executable functions that the agent can invoke to interact with the external environment.
 */
interface ToolDefinition {
    // Identifies this asset as a tool. Constraint: Must always be the exact string 'tool'.
    type: 'tool';
    // The strict programmatic identifier for the function. Constraint: Must be snake_case and globally unique.
    name: string;
    // A detailed explanation of what the tool does, when to use it, and what it returns. CRITICAL: The agent relies heavily on this for tool selection.
    description: string;
    // The actual shell command to execute. Supports handlebar templating (e.g., `python scripts/process.py --input {{args.file}}`).
    command: string;
    // The execution environment context. 'system' uses the local host OS shell. 'remote_ssh' executes on a configured remote server.
    runtime: 'system' | 'node' | 'python' | 'docker' | 'remote_ssh';
    // Safety guardrail. 'always' pauses execution to ask the user for permission. Set to 'never' ONLY for harmless, read-only operations.
    confirmation: 'always' | 'never';
    // A strictly typed JSON schema of the arguments the LLM must provide to execute the command. Prevents hallucinated arguments.
    args: Record<string, {
        // The data type of the argument.
        type: 'string' | 'number' | 'boolean';
        // Instructions for the LLM on how to generate this specific argument.
        description: string;
        // Whether the tool will fail if this argument is omitted. Defaults to false if not specified.
        required?: boolean;
    }>;
}

/** * 4. WORKFLOW DEFINITION
 * File Pattern: .agent/workflows/*.md
 * Purpose: Defines multi-step, complex standard operating procedures (SOPs) for the agent to follow.
 */
interface WorkflowDefinition {
    // Identifies this asset as a workflow. Constraint: Must always be the exact string 'workflow'.
    type: 'workflow';
    // The human-readable title of the workflow. Should be action-oriented (e.g., 'Generate API Documentation').
    name: string;
    // The shortcut command the user types to trigger the workflow. Constraint: Must begin with a forward slash (e.g., '/docs').
    slug: `/${string}`;
    // A summary of the workflow's purpose so the Router agent knows when to suggest it to the user.
    description: string;
    // 'interactive' requires user approval between steps. 'autonomous' runs end-to-end. 'background' delegates to the Agent Manager for headless, asynchronous execution.
    mode: 'interactive' | 'autonomous' | 'background';
    // An array of expected tangible outputs the agent must generate before considering the workflow complete. Optional.
    expected_artifacts?: Array<'implementation_plan' | 'task_list' | 'code_diff' | 'walkthrough' | 'screenshot' | 'browser_recording'>;
    // Context resources to preload before starting. Can be file globs or other agent handles (e.g., '@QA_Agent').
    context: string[];
    // Instructions for what the agent should do or suggest immediately after the workflow succeeds.
    on_finish: string;
    // A schema for a UI form presented to the user to gather required variables before the workflow begins.
    inputs: Array<{
        // The variable name injected into the workflow context.
        name: string;
        // The data type, driving the UI input component (e.g., file picker vs text box).
        type: 'text' | 'string' | 'boolean' | 'file_path';
        // Help text shown to the user in the form. Optional.
        description?: string;
        // A pre-filled value for the form. Optional.
        default?: any;
        // Whether the user must provide this before starting. Defaults to true.
        required?: boolean;
    }>;
}

/** * 5. KNOWLEDGE DEFINITION
 * File Pattern: .agent/knowledge/*.md
 * Purpose: Configures custom Retrieval-Augmented Generation (RAG) indexes.
 */
interface KnowledgeDefinition {
    // The programmatic identifier for the RAG index. Constraint: Must be snake_case.
    name: string;
    // An array of URLs, file paths, or directories to scrape and ingest into the vector database.
    sources: string[];
    // How often the index should rebuild to capture changes.
    refresh_schedule: 'always' | 'daily' | 'weekly' | 'manual';
    // The chunking algorithm to use. 'code' respects semantic boundaries of functions/classes. 'prose' chunks by paragraphs/sections.
    strategy: 'code' | 'prose' | 'mixed';
    // Who or what can query this index. Can be an array of agent handles or a general visibility flag ('public'/'private').
    access: string[] | 'public' | 'private';
}

/** * 6. EVALUATION DEFINITION
 * File Pattern: .agent/evals/*.md
 * Purpose: Defines automated LLM-as-a-Judge test suites to verify agent behavior and output quality.
 */
interface EvaluationDefinition {
    // The human-readable name of the test suite.
    name: string;
    // The specific agent being tested. Constraint: Must be a valid agent handle starting with '@'.
    target_agent: `@${string}`;
    // The reasoning model assigned to evaluate the target agent. Instruction: Always use a high-tier reasoning model like 'gemini-3.1-pro' for judging.
    judge_model: 'claude-opus-4.6-thinking' | 'gemini-3.1-pro';
    // The minimum score required to pass the evaluation. Range: 0-100.
    pass_threshold: number;
    // An array of simulated user prompts or inputs to feed into the target agent during the test.
    scenarios: string[];
    // An array of strict grading criteria the judge model must use to score the target agent's responses.
    rubric: string[];
}

/** * 7. SKILL DEFINITION
 * File Pattern: .agent/skills/<skill-name>/SKILL.md
 * Purpose: Defines progressive disclosure capabilities that load dynamic tools, prompts, or scripts only when semantically relevant.
 */
interface SkillDefinition {
    // Identifies this asset as a skill. Constraint: Must always be the exact string 'skill'.
    type: 'skill';
    // The unique identifier for the skill bundle. Constraint: Must be kebab-case and match the parent directory name.
    name: string;
    // A highly descriptive explanation of what the skill allows the agent to do. CRITICAL: The router uses semantic vector matching on this string to load the skill dynamically.
    description: string;
    // Defines where the skill is installed. 'workspace' limits it to the current project. 'global' makes it available across all user projects.
    scope: 'workspace' | 'global';
}

/**
 * 8. KNOWLEDGE SOURCE DEFINITION
 * File Pattern: .agent/knowledge/sources/ ** / *.md
 * Purpose: Metadata for individual documents ingested into a knowledge index.
 */
interface KnowledgeSourceDefinition {
    // The structural classification of the document.
    archetype: 'concept' | 'protocol' | 'constraint' | 'pattern' | 'vocabulary' | 'context';
    // The current lifecycle state of the document. 'active' is preferred for RAG.
    status: 'draft' | 'review' | 'active' | 'deprecated';
    // Semantic versioning string (e.g., '1.0.0').
    version: string;
    // The date the source was initially added. Format: YYYY-MM-DD.
    created: string;
    // The date the source was last modified. Format: YYYY-MM-DD.
    updated: string;
    // An array of paths to other knowledge source files that must be understood prior to this one. Optional.
    requires?: string[];
    // An array of paths to tangentially related knowledge source files. Optional.
    related?: string[];
    // An array of string tags for metadata filtering during RAG retrieval. Optional.
    tags?: string[];
}

/**
 * 9. INDEX DEFINITION
 * File Pattern: .agent/knowledge/ ** /_index.md
 * Purpose: Defines the aggregation rules and context modes for a specific knowledge namespace.
 */
interface IndexDefinition {
    // Identifies this asset as an index configuration. Constraint: Must always be the exact string 'index'.
    archetype: 'index';
    // The lifecycle state of the index configuration.
    status: 'draft' | 'review' | 'active' | 'deprecated';
    // Semantic versioning string (e.g., '1.0.0').
    version: string;
    // Creation date. Format: YYYY-MM-DD.
    created: string;
    // Last modification date. Format: YYYY-MM-DD.
    updated: string;
    // The boundary constraint for this index (e.g., 'frontend', 'backend', 'system-design').
    scope: string;
    // Specific instructions on how the RAG pipeline should process files in this scope. Optional.
    index_policy?: string;
    // Rules for how files should be named or organized within this namespace. Optional.
    path_convention?: string;
    // The overarching project this index belongs to. Optional.
    project?: string;
    // Hints to the agent on how to apply the retrieved information (e.g., 'strict-compliance', 'creative-reference'). Optional.
    context_mode?: string;
}
