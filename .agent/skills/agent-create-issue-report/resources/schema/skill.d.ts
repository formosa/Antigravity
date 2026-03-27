// issue-report.d.ts
// Canonical Resolution Report contract used by agent-create-issue-report.

type IssueStatus = 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'WONT_FIX' | 'DEFERRED';
type IssueSeverity = 'CRITICAL' | 'MAJOR' | 'MODERATE' | 'MINOR';

interface ResolutionOption {
    label: string;
    description: string;
    supporting_insights: string;
    citations: string;
}

/**
 * Current generation target.
 * Legacy v4/v5 reports remain valid repository artifacts but are intentionally not represented
 * as the primary output contract here.
 */
interface CanonicalIssueReportDefinition {
    document: {
        id: string;
        title: string;
        format_version: 'IT-1.0';
        target_platform: string;
        target_model: string;
        subject: string;
        /** ISO 8601 date string: YYYY-MM-DD */
        created: string;
        /** ISO 8601 date string: YYYY-MM-DD */
        updated: string;
        /** Present only when status is RESOLVED. */
        resolved?: string;
        status: IssueStatus;
        severity: IssueSeverity | string;
        type: string;
    };
    agent_context: {
        id: string;
        status: IssueStatus;
        severity: IssueSeverity | string;
        type: string;
        tier_refs: string[];
        section_ref: string;
        rule_refs: string[];
        /** ISO 8601 date string: YYYY-MM-DD */
        updated: string;
        /** Present only when status is RESOLVED. */
        resolved?: string;
    };
    resolution_callout?: string;
    validation_audit: {
        source_summary: string;
        narrative: string;
        findings: [string, string, ...string[]];
    };
    strategies: {
        option_a: ResolutionOption;
        option_b: ResolutionOption;
    };
    comparative_analysis: {
        tradeoffs: [string, string, ...string[]];
        recommended_option: 'Option A' | 'Option B';
        endorsement_rationale: string;
        justifications: [string, string, string, ...string[]];
    };
    implementation_note: string;
}
