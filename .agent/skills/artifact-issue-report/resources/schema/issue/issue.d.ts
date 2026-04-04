// issue.d.ts
// Antigravity Agent Asset Configuration Schema

/**
 * ISSUE DEFINITION
 * File Pattern: any repo-relative `Issue-*.md` artifact path
 * Purpose: Authoritative single source of truth for an individual issue-resolution artifact.
 *
 * Current generation target:
 * - canonical two-option issue reports with an explicit implementation note
 *
 * Historical compatibility:
 * - legacy v4/v5 issue reports remain valid repository artifacts for read-only validation
 *   and first-write migration, but they are not generation targets.
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
            target_model: string;
            subject: string;
            /** ISO 8601 Date format YYYY-MM-DD */
            created: string;
            /** ISO 8601 Date format YYYY-MM-DD */
            updated: string;
            /** Present only when the issue status is RESOLVED. */
            resolved?: string;
            status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
            severity: 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
            type: 'LOGICAL_CONFLICT' | 'DESIGN_INADEQUACY' | 'UNNECESSARY_COMPLEXITY' | 'AXIOM_VIOLATION' | 'SCHEMA_DEFECT' | 'MIGRATION_GAP' | 'LIFECYCLE_GAP';
            [key: string]: string | number | boolean | undefined;
        };
    };
    body_content: {
        /** Main title for the issue resolution strategy encoded as an h2 block. */
        main_header: string;

        /** Agent Context YAML block encoded at the top of the body immediately following its header. */
        agent_context: {
            id: string;
            status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
            severity: 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
            type: 'LOGICAL_CONFLICT' | 'DESIGN_INADEQUACY' | 'UNNECESSARY_COMPLEXITY' | 'AXIOM_VIOLATION' | 'SCHEMA_DEFECT' | 'MIGRATION_GAP' | 'LIFECYCLE_GAP';
            tier_refs: string[];
            section_ref: string;
            rule_refs: string[];
            updated: string;
            /** Present only when the issue status is RESOLVED. */
            resolved?: string;
        };

        /** Optional preserved tracker resolution callout retained only when the tracker provides one. */
        resolution_callout?: string;

        /** Section containing the validation audit of the issue. */
        validation_audit: {
            title: string;
            body_text: string;
            findings: string[];
        };

        /** Section containing exactly two canonical suggested strategies. */
        suggested_strategies: {
            title: string;
            option_a: {
                option_label: string;
                description: string;
                supporting_insights: string;
                citations: string;
            };
            option_b: {
                option_label: string;
                description: string;
                supporting_insights: string;
                citations: string;
            };
        };

        /** Section containing the comparative analysis and endorsement rationale. */
        comparative_analysis: {
            title: string;
            analysis_body: string;
            endorsement_and_justification: string;
            recommendation_summary: string[];
        };

        /** Required implementation note describing either pending or resolved implementation state. */
        implementation_note: {
            title: string;
            body_text: string;
        };
    };
}
