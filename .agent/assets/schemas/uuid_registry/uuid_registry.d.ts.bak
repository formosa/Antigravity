// schema.d.ts
// Antigravity Agent Asset Configuration Schema (v1.18.3)
// OPTIMIZED FOR GEMINI 3.1 PRO

/** UUID REGISTRY DEFINITION
 * File Pattern: uuid_registry/*.json
 * Purpose: Authoritative single source of truth for all identified UUIDs for database primary keys, distributed systems, and entity tracking.
 */
interface UUIDRegistry {
    /**
     * The registry maps a UUID formatted string to its metadata.
     * Pattern: ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
     */
    [uuid: string]: {
        /** The UUID version used (4 for random, 7 for time-ordered). */
        version: 4 | 7;
        /** True if the ID contains a sortable timestamp (v7), false if opaque (v4). */
        is_sortable: boolean;
        /** Semantic context for the Agent to understand why this ID exists. */
        purpose: string;
        /** ISO 8601 timestamp of generation. */
        created_at: string;
        /** Method used to ensure cryptographic security. Default is CSPRNG */
        entropy_source?: string;
        /** The workspace file or resource this UUID is mapped to. */
        linked_entity?: string;
    };
}
