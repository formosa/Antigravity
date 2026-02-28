"""
DDR System v4.0 - DAG Visualization Pipeline.

Generates publication-quality SVG and PNG DAG diagrams from a DDR System
YAML definition file using the Graphviz DOT engine.

Supports both file types:
  - System-definition files (e.g. ddr_system_v4.0.yaml): tier_definitions
    are read dynamically to build tier labels, layer labels, core question
    annotations, optional/merge/terminal tier markers, and topology edges.
  - Project-instance files: falls back to hardcoded DDR v4.0 defaults for
    all tier metadata. Graph topology is derived from parent_ids in nodes.

Color palette mirrors the DDR v4.0 specification Mermaid diagram (§10)
adapted for white-background rendering.

Usage
-----
python visualize.py <ddr_yaml_file> [--output-dir <path>]

Requirements
------------
- Python packages: see requirements.txt
- System binary: Graphviz (dot must be on PATH)
  Install: brew install graphviz | apt install graphviz | winget install graphviz
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import graphviz
import yaml

_SCRIPT_DIR = Path(__file__).parent
_ASSETS_DIR = _SCRIPT_DIR.parent / "assets"

sys.path.insert(0, str(_SCRIPT_DIR))
from validate import (
    TIER_ORDER,
    TIER_SKIP_EXCEPTIONS,
    build_graph,
    generate_report,
    load_ddr_yaml,
    verify,
    _extract_tier_metadata,
)


# ---------------------------------------------------------------------------
# Hardcoded DDR v4.0 defaults (used when tier_definitions is absent)
# ---------------------------------------------------------------------------

_TIER_LABELS_DEFAULT: dict[str, str] = {
    "XPD":  "Existential Purpose Document",
    "SIL":  "Strategic Intent Layer",
    "GPCL": "Governance, Policy & Quality Layer",
    "FCL":  "Functional Capability Layer",
    "CL":   "Constraint Layer",
    "SAL":  "System Architecture Layer",
    "ICL":  "Interface & Contracts Layer",
    "CDL":  "Component Design Layer",
    "ISL":  "Implementation Scaffold Layer",
}

_LAYER_LABELS_DEFAULT: dict[str, str] = {
    "XPD":  "OPTIONAL ROOT",
    "SIL":  "INTENT LAYER",
    "GPCL": "GOVERNANCE LAYER",
    "FCL":  "FUNCTIONAL LAYER",
    "CL":   "CONSTRAINT LAYER",
    "SAL":  "ARCHITECTURE LAYER",
    "ICL":  "CONTRACT LAYER",
    "CDL":  "DESIGN LAYER",
    "ISL":  "SCAFFOLD LAYER",
}

# Hardcoded DDR v4.0 topology edges used as fallback.
# Each entry: (src_tier, dst_tier, edge_type, is_conditional)
_TOPOLOGY_EDGES_DEFAULT: list[tuple[str, str, str, bool]] = [
    ("XPD",  "SIL",  "derives",    False),
    ("SIL",  "GPCL", "derives",    False),
    ("GPCL", "FCL",  "derives",    False),
    ("FCL",  "SAL",  "derives",    False),  # always-edge; C-2 exception
    ("FCL",  "CL",   "derives",    True),   # conditional on CL active
    ("CL",   "SAL",  "constrains", True),   # conditional on CL active
    ("SAL",  "ICL",  "derives",    False),
    ("ICL",  "CDL",  "implements", False),
    ("CDL",  "ISL",  "implements", False),
]


# ---------------------------------------------------------------------------
# Tier display metadata extractor
# ---------------------------------------------------------------------------

def _extract_display_metadata(ddr_data: dict[str, Any]) -> dict[str, Any]:
    """
    Build tier display metadata from tier_definitions when present,
    falling back to hardcoded DDR v4.0 defaults.

    Derives: tier labels, layer labels, core questions (first line,
    truncated to 72 chars), optional/merge/terminal tier sets, and
    canonical topology edges for the tier topology diagram.

    Parameters
    ----------
    ddr_data : dict
        Parsed DDR YAML data.

    Returns
    -------
    dict
        Keys:
          labels         : dict[tier_id → display label]
          layer_labels   : dict[tier_id → layer band label]
          core_questions : dict[tier_id → first line of core_question]
          optional_tiers : set[str]
          merge_tiers    : set[str]
          terminal_tiers : set[str]
          topology_edges : list of (src, dst, edge_type, is_conditional)
    """
    tier_defs: list[dict] = ddr_data.get("tier_definitions", [])
    struct_meta = _extract_tier_metadata(ddr_data)

    if not tier_defs:
        return {
            "labels":         dict(_TIER_LABELS_DEFAULT),
            "layer_labels":   dict(_LAYER_LABELS_DEFAULT),
            "core_questions": {},
            "topology_edges": list(_TOPOLOGY_EDGES_DEFAULT),
            **struct_meta,
        }

    labels:         dict[str, str] = {}
    layer_labels:   dict[str, str] = {}
    core_questions: dict[str, str] = {}
    topology_edges: list[tuple[str, str, str, bool]] = []

    for td in tier_defs:
        tier_id = td.get("tier_id", "")
        if not tier_id:
            continue

        labels[tier_id]       = td.get("label",       _TIER_LABELS_DEFAULT.get(tier_id, tier_id))
        layer_labels[tier_id] = td.get("layer_label", _LAYER_LABELS_DEFAULT.get(tier_id, ""))

        cq = td.get("core_question", "").strip()
        if cq:
            first_line = cq.split("\n")[0].strip()[:72]
            core_questions[tier_id] = first_line

        for cr in td.get("child_relationships", []):
            child_tier = cr.get("tier", "")
            if child_tier and child_tier != "NONE":
                condition = cr.get("condition", "always")
                topology_edges.append((
                    tier_id,
                    child_tier,
                    cr.get("edge_type", "derives"),
                    condition != "always",
                ))

    # Ensure all spec tiers have a label (fills gaps in partial definitions)
    for tier_id in _TIER_LABELS_DEFAULT:
        labels.setdefault(tier_id, _TIER_LABELS_DEFAULT[tier_id])
        layer_labels.setdefault(tier_id, _LAYER_LABELS_DEFAULT.get(tier_id, ""))

    return {
        "labels":         labels,
        "layer_labels":   layer_labels,
        "core_questions": core_questions,
        "topology_edges": topology_edges if topology_edges else list(_TOPOLOGY_EDGES_DEFAULT),
        **struct_meta,
    }


# ---------------------------------------------------------------------------
# Style loader
# ---------------------------------------------------------------------------

def _load_style() -> dict[str, Any]:
    """
    Load the visual style configuration from assets/style_config.json.

    Returns
    -------
    dict
        Parsed style configuration.

    Raises
    ------
    FileNotFoundError
        If style_config.json is not found in the assets directory.
    """
    cfg_path = _ASSETS_DIR / "style_config.json"
    if not cfg_path.exists():
        raise FileNotFoundError(
            f"style_config.json not found at {cfg_path}. "
            "Ensure the assets/ directory is intact."
        )
    with cfg_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Node and edge styling helpers
# ---------------------------------------------------------------------------

def _get_node_attrs(node: dict[str, Any], style: dict) -> dict[str, str]:
    """
    Derive Graphviz node attribute dictionary for a DDR node.

    Parameters
    ----------
    node : dict
        A single DDR node definition from the YAML nodes list.
    style : dict
        Loaded style configuration.

    Returns
    -------
    dict
        Graphviz attribute key-value pairs.
    """
    status    = node.get("status", "DRAFT")
    tier      = node.get("tier", "")
    tier_style   = style["tiers"].get(tier,   style["tiers"]["_default"])
    status_style = style["status"].get(status, style["status"]["DRAFT"])

    label = "\\n".join([
        f"{node.get('id', '?')}",
        f"{node.get('title', '')}",
        f"[{status}]  v{node.get('version', '?')}",
    ])

    return {
        "label":     label,
        "shape":     "box",
        "style":     "filled,rounded",
        "fillcolor": status_style["fillcolor"],
        "color":     status_style.get("bordercolor", tier_style["border_color"]),
        "fontcolor": status_style["fontcolor"],
        "fontname":  "Courier New",
        "fontsize":  "9",
        "margin":    "0.18,0.1",
        "penwidth":  "3.0" if status == "DIRTY" else "1.5",
    }


def _get_edge_attrs(edge_type: str, style: dict) -> dict[str, str]:
    """
    Derive Graphviz edge attribute dictionary for a DDR edge.

    Parameters
    ----------
    edge_type : str
        One of: derives, constrains, implements, extends.
    style : dict
        Loaded style configuration.

    Returns
    -------
    dict
        Graphviz edge attribute key-value pairs.
    """
    es = style["edges"].get(edge_type, style["edges"]["_default"])
    return {
        "color":     es["color"],
        "style":     es["dash"],
        "arrowhead": es["arrowhead"],
        "fontcolor": es["color"],
        "fontname":  "Helvetica",
        "fontsize":  "8",
        "penwidth":  es.get("penwidth", "1.5"),
        "label":     f" {edge_type}",
    }


# ---------------------------------------------------------------------------
# Legend builder
# ---------------------------------------------------------------------------

def _add_legend(dot: graphviz.Digraph, style: dict) -> None:
    """
    Append a self-contained legend cluster to a Graphviz diagram.

    Covers node status colours and all four edge type styles so the
    diagram is interpretable without external reference.

    Parameters
    ----------
    dot : graphviz.Digraph
        The diagram to append the legend to (mutated in place).
    style : dict
        Loaded style configuration.
    """
    with dot.subgraph(name="cluster_legend") as leg:
        leg.attr(
            label="LEGEND",
            style="filled",
            fillcolor="#f9f9f9",
            color="#aaaaaa",
            fontname="Helvetica Neue Bold",
            fontsize="10",
            rank="sink",
            margin="10",
        )

        prev_id: str | None = None
        for status, s_style in style["status"].items():
            if status.startswith("_"):
                continue
            leg_id = f"legend_status_{status}"
            leg.node(
                leg_id,
                label=status,
                shape="box",
                style="filled,rounded",
                fillcolor=s_style["fillcolor"],
                color=s_style.get("bordercolor", "#666666"),
                fontcolor=s_style["fontcolor"],
                fontname="Courier New",
                fontsize="8",
                margin="0.12,0.06",
                penwidth="1.5",
            )
            if prev_id:
                leg.edge(prev_id, leg_id, style="invis")
            prev_id = leg_id

        edge_prev: str | None = None
        for edge_type, es in style["edges"].items():
            if edge_type.startswith("_"):
                continue
            src = f"legend_edge_src_{edge_type}"
            dst = f"legend_edge_dst_{edge_type}"
            leg.node(src, label="", shape="point", width="0.01")
            leg.node(dst, label=f" → {edge_type}", shape="none",
                     fontname="Helvetica", fontsize="8", fontcolor=es["color"])
            leg.edge(src, dst, color=es["color"], style=es["dash"],
                     arrowhead=es["arrowhead"], penwidth=es.get("penwidth", "1.5"))
            if edge_prev:
                leg.edge(edge_prev, src, style="invis")
            edge_prev = dst


# ---------------------------------------------------------------------------
# Full DAG diagram
# ---------------------------------------------------------------------------

def build_full_dag_diagram(
    G: "nx.DiGraph",  # noqa: F821
    ddr_data: dict[str, Any],
    style: dict,
) -> graphviz.Digraph:
    """
    Construct the complete DDR DAG diagram with tier cluster bands.

    Cluster labels are built dynamically from tier_definitions (when
    present), showing layer_label, tier ID, tier label, and core_question
    first line. Optional, merge, and terminal-leaf tiers receive visual
    markers. Falls back to hardcoded DDR v4.0 defaults for project-instance
    files without tier_definitions.

    Parameters
    ----------
    G : nx.DiGraph
        Validated networkx DAG.
    ddr_data : dict
        Parsed DDR YAML data.
    style : dict
        Loaded style configuration.

    Returns
    -------
    graphviz.Digraph
        Fully configured Graphviz diagram ready for rendering.
    """
    active_tiers: list[str] = ddr_data.get("active_tiers", list(TIER_ORDER.keys()))
    project_name: str = (
        ddr_data.get("project", {}).get("name")
        or ddr_data.get("system_metadata", {}).get("authority", "DDR System")
    )
    display_meta = _extract_display_metadata(ddr_data)

    dot = graphviz.Digraph(
        name="DDR_DAG_Full",
        engine="dot",
        graph_attr={
            "rankdir":  "TB",
            "compound": "true",
            "fontname": "Helvetica Neue",
            "fontsize": "13",
            "label":    f"DDR System v4.0 — {project_name}\\nFull DAG",
            "labelloc": "t",
            "splines":  "ortho",
            "nodesep":  "0.55",
            "ranksep":  "1.1",
            "bgcolor":  "#ffffff",
            "dpi":      "300",
            "margin":   "0.6",
            "pad":      "0.4",
        },
        node_attr={"fontname": "Courier New",  "fontsize": "9"},
        edge_attr={"fontname": "Helvetica",    "fontsize": "8"},
    )

    nodes_by_tier: dict[str, list[dict]] = defaultdict(list)
    for node in ddr_data.get("nodes", []):
        nodes_by_tier[node.get("tier", "UNKNOWN")].append(node)

    for tier in TIER_ORDER:
        if tier not in active_tiers:
            continue

        tier_style   = style["tiers"].get(tier, style["tiers"]["_default"])
        tier_nodes   = nodes_by_tier.get(tier, [])
        is_optional  = tier in display_meta["optional_tiers"]
        is_merge     = tier in display_meta["merge_tiers"]
        is_terminal  = tier in display_meta["terminal_tiers"]

        layer_lbl = display_meta["layer_labels"].get(tier, "")
        tier_lbl  = display_meta["labels"].get(tier, tier)
        core_q    = display_meta["core_questions"].get(tier, "")

        # Build cluster label: layer → tier with markers → label → core question
        markers: list[str] = []
        if is_optional:
            markers.append("[OPTIONAL]")
        if is_merge:
            markers.append("← MERGE NODE")
        if is_terminal:
            markers.append("← TERMINAL LEAF")

        header = f"{tier}"
        if markers:
            header += "  " + "  ".join(markers)

        cluster_label_parts = []
        if layer_lbl:
            cluster_label_parts.append(layer_lbl)
        cluster_label_parts.append(header)
        cluster_label_parts.append(tier_lbl)
        if core_q:
            cluster_label_parts.append(f'"{core_q}"')

        cluster_label = "\\n".join(cluster_label_parts)

        with dot.subgraph(name=f"cluster_{tier}") as sub:
            sub.attr(
                label=cluster_label,
                style="filled",
                fillcolor=tier_style["cluster_bg"],
                color=tier_style["border_color"],
                fontcolor=tier_style["label_color"],
                fontname="Helvetica Neue Bold",
                fontsize="9",
                penwidth="2.5" if is_merge else "1.5",
                margin="14",
            )

            if not tier_nodes:
                sub.node(
                    f"_empty_{tier}",
                    label=f"(no {tier} nodes defined)",
                    shape="plaintext",
                    fontname="Helvetica",
                    fontsize="8",
                    fontcolor="#999999",
                )
            else:
                for node in tier_nodes:
                    attrs = _get_node_attrs(node, style)
                    sub.node(node["id"], **attrs)

    # Add all edges from parent_ids
    for node in ddr_data.get("nodes", []):
        for parent_entry in node.get("parent_ids", []):
            parent_id = parent_entry.get("id")
            edge_type = parent_entry.get("edge_type", "derives")
            if not parent_id:
                continue
            if not G.has_node(parent_id) or not G.has_node(node["id"]):
                continue
            edge_attrs = _get_edge_attrs(edge_type, style)
            dot.edge(parent_id, node["id"], **edge_attrs)

    _add_legend(dot, style)
    return dot


# ---------------------------------------------------------------------------
# Tier topology diagram
# ---------------------------------------------------------------------------

def build_tier_topology_diagram(
    ddr_data: dict[str, Any],
    style: dict,
) -> graphviz.Digraph:
    """
    Construct a tier-level topology diagram without individual nodes.

    Tier labels, layer labels, optional/merge/terminal markers, and
    topology edges are all derived dynamically from tier_definitions when
    present. Inactive optional tiers are rendered in gray with dashed
    borders. Inactive edges (connecting tiers not in active_tiers) are
    rendered gray.

    Parameters
    ----------
    ddr_data : dict
        Parsed DDR YAML data.
    style : dict
        Loaded style configuration.

    Returns
    -------
    graphviz.Digraph
        Tier topology diagram.
    """
    active_tiers: list[str] = ddr_data.get("active_tiers", list(TIER_ORDER.keys()))
    project_name: str = (
        ddr_data.get("project", {}).get("name")
        or ddr_data.get("system_metadata", {}).get("authority", "DDR System")
    )
    display_meta = _extract_display_metadata(ddr_data)

    dot = graphviz.Digraph(
        name="DDR_Tier_Topology",
        engine="dot",
        graph_attr={
            "rankdir":  "TB",
            "fontname": "Helvetica Neue",
            "fontsize": "12",
            "label":    f"DDR System v4.0 — {project_name}\\nTier Topology",
            "labelloc": "t",
            "splines":  "ortho",
            "nodesep":  "0.4",
            "ranksep":  "0.9",
            "bgcolor":  "#ffffff",
            "dpi":      "300",
            "pad":      "0.5",
        },
    )

    # Tier nodes
    for tier_id, rank in TIER_ORDER.items():
        is_active   = tier_id in active_tiers
        is_optional = tier_id in display_meta["optional_tiers"]
        is_merge    = tier_id in display_meta["merge_tiers"]
        is_terminal = tier_id in display_meta["terminal_tiers"]
        tier_style  = style["tiers"].get(tier_id, style["tiers"]["_default"])

        tier_lbl  = display_meta["labels"].get(tier_id, tier_id)
        layer_lbl = display_meta["layer_labels"].get(tier_id, "")
        core_q    = display_meta["core_questions"].get(tier_id, "")

        markers: list[str] = []
        if is_optional:
            markers.append("[optional]")
        if is_merge:
            markers.append("← MERGE")
        if is_terminal:
            markers.append("← LEAF")

        header = tier_id
        if markers:
            header += "  " + "  ".join(markers)
        if not is_active:
            header += "  [INACTIVE]"

        label_parts = []
        if layer_lbl:
            label_parts.append(layer_lbl)
        label_parts.append(header)
        label_parts.append(tier_lbl)
        if core_q and is_active:
            label_parts.append(f'"{core_q[:60]}"')

        node_label = "\\n".join(filter(None, label_parts))

        node_color  = tier_style["border_color"] if is_active else "#cccccc"
        fill_color  = tier_style["cluster_bg"]   if is_active else "#f0f0f0"
        font_color  = tier_style["label_color"]  if is_active else "#aaaaaa"
        dash_style  = "filled,rounded" + (",dashed" if not is_active else "")
        penwidth    = "2.5" if (is_merge and is_active) else "1.5"

        dot.node(
            f"TIER_{tier_id}",
            label=node_label,
            shape="box",
            style=dash_style,
            fillcolor=fill_color,
            color=node_color,
            fontcolor=font_color,
            fontname="Helvetica Neue Bold",
            fontsize="10",
            margin="0.25,0.15",
            penwidth=penwidth,
            width="3.8",
        )

    # Topology edges derived dynamically from tier_definitions (or hardcoded default)
    seen_edges: set[tuple[str, str]] = set()
    for src, dst, edge_type, is_conditional in display_meta["topology_edges"]:
        # Deduplicate: child_relationships and parent_relationships may overlap
        edge_key = (src, dst)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        src_active = src in active_tiers
        dst_active = dst in active_tiers

        edge_attrs = _get_edge_attrs(edge_type, style)
        if not (src_active and dst_active):
            edge_attrs["color"]     = "#cccccc"
            edge_attrs["fontcolor"] = "#cccccc"
            edge_attrs["style"]     = "dashed"

        dot.edge(f"TIER_{src}", f"TIER_{dst}", **edge_attrs)

    return dot


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_outputs(
    dot: graphviz.Digraph,
    output_dir: Path,
    stem: str,
) -> list[Path]:
    """
    Render a Graphviz diagram to SVG and PNG in the output directory.

    Parameters
    ----------
    dot : graphviz.Digraph
        Configured Graphviz diagram.
    output_dir : Path
        Directory where output files will be written.
    stem : str
        Base filename without extension (e.g. 'ddr_dag_full').

    Returns
    -------
    list of Path
        Paths of all generated output files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    for fmt in ("svg", "png"):
        dot.format = fmt
        rendered = dot.render(
            filename=str(output_dir / stem),
            cleanup=True,
            quiet=True,
        )
        rendered_path = Path(rendered)
        if rendered_path.exists():
            generated.append(rendered_path)

    return generated


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main() -> int:
    """
    Main entry point for the DDR DAG visualization pipeline.

    Loads the DDR YAML (system-definition or project-instance), validates
    structural invariants, generates the full DAG and tier topology
    diagrams, and writes all output files to the specified directory.

    Returns
    -------
    int
        0 = success CLEAN, 1 = success with violations, 2 = fatal error.
    """
    if not shutil.which("dot"):
        print(
            "ERROR: Graphviz 'dot' binary not found on PATH.\n"
            "Install: brew install graphviz  |  apt install graphviz  "
            "|  winget install graphviz",
            file=sys.stderr,
        )
        return 2

    parser = argparse.ArgumentParser(
        description="Generate DDR System v4.0 DAG visualizations."
    )
    parser.add_argument(
        "yaml_file",
        help="Path to the DDR YAML definition file (system-definition or project-instance).",
    )
    parser.add_argument(
        "--output-dir",
        default="./ddr_output",
        help="Directory for output files (default: ./ddr_output).",
    )
    args = parser.parse_args()

    try:
        ddr_data = load_ddr_yaml(args.yaml_file)
    except Exception as exc:
        print(f"ERROR loading YAML: {exc}", file=sys.stderr)
        return 2

    try:
        style = _load_style()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    G, parse_errors   = build_graph(ddr_data)
    result            = verify(G, ddr_data)
    result.violations = parse_errors + result.violations
    md_report, json_report = generate_report(result, ddr_data)

    output_dir      = Path(args.output_dir)
    generated_files: list[Path] = []

    try:
        full_dot = build_full_dag_diagram(G, ddr_data, style)
        generated_files.extend(render_outputs(full_dot, output_dir, "ddr_dag_full"))
    except Exception as exc:
        print(f"ERROR rendering full DAG: {exc}", file=sys.stderr)
        return 2

    try:
        topo_dot = build_tier_topology_diagram(ddr_data, style)
        generated_files.extend(render_outputs(topo_dot, output_dir, "ddr_dag_tiers"))
    except Exception as exc:
        print(f"ERROR rendering tier topology: {exc}", file=sys.stderr)
        return 2

    md_path   = output_dir / "validation_report.md"
    json_path = output_dir / "validation_report.json"
    md_path.write_text(md_report,                             encoding="utf-8")
    json_path.write_text(json.dumps(json_report, indent=2),   encoding="utf-8")
    generated_files.extend([md_path, json_path])

    print("\n✅ DDR Visualization Complete")
    print(f"   Output directory: {output_dir.resolve()}")
    print("\n   Generated files:")
    for f in generated_files:
        print(f"     {f.name}")

    tier_defs_present = bool(ddr_data.get("tier_definitions"))
    file_type = "system-definition" if tier_defs_present else "project-instance"
    print(f"\n   Input file type: {file_type}")
    if tier_defs_present:
        td_count = len(ddr_data["tier_definitions"])
        ext_count = len(ddr_data.get("extension_catalog", []))
        print(f"   Tier definitions loaded: {td_count}")
        if ext_count:
            print(f"   Extension catalog entries: {ext_count}")

    status_str = (
        "CLEAN ✅"
        if result.clean
        else f"DIRTY ❌ ({len(result.violations)} violations)"
    )
    print(f"\n   Validation status: {status_str}")

    if result.violations:
        print("\n   Violations summary:")
        for v in result.violations[:10]:
            icon = {"CRITICAL": "⛔", "ERROR": "🔴", "WARNING": "🟡"}.get(v.severity, "•")
            print(f"     {icon} [{v.rule_id}] {v.node_id}")
        if len(result.violations) > 10:
            print(f"     ... and {len(result.violations) - 10} more. See validation_report.md")

    print("\n   See validation_report.md for the full VERIFY report.\n")
    return 0 if result.clean else 1


if __name__ == "__main__":
    sys.exit(main())
