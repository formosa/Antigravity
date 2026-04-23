// Base Rule Asset Configuration Schema
interface RuleDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
        trigger: "glob" | "regex" | "always" | "never" | "event";
        globs?: string | string[];
        priority: "critical" | "high" | "standard" | "low";
        execution_tier?: "standard" | "heavy";
    };
    body_content: {
        constraints: string;
        verification_step?: string;
    };
}
