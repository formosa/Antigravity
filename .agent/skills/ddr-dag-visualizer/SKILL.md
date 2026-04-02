---
name: ddr-dag-visualizer
version: 2.0.2
description: Validates DDR YAML and generates deterministic SVG and PNG DAG artifacts plus validation reports. Use when the task is to inspect DDR graph structure, render diagrams, or confirm node and edge integrity from YAML. Do not use when the task is limited to text-only spec edits without diagram or validation output.
---

<when_to_use>

- The user asks to visualize, validate, or inspect a DDR DAG from YAML.
- The user asks to audit DDR node/edge/tier integrity.
- Do not use this skill when the request is only to edit prose or schema text without generating validation or visualization artifacts.
- Example prompt: "Visualize ddr/ddr_system_v6.3.yaml and write the outputs to ddr/output."
- Example prompt: "Validate this DDR YAML and generate DAG diagrams plus a validation report."
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

- Read `.agent/skills/ddr-dag-visualizer/scripts/requirements.txt` to confirm the Python package prerequisites before first use.
- Run `.agent/skills/ddr-dag-visualizer/scripts/visualize.py` to generate the diagrams and validation reports.
- Read `.agent/skills/ddr-dag-visualizer/references/ddr_node_schema.yaml` to confirm the expected DDR node contract during troubleshooting.
- Read `.agent/skills/ddr-dag-visualizer/references/output_schema.yaml` to confirm the expected report and artifact output structure.
</resources_reference>
