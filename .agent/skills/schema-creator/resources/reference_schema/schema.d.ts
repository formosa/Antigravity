// issues-tracker.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** ISSUES TRACKER DEFINITION
 * File Pattern: DDR_v4_Issues_Tracker.md or issues-tracker/*.md
 * Purpose: Authoritative single source of truth for all identified issues with DDR System Specifications.
 */
interface IssuesTrackerDefinition {
    /**
     * Encoded as an HTML comment block at the top of the file: `<!-- AGENT PARSING HEADER ... -->`
     * Note: This deviates from standard YAML frontmatter to prevent rendering in standard markdown readers.
     */
    frontmatter: {
        skill: string;
        version: string;
        target_agent: string;
        platform: string;
        context_mode: string;
        schema_version: string;
        document_type: string;
        subject_system: string;
        subject_file: string;
        last_updated: string;
        total_issues: number;
        open_issues: number;
        resolved_issues: number;
        load_trigger: string;
        [key: string]: any;
    };
    body_content: {
        /** Encoded as a YAML block ```yaml inside the ## DOCUMENT METADATA section. */
        document_metadata: {
            id: string;
            title: string;
            format_version: string;
            target_platform: string;
            target_model: string;
            subject: string;
            created: string;
            /** ISO 8601 Date format YYYY-MM-DD */
            last_modified: string;
            author: string;
            status_values: string[];
            severity_values: string[];
            type_values: string[];
        };
        /** Raw markdown text defining the expected schema. */
        issue_schema: string;
        /** Markdown table serving as the primary index of all issues. Maintains sort order by severity then issue number. */
        issue_registry: string;
        /** Collection of discrete issues, demarcated by `### ISSUE-[NNN]:` headers. */
        issues: Array<{
            issue_id: string;
            title: string;
            /** Parsed from the `<!-- AGENT_CONTEXT ... -->` block within the issue section. */
            agent_context: {
                id: string;
                status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
                severity: 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
                /** Constrained to exact values defined in document_metadata.type_values */
                type: 'LOGICAL_CONFLICT' | 'DESIGN_INADEQUACY' | 'UNNECESSARY_COMPLEXITY' | 'AXIOM_VIOLATION' | 'SCHEMA_DEFECT' | 'MIGRATION_GAP' | 'LIFECYCLE_GAP';
                tier_refs: string[];
                section_ref: string;
                rule_refs: string[];
                /** ISO 8601 Date format YYYY-MM-DD */
                created: string;
                /** ISO 8601 Date format YYYY-MM-DD */
                updated: string;
                resolved: string | null;
            };
            problem_statement: string;
            evidence_and_justification: string;
            impact_assessment: string;
            resolutions: Array<{
                option_label: string;
                description: string;
            }>;
            notes?: string;
        }>;
    };
}
