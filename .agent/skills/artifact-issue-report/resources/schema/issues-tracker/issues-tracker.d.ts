// issues-tracker.d.ts
// Shared Issues Tracker contracts managed by artifact-issue-tracker across blank
// initialization (`IT-1.0`) and populated maintenance updates (`IT-1.1`).

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
type IssuesTrackerFormatVersion = 'IT-1.0' | 'IT-1.1';
type RecommendedOption = 'A' | 'B' | 'C';

interface IssueRegistryRow {
    id: string;
    severity: IssueSeverity;
    type: IssueType;
    status: IssueStatus;
    tiers_affected: string;
    title: string;
}

interface CrossIssueDependencyRow {
    issue: string;
    depends_on: string;
    nature_of_dependency: string;
}

interface FooterSummary {
    total_issues: number;
    resolved_issues: number;
    /** ISO 8601 date string: YYYY-MM-DD */
    last_updated: string;
}

interface BaseIssuesTrackerDefinition {
    document_metadata: {
        id: string;
        title: string;
        format_version: IssuesTrackerFormatVersion;
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
    issue_registry_rows: IssueRegistryRow[];
    resolution_workflow_markdown: string;
    cross_issue_dependency_map: CrossIssueDependencyRow[];
    footer_summary: FooterSummary;
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

interface Citation {
    label: string;
    url: string;
    relevance_note: string;
}

interface UpdatedIssueEntry extends CanonicalIssueEntry {
    resolution_c: string;
    comparative_analysis: string;
    recommendation: {
        endorsed_option: RecommendedOption;
        justification: string;
    };
    supporting_citations: Citation[];
}

/**
 * Blank initialization contract used by artifact-issue-tracker when creating new tracker
 * artifacts.
 */
interface CanonicalIssuesTrackerDefinition extends BaseIssuesTrackerDefinition {
    document_metadata: BaseIssuesTrackerDefinition['document_metadata'] & {
        format_version: 'IT-1.0';
    };
    /**
     * A blank initialized tracker contains exactly one empty row in this table and zero issue
     * entries. Populated trackers replace the empty row with real issue rows.
     */
    issue_registry_rows: IssueRegistryRow[];
    issues: CanonicalIssueEntry[];
}

/**
 * Populated maintenance contract used by artifact-issue-tracker after an existing tracker is
 * migrated in place.
 */
interface UpdatedIssuesTrackerDefinition extends BaseIssuesTrackerDefinition {
    document_metadata: BaseIssuesTrackerDefinition['document_metadata'] & {
        format_version: 'IT-1.1';
    };
    issues: UpdatedIssueEntry[];
}

type AnyIssuesTrackerDefinition =
    | CanonicalIssuesTrackerDefinition
    | UpdatedIssuesTrackerDefinition;
