// issue.d.ts
// Antigravity Agent Asset Configuration Schema

/** ISSUE DEFINITION
 * File Pattern: DDR_v4_Issue-*.md
 * Purpose: Authoritative single source of truth for an individual identified issue, detailing its validation audit, proposed resolutions, and comparative analysis.
 */
interface IssueDefinition {
    /**
     * Standard YAML frontmatter defining the document metadata.
     */
    frontmatter: {
        document: {
            id: string;
            title: string;
            format_version: string;
            target_platform: string;
            subject: string;
            /** ISO 8601 Date format YYYY-MM-DD */
            created: string;
            status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
            severity: 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
            type: 'LOGICAL_CONFLICT' | 'DESIGN_INADEQUACY' | 'UNNECESSARY_COMPLEXITY' | 'AXIOM_VIOLATION' | 'SCHEMA_DEFECT' | 'MIGRATION_GAP' | 'LIFECYCLE_GAP';
            [key: string]: string | number | boolean;
        };
    };
    body_content: {
        /** Main title for the issue resolution strategy encoded as an h2 block. */
        main_header: string;

        /** Agent Context yaml block encoded at the top of the body immediately following its header */
        agent_context: {
            id: string;
            status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
            severity: 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
            type: 'LOGICAL_CONFLICT' | 'DESIGN_INADEQUACY' | 'UNNECESSARY_COMPLEXITY' | 'AXIOM_VIOLATION' | 'SCHEMA_DEFECT' | 'MIGRATION_GAP' | 'LIFECYCLE_GAP';
            tier_refs: string[];
            section_ref: string;
            rule_refs: string[];
        };

        /** Section containing the validation audit of the issue */
        validation_audit: {
            title: string;
            body_text: string;
            findings: string[];
        };

        /** Section containing suggested strategies for optimal resolution */
        suggested_strategies: {
            title: string;
            options: Array<{
                option_label: string;
                description: string;
                supporting_insights: string;
                citations: string;
            }>;
        };

        /** Section containing comparative analysis and recommended strategy */
        comparative_analysis: {
            title: string;
            analysis_body: string;
            endorsement_and_justification: string;
        };
    };
}
