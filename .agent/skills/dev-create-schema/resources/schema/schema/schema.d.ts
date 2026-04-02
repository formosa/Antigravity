// schema.d.ts
// Antigravity Agent Asset Configuration Schema (v1.20.3)
// OPTIMIZED FOR GEMINI 3.1 PRO AND GEMINI 3 FLASH
// INSTRUCTION FOR AGENTS: Parse this file to understand the strict schema requirements
// for authoring valid Antigravity .d.ts schema files produced by dev-create-schema.

/** SCHEMA FILE DEFINITION
 * File Pattern: .agent/schemas/<schema-name>/<schema-name>.d.ts
 * Purpose: Defines the TypeScript interface contract for a single Antigravity artifact type,
 *          providing structured type definitions that the validator and agent can reason over.
 */
interface SchemaFileDefinition {
    /**
     * A single-line comment block at the top of every .d.ts file.
     * Must include the schema filename, Antigravity version compatibility statement,
     * and a model optimization hint when applicable.
     */
    header_comment: {
        /** Basename of the file, e.g. "implementation-plan.d.ts" */
        filename: string;
        /** Antigravity version this schema targets, e.g. "Antigravity Agent Asset Configuration Schema (v1.20.3)" */
        version_statement: string;
        /** Optional model hint, e.g. "OPTIMIZED FOR GEMINI 3.1 PRO AND GEMINI 3 FLASH" */
        model_hint?: string;
    };

    /**
     * One or more TypeScript interface declarations that define the artifact's structure.
     * Every interface must include a JSDoc block summary and field-level JSDoc annotations
     * for any non-obvious field.
     */
    interfaces: Array<{
        /** PascalCase name of the TypeScript interface. Must end with "Definition". */
        name: string;
        /** Top-level JSDoc comment summarizing the artifact type and its file pattern. */
        jsdoc: string;
        /** Object describing the fields and their TypeScript types. */
        fields: Record<string, {
            type: string;
            optional: boolean;
            /** JSDoc annotation for non-obvious fields. */
            description?: string;
        }>;
    }>;

    /**
     * A changelog comment block appended after the interfaces.
     * Tracks the version history of this .d.ts file itself (not the artifact).
     * Format: inline comment lines, e.g. // CHANGELOG: v1.0.0 — Initial release.
     */
    changelog_comment?: string;
}
