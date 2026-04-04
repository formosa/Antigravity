{
    "$schema": "http://json-schema.org",
    "title": "Antigravity UUID Registry",
    "type": "object",
    "patternProperties": {
        "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$": {
            "type": "object",
            "properties": {
                "version": {
                    "type": "integer",
                    "enum": [
                        4,
                        7
                    ],
                    "description": "The UUID version used (4 for random, 7 for time-ordered)."
                },
                "is_sortable": {
                    "type": "boolean",
                    "description": "True if the ID contains a sortable timestamp (v7), false if opaque (v4)."
                },
                "purpose": {
                    "type": "string",
                    "description": "Semantic context for the Agent to understand why this ID exists."
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "ISO 8601 timestamp of generation."
                },
                "entropy_source": {
                    "type": "string",
                    "default": "CSPRNG",
                    "description": "Method used to ensure cryptographic security."
                },
                "linked_entity": {
                    "type": "string",
                    "description": "The workspace file or resource this UUID is mapped to."
                }
            },
            "required": [
                "version",
                "is_sortable",
                "purpose",
                "created_at"
            ]
        }
    }
}
