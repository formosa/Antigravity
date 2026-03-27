// Local SKILL.md contract reference for agent-create-issues-tracker

interface SkillDefinition {
    frontmatter: {
        name: string;
        description: string;
    };
    body_content: {
        when_to_use: string;
        how_to_use: string;
        constraints?: string;
        resources_reference?: string;
    };
}
