---
name: create-ddr-system-doc
version: 1.0.2
description: Generates authoritative DDR System Markdown documentation from a DDR schema YAML plus DDR system specification YAML. Use when the task is to create, regenerate, or validate a comprehensive `DDR System(vX).md` document from authoritative DDR source files. Do not use when the task is to revise the source schema or semantic authority directly.
---

<when_to_use>

- The user provides a DDR System schema file and a DDR System specification file and asks for a documentation artifact.
- The user asks to regenerate, standardize, or validate a `DDR System(vX).md` document from DDR YAML sources.
- The task requires deterministic conversion of DDR rule catalogs, tier definitions, lifecycle rules, extensions, and topology into a single Markdown reference document.
- Do not use this skill when the user wants to patch the source YAML authorities rather than generate documentation from them.
- Example prompt: "Generate DDR System(v6.3).md from ddr/ddr_node_schema_v6.3.yaml and ddr/ddr_system_v6.3.yaml."
- Example prompt: "Regenerate the DDR system document from the current schema/spec pair and validate the result."
</when_to_use>

<how_to_use>

1. Resolve parameters before writing anything:
   - Required: `SCHEMA_PATH`, `SPEC_PATH`
   - Optional: `OUTPUT_PATH`
   - Optional: `OVERWRITE_EXISTING` (default `false`)
2. Run pre-flight checks in this order:
   - If either required path is missing or unreadable, halt and return `RFQ` naming the missing or unreadable path.
   - If `OUTPUT_PATH` is omitted, default to a sibling of `SPEC_PATH` named `DDR System(v<ddr_version>).md`.
   - If the target output already exists and overwrite was not explicitly requested, halt and return `RFQ` requesting overwrite approval.
3. Use the deterministic generator first:
   - `python .agent/skills/create-ddr-system-doc/scripts/build_ddr_system_doc.py <SCHEMA_PATH> <SPEC_PATH> --output <OUTPUT_PATH>`
   - Add `--overwrite` only when explicit overwrite approval exists.
4. Validate the generated artifact immediately:
   - `python .agent/skills/create-ddr-system-doc/scripts/validate_ddr_system_doc.py <OUTPUT_PATH> --spec <SPEC_PATH>`
5. If generation or validation fails:
   - Report the exact validator or schema-validation error.
   - Do not freehand missing rules, statuses, or semantics.
   - Do not modify the source schema or source specification unless the user explicitly asks for source edits.
6. Use the bundled references only when manual review or extension is needed:
   - Read `.agent/skills/create-ddr-system-doc/resources/reference.md` for source-precedence and fidelity rules.
   - Read `.agent/skills/create-ddr-system-doc/resources/output-blueprint.md` for the canonical section map and output contract.
7. Return one concise success line with the written output path after the validator passes.

Reference example:

- `python .agent/skills/create-ddr-system-doc/scripts/build_ddr_system_doc.py .agent/assets/proposals/processed/v6.1/ddr_node_schema.yaml .agent/assets/proposals/processed/v6.1/ddr_system_v6.1.yaml --output ".agent/assets/proposals/processed/v6.1/DDR System(v6.1).md" --overwrite`
</how_to_use>

<constraints>

- Do not invent rule IDs, lifecycle transitions, extension contracts, or tier semantics that are not present in the source artifacts.
- Do not silently continue when the specification fails schema validation.
- Do not overwrite an existing documentation file without explicit approval.
- Do not modify the source schema or specification while generating documentation.
- Do not drop optional sections that are present in the specification; document them or explicitly surface why generation failed.
- Preserve source terminology exactly for statuses, operation names, rule IDs, extension IDs, and tier IDs.
</constraints>

<resources_reference>

- Run `.agent/skills/create-ddr-system-doc/scripts/build_ddr_system_doc.py` to generate the documentation artifact from the source YAML files.
- Run `.agent/skills/create-ddr-system-doc/scripts/validate_ddr_system_doc.py` to validate the generated Markdown against the source specification.
- Read `.agent/skills/create-ddr-system-doc/resources/reference.md` to preserve source-precedence and fidelity rules during manual review.
- Read `.agent/skills/create-ddr-system-doc/resources/output-blueprint.md` to preserve the canonical section map and output contract.
</resources_reference>
