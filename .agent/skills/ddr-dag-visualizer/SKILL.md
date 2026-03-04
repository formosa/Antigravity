---
name: ddr-dag-visualizer
version: 2.0.0
description: Validates DDR YAML and generates deterministic SVG/PNG DAG artifacts plus validation reports.
---

<when_to_use>

- The user asks to visualize, validate, or inspect a DDR DAG from YAML.
- The user asks to audit DDR node/edge/tier integrity.
</when_to_use>

<how_to_use>

1. Confirm input YAML path and output directory (default `./ddr_output/`).
2. Verify prerequisites:
   - `python -m pip install -r .agent/skills/ddr-dag-visualizer/scripts/requirements.txt`
   - `dot -V`
3. Run pipeline:
   - `python .agent/skills/ddr-dag-visualizer/scripts/visualize.py <path_to_ddr.yaml> --output-dir <output_dir>`
4. Report generated files and print `validation_report.md` exactly.
5. If failure occurs, report stderr verbatim and run targeted checks:
   - Graphviz availability
   - YAML parse validity
   - missing `parent_ids` references

If input path is missing or unreadable, halt and request it.
</how_to_use>

<constraints>
- Never modify the source YAML unless explicitly instructed.
- Never paraphrase validation violations; quote the report.
- Use script output as source of truth.
- Keep responses concise and artifact-focused.
</constraints>

<resources_reference>

- `.agent/skills/ddr-dag-visualizer/scripts/requirements.txt`
- `.agent/skills/ddr-dag-visualizer/scripts/visualize.py`
- `.agent/skills/ddr-dag-visualizer/references/ddr_node_schema.yaml`
- `.agent/skills/ddr-dag-visualizer/references/output_schema.yaml`
</resources_reference>
