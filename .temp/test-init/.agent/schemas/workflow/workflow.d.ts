// Base Workflow Asset Configuration Schema
interface WorkflowDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
    };
    body_content: {
        steps: string;
    };
}
