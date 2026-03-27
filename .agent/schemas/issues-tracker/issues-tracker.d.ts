// issues-tracker.d.ts
// Canonical Issues Tracker contract for blank initialization and populated trackers
// generated from the lean v6-style format used by agent-create-issues-tracker.

type IssueStatus = 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
type IssueSeverity = 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';
type IssueType =
    | 'LOGICAL_CONFLICT'
    | 'DESIGN_INADEQUACY'
    | 'UNNECESSARY_COMPLEXITY'
    | 'AXIOM_VIOLATION'
    | 'SCHEMA_DEFECT'
    | 'MIGRATION_GAP'
    | 'LIFECYCLE_GAP';

/**
 * This file documents the current canonical format.
 * Legacy v4/v5 validation is handled by the validator and is intentionally not the
 * generation target represented by this interface.
 */
interface CanonicalIssuesTrackerDefinition {
    document_metadata: {
        id: string;
        title: string;
        format_version: 'IT-1.0';
        target_platform: string;
        target_model: string;
        subject: string;
        /** ISO 8601 date string: YYYY-MM-DD */
        created: string;
        /** ISO 8601 date string: YYYY-MM-DD */
        last_modified: string;
        author: string;
        open_issues: number;
        resolved_issues: number;
        status_values: IssueStatus[];
        severity_values: IssueSeverity[];
        type_values: IssueType[];
    };
    issue_schema_markdown: string;
    /**
     * A blank initialized tracker contains exactly one empty row in this table and zero issue
     * entries. Populated trackers replace the empty row with real issue rows.
     */
    issue_registry_rows: Array<{
        id: string;
        severity: IssueSeverity;
        type: IssueType;
        status: IssueStatus;
        tiers_affected: string;
        title: string;
    }>;
    issues: CanonicalIssueEntry[];
    resolution_workflow_markdown: string;
    cross_issue_dependency_map: Array<{
        issue: string;
        depends_on: string;
        nature_of_dependency: string;
    }>;
    footer_summary: {
        total_issues: number;
        resolved_issues: number;
        /** ISO 8601 date string: YYYY-MM-DD */
        last_updated: string;
    };
}

interface CanonicalIssueEntry {
    issue_id: string;
    title: string;
    status: IssueStatus;
    severity: IssueSeverity;
    type: IssueType;
    tiers_affected: string;
    spec_section: string;
    /** Optional one-line note inserted when a resolved issue records its chosen fix. */
    resolution_note?: string;
    problem_statement: string;
    evidence_and_justification: string;
    impact_assessment: string;
    resolution_a: string;
    resolution_b: string;
    notes: string;
}
