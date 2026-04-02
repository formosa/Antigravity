// Antigravity Agent Asset Configuration Schema
// OPTIMIZED FOR DIRECTORY-LEVEL AGENT ASSET INDEX DOCUMENTS
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict structure for Markdown index assets that summarize and route to other agent assets in sibling directories.

/** ASSET DIRECTORY INDEX DEFINITION
 * File Pattern: .agent/<asset-directory>/index.md
 * Purpose: Provides a deterministic, machine-readable and human-readable registry for the assets contained in a specific directory such as tools, skills, workflows, or rules.
 */
interface AssetDirectoryIndexDefinition {
    /**
     * No YAML frontmatter is used.
     * The header is encoded as:
     * 1. A required H1 title.
     * 2. A required blockquote preamble containing compact routing metadata.
     */
    document_header: {
        /** Required H1 title (for example: `# Agent Tools Index`). */
        title: string;
        /** First blockquote statement summarizing the directory registry. */
        summary: string;
        /** Optional blockquote line clarifying intended use or scan scope. */
        scope?: string;
        /** Required total count for the indexed asset type. */
        total_assets: number;
        /** Optional markdown link to the logical parent directory. */
        parent?: string;
        /** Required conflict-resolution rule pointing back to the authoritative asset definitions. */
        authority_rule: string;
    };
    body_content: {
        /**
         * Required ordered guidance section, typically headed `## Use This Index`.
         * Must be encoded as a numbered Markdown list defining the intended scan order.
         */
        use_this_index: string;
        /**
         * Required discovery section, typically headed `## Selection Map`.
         * Each bullet must identify one asset id and a concise intent-oriented selection hint.
         */
        selection_map: Array<{
            /** Canonical asset identifier, usually wrapped as inline code in the markdown source. */
            id: string;
            /** One-line selection guidance for first-pass routing. */
            selection_hint: string;
        }>;
        /**
         * Required manifest section encoded as a fenced YAML block.
         * The root key should name the asset collection being indexed (for example: `tools`, `skills`, `rules`).
         */
        manifest: {
            /** Must be `yaml` for deterministic fenced-block parsing. */
            fence_language: "yaml";
            /** Collection key for the manifest entries. */
            root_key: string;
            /** Ordered manifest entries. Record order should match the later detailed record order. */
            entries: AssetDirectoryManifestEntry[];
        };
        /**
         * Required detailed records section.
         * The markdown heading may vary by asset type (for example: `## Tool Records`, `## Skill Records`).
         */
        detailed_records: {
            /** Section heading label as rendered in the document. */
            section_heading: string;
            /** One subsection per indexed asset, typically encoded with H3 headings. */
            records: AssetDirectoryRecord[];
        };
        /** Required flat category/count summary for quick aggregate scanning. */
        category_totals: Array<{
            category: string;
            count: number;
        }>;
        /** Required boundary rules stating what the index does not authoritatively define. */
        index_boundaries: string[];
    };
}

interface AssetDirectoryManifestEntry {
    /** Canonical asset identifier. */
    id: string;
    /** Repo-relative path to the authoritative asset definition. */
    definition?: string;
    /** Stable grouping label used for counts and filtering. */
    category?: string;
    /** Runtime or execution environment when relevant to the asset type. */
    runtime?: string;
    /** Confirmation policy when relevant to the asset type. */
    confirmation?: string;
    /** Summary of accepted tool or command arguments when relevant. */
    tool_args?: string;
    /**
     * Direct CLI flags or equivalent execution modifiers.
     * Use `none` when the asset exposes no direct flags.
     */
    direct_cli_flags?: string[] | string;
    /** Indicates whether downstream workflows must capture the primary output. */
    output_capture_required?: boolean;
    /** Safety posture for side-effectful assets. */
    destructive_capability?: "none" | "conditional" | "always";
    /** Primary emitted files, stdout artifacts, or other material outputs. */
    primary_outputs?: string[];
    /** Primary writes or other externally visible side effects. */
    primary_side_effects?: string[];
    /** Repo-relative implementation path or explanatory source note. */
    implementation?: string;
    /** Search-oriented synonyms or tags for semantic routing. */
    keywords?: string[];
    /** Intent-oriented criteria for when the asset should be selected. */
    use_when?: string[];
    /**
     * Permits additional asset-specific scalar or list metadata without forcing schema churn.
     * Keep additional fields explicit in the markdown manifest; do not use nested free-form objects.
     */
    [key: string]: string | number | boolean | string[] | undefined;
}

interface AssetDirectoryRecord {
    /** Canonical asset identifier represented by the subsection heading. */
    id: string;
    /** Repo-relative path to the authoritative asset definition, when one exists. */
    definition?: string;
    /** Repo-relative implementation path or explanatory implementation note. */
    implementation?: string;
    /** Concise statement of the asset's best-fit purpose. */
    best_used_for?: string;
    /** Flat notes about accepted inputs or invocation assumptions. */
    input_notes?: string[];
    /** Flat notes about outputs, generated artifacts, or emitted values. */
    output_notes?: string[];
    /** Flat notes about validation steps or post-run checks. */
    post_run_checks?: string[];
    /** Flat safety rules or operational guardrails. */
    safety_contract?: string[];
    /** Guidance on when the reader must defer to the linked authoritative definition. */
    open_definition_when?: string;
}
