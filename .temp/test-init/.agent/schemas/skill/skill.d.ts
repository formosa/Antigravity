// Base Skill Asset Configuration Schema
interface SkillDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
    };
    body_content: {
        when_to_use: string;
        how_to_use: string;
        constraints: string;
        resources_reference: string;
    };
}
