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

# DDR DAG Visualizer

## Goal

Produce publication-quality, multimodal-ready DAG visualizations and a
deterministic VERIFY validation report from any DDR System v4.0 YAML
definition file. Tier metadata (labels, optional tiers, merge nodes,
topology edges) is loaded dynamically from `tier_definitions` when present,
and falls back to hardcoded DDR v4.0 defaults for minimal project-instance
files. Every structural invariant in DDR v4.0 (§3.5, §6, §7) is enforced
by the validation script — the LLM does not interpret rules; the script does.

## Prerequisites — Run Once

Before first use, verify system dependencies are installed:

```bash
python -m pip install -r scripts/requirements.txt
```

Graphviz system binary is **required**. Install if absent:

- macOS:   `brew install graphviz`
- Ubuntu:  `sudo apt-get install graphviz`
- Windows: `winget install graphviz` (or <https://graphviz.org/download/>)

Verify: `dot -V`

## Accepted Input File Types

| File Type             | Contents                                                                                                  | Example                       |
| --------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **System-definition** | Full DDR spec: tier_definitions, axioms, operations, extension_catalog, nodes, and all normative sections | `ddr_system_v4.0.yaml`        |
| **Project-instance**  | Minimal: ddr_version, active_tiers, nodes                                                                 | Any project-specific DDR file |

Both types are accepted without any modification to the command.

## Instructions

1. **Identify the DDR YAML file.** Ask the user for the path to their DDR
   YAML file if not already provided. The file must conform to the schema
   defined in `references/ddr_node_schema.yaml`.

2. **Determine output directory.** Default to `./ddr_output/` unless the
   user specifies otherwise.

3. **Run the visualization pipeline.** Execute:

```bash
   python scripts/visualize.py <path_to_ddr.yaml> --output-dir <output_dir>
```

1. **Report results to the user.** After execution, list the generated
   files from stdout and display the contents of `validation_report.md`.
   - CRITICAL: Do NOT interpret or paraphrase validation violations.
     Report them exactly as written in `validation_report.md`.
   - CRITICAL: Do NOT modify the YAML file autonomously based on
     violations. Present findings; await explicit user instruction before
     any edits.

2. **Handle errors.** If the script exits with a non-zero code:
   - Check that Graphviz binary is installed (`dot -V`).
   - Check YAML syntax: `python -c "import yaml; yaml.safe_load(open('<path>'))"`.
   - Check that all `parent_ids` reference node IDs that exist in the file.
   - Report the specific error message from stderr verbatim.

## Output Files

| File                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `ddr_dag_full.svg`       | Complete DAG: tier clusters, nodes, edges, legend |
| `ddr_dag_full.png`       | Same at 300 DPI raster                            |
| `ddr_dag_tiers.svg`      | Tier topology overview (no individual nodes)      |
| `validation_report.md`   | Human-readable VERIFY output                      |
| `validation_report.json` | Machine-readable VERIFY output                    |

## Constraints

- NEVER run DELETE, MODIFY, or INSERT operations on the YAML file without
  explicit user confirmation of each change.
- NEVER assume a validation violation is a false positive. Report all
  violations. The rules are defined in DDR v4.0 §2–§7.
- If the YAML file contains no nodes, generate the tier topology diagram
  only and note that no nodes were found.
- Run scripts only — do not attempt to rewrite visualization logic inline.

## Example

User: "Visualize my DDR structure from ddr_system_v4.0.yaml"

Agent:

1. Runs: `python scripts/visualize.py ddr_system_v4.0.yaml --output-dir ./ddr_output/`
2. Opens `ddr_output/validation_report.md`
3. Reports: "Visualization complete. 5 files generated in ./ddr_output/.
   Validation status: CLEAN — no violations detected."
