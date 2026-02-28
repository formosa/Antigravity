---
name: ddr-dag-visualizer
description: >
  Generates high-quality SVG/PNG DAG visualizations and a structural
  validation report for any DDR System v4.0 YAML definition file. Accepts
  both system-definition files (containing the full DDR specification
  including tier_definitions, axioms, operations, and extension_catalog,
  such as ddr_system_v4.0.yaml) and project-instance files (containing
  ddr_version, active_tiers, and nodes for a specific software project).
  Use this skill when the user asks to visualize, diagram, render, audit,
  validate, inspect, or review the structure of a DDR System DAG, or when
  they reference a .yaml or .yml file containing DDR tiers, nodes,
  parent_ids, edges, tier_definitions, or axioms. Also use when the user
  asks to check or verify their DDR structure.
---

<when_to_use>

- The user asks to visualize, diagram, render, audit, validate, inspect, or review the structure of a DDR System DAG.
- The user references a .yaml or .yml file containing DDR tiers, nodes, parent_ids, edges, tier_definitions, or axioms.
- The user asks to check or verify their DDR structure.
</when_to_use>

<how_to_use>

1. **Context Verification (Silent):** Determine the input file type (System-definition or Project-instance). Both types are accepted.
2. **Prerequisites Check:** Before first use, verify system dependencies are installed: `python -m pip install -r scripts/requirements.txt`. Graphviz is also required (`dot -V`). Install via `winget install graphviz` (Windows), `brew install graphviz` (macOS), or `sudo apt-get install graphviz` (Ubuntu) if absent.
3. **Identify the DDR YAML file:** Ask the user for the path to their DDR YAML file if not already provided. The file must conform to the schema defined in `references/ddr_node_schema.yaml`.
4. **Determine output directory:** Default to `./ddr_output/` unless the user specifies otherwise.
5. **Run the visualization pipeline:** Execute `python scripts/visualize.py <path_to_ddr.yaml> --output-dir <output_dir>`.
6. **Report results to the user:** After execution, list the generated files (`ddr_dag_full.svg`, `ddr_dag_full.png`, `ddr_dag_tiers.svg`, `validation_report.md`, `validation_report.json`) from stdout and display the contents of `validation_report.md` to the user.
    - CRITICAL: Do NOT interpret or paraphrase validation violations. Report them exactly as written in `validation_report.md`.
    - CRITICAL: Do NOT modify the YAML file autonomously based on violations. Present findings; await explicit user instruction before any edits.
7. **Handle errors:** If the script exits with a non-zero code:
    - Check that Graphviz binary is installed (`dot -V`).
    - Check YAML syntax: `python -c "import yaml; yaml.safe_load(open('<path>'))"`.
    - Check that all `parent_ids` reference node IDs that exist in the file.
    - Report the specific error message from stderr verbatim.
</how_to_use>

<constraints>
- NEVER run DELETE, MODIFY, or INSERT operations on the YAML file without explicit user confirmation of each change.
- NEVER assume a validation violation is a false positive. Report all violations. The rules are defined in DDR v4.0 §2–§7. Every structural invariant in DDR v4.0 is enforced by the validation script — the LLM does not interpret rules; the script does.
- If the YAML file contains no nodes, generate the tier topology diagram only and note that no nodes were found.
- Run scripts only — do not attempt to rewrite visualization logic inline.
- Never use generic Markdown headers for execution steps. All operational directives must reside within XML fenced blocks.
- Do not include explanatory conversational text outside of the XML blocks.
</constraints>

<resources_reference>

- `scripts/requirements.txt`
- `scripts/visualize.py`
- `references/ddr_node_schema.yaml`
</resources_reference>
