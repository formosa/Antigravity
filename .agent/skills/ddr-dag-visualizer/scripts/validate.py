"""
DDR System v4.0 - Structural Validation Engine.

Implements the VERIFY operation (§7.1) and all DAG invariants (§3.5, §6)
for a DDR System defined in a YAML file parsed into a networkx DiGraph.

Accepts both file types defined by ddr_node_schema.yaml:
  - System-definition files (e.g. ddr_system_v4.0.yaml): contain
    tier_definitions, axioms, operations, extension_catalog, and nodes.
    Tier metadata is loaded dynamically from tier_definitions.
  - Project-instance files: contain only ddr_version, active_tiers, nodes.
    Tier metadata falls back to hardcoded DDR v4.0 spec-derived defaults.

Notes
-----
Audit C-2 (FCL->SAL always-edge tier-skip exception) is encoded as a
first-class constant in TIER_SKIP_EXCEPTIONS.

Audit H-1 (status state machine) is implemented as VALID_TRANSITIONS,
providing the formal transition model absent from the prose specification.

Audit C-3 (ORL-R7 TBD) is flagged as an annotation in the tier_migration
section of ddr_system_v4.0.yaml; no runtime impact.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

import networkx as nx
import yaml
from align_table import process_document


# ---------------------------------------------------------------------------
# Spec-derived constants (DDR v4.0 §3, §7)
# ---------------------------------------------------------------------------

TIER_ORDER: dict[str, int] = {
    "XPD": 0, "SIL": 1, "GPCL": 2, "FCL": 3,
    "CL": 4, "SAL": 5, "ICL": 6, "CDL": 7, "ISL": 8,
}

VALID_EDGE_TYPES: frozenset[str] = frozenset({
    "derives", "constrains", "implements", "extends"
})

# Audit C-2: FCL→SAL always-edge is a documented exception to the
# no-tier-skipping invariant (§3.5 INV-2, §3.4 topology diagram).
TIER_SKIP_EXCEPTIONS: frozenset[tuple[str, str]] = frozenset({
    ("FCL", "SAL"),
})

# Audit H-1: formal status transition model (§3.1, §7.1, §7.2).
VALID_TRANSITIONS: dict[tuple[str, str], str] = {
    ("DRAFT",      "ACTIVE"):      "VALIDATE",
    ("DRAFT",      "DELETED"):     "DELETE",
    ("ACTIVE",     "DIRTY"):       "MODIFY/propagation",
    ("ACTIVE",     "DEPRECATED"):  "MODIFY",
    ("ACTIVE",     "SUPERSEDED"):  "SUPERSEDE",
    ("DIRTY",      "ACTIVE"):      "VERIFY+VALIDATE",
    ("DIRTY",      "DEPRECATED"):  "MODIFY",
    ("DIRTY",      "SUPERSEDED"):  "SUPERSEDE",
    ("DEPRECATED", "SUPERSEDED"):  "SUPERSEDE",
    ("DEPRECATED", "DELETED"):     "DELETE",
}

VALID_STATUSES: frozenset[str] = frozenset({
    "DRAFT", "ACTIVE", "DIRTY", "DEPRECATED", "SUPERSEDED"
})

# Spec-derived defaults — used when tier_definitions is absent.
_DEFAULT_OPTIONAL_TIERS:  frozenset[str] = frozenset({"XPD", "CL"})
_DEFAULT_MANDATORY_TIERS: frozenset[str] = frozenset({
    "SIL", "GPCL", "FCL", "SAL", "ICL", "CDL", "ISL"
})
_DEFAULT_MERGE_TIERS:     frozenset[str] = frozenset({"SAL"})
_DEFAULT_TERMINAL_TIERS:  frozenset[str] = frozenset({"ISL"})


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Violation:
    """
    A single structural violation detected during VERIFY.

    Parameters
    ----------
    rule_id : str
        The DDR specification rule ID violated (e.g. 'AX-7', 'CIT-R1').
    node_id : str
        Primary node involved. May be an edge string 'PARENT_ID -> CHILD_ID'
        or 'active_tiers' for schema-level violations.
    description : str
        Human-readable explanation with architectural consequence.
    severity : str
        One of 'CRITICAL', 'ERROR', or 'WARNING'.
    """
    rule_id: str
    node_id: str
    description: str
    severity: str = "ERROR"


@dataclass
class VerifyResult:
    """
    Aggregated result of a full VERIFY traversal.

    Parameters
    ----------
    clean : bool
        True only when violations is empty and no DIRTY nodes remain.
    violations : list of Violation
        All structural violations detected. Empty list → CLEAN.
    node_count : int
        Total nodes in the graph.
    tier_counts : dict
        Node count per tier.
    status_counts : dict
        Node count per status value.
    """
    clean: bool
    violations: list[Violation] = field(default_factory=list)
    node_count: int = 0
    tier_counts: dict[str, int] = field(default_factory=dict)
    status_counts: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Tier metadata extraction
# ---------------------------------------------------------------------------

def _extract_tier_metadata(ddr_data: dict[str, Any]) -> dict[str, Any]:
    """
    Extract tier structural metadata from tier_definitions when present,
    falling back to hardcoded DDR v4.0 spec-derived defaults.

    Supports both system-definition files (full tier_definitions section)
    and minimal project-instance files (no tier_definitions).

    Parameters
    ----------
    ddr_data : dict
        Parsed DDR YAML data.

    Returns
    -------
    dict
        Keys: 'optional_tiers', 'mandatory_tiers', 'merge_tiers',
        'terminal_tiers' — each a set of tier ID strings.

    Examples
    --------
    >>> meta = _extract_tier_metadata({"ddr_version": "4.0", "active_tiers": [], "nodes": []})
    >>> "SAL" in meta["merge_tiers"]
    True
    >>> "ISL" in meta["terminal_tiers"]
    True
    """
    tier_defs: list[dict] = ddr_data.get("tier_definitions", [])

    if not tier_defs:
        return {
            "optional_tiers":  set(_DEFAULT_OPTIONAL_TIERS),
            "mandatory_tiers": set(_DEFAULT_MANDATORY_TIERS),
            "merge_tiers":     set(_DEFAULT_MERGE_TIERS),
            "terminal_tiers":  set(_DEFAULT_TERMINAL_TIERS),
        }

    optional_tiers:  set[str] = set()
    mandatory_tiers: set[str] = set()
    merge_tiers:     set[str] = set()
    terminal_tiers:  set[str] = set()

    for td in tier_defs:
        tier_id = td.get("tier_id", "")
        if not tier_id:
            continue
        if td.get("is_optional", False):
            optional_tiers.add(tier_id)
        else:
            mandatory_tiers.add(tier_id)
        if td.get("is_merge_node", False):
            merge_tiers.add(tier_id)
        if td.get("is_terminal_leaf", False):
            terminal_tiers.add(tier_id)

    # Guarantee non-empty sets: fall back to defaults if tier_definitions
    # is present but incomplete (e.g. partially authored system file).
    return {
        "optional_tiers":  optional_tiers  or set(_DEFAULT_OPTIONAL_TIERS),
        "mandatory_tiers": mandatory_tiers or set(_DEFAULT_MANDATORY_TIERS),
        "merge_tiers":     merge_tiers     or set(_DEFAULT_MERGE_TIERS),
        "terminal_tiers":  terminal_tiers  or set(_DEFAULT_TERMINAL_TIERS),
    }


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def load_ddr_yaml(path: str | Path) -> dict[str, Any]:
    """
    Load and parse a DDR System YAML definition file.

    Parameters
    ----------
    path : str or Path
        Path to the DDR YAML file (system-definition or project-instance).

    Returns
    -------
    dict
        Parsed DDR data structure.

    Raises
    ------
    FileNotFoundError
        If the specified path does not exist.
    yaml.YAMLError
        If the file contains invalid YAML syntax.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"DDR YAML file not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data if data else {}


def build_graph(
    ddr_data: dict[str, Any],
) -> tuple[nx.DiGraph, list[Violation]]:
    """
    Construct a networkx DiGraph from the `nodes` section of a parsed
    DDR YAML data structure.

    Parameters
    ----------
    ddr_data : dict
        Parsed DDR YAML content.

    Returns
    -------
    G : nx.DiGraph
        Graph with node attributes matching the DDR node schema and
        edge attributes containing 'edge_type'.
    parse_errors : list of Violation
        Violations detected during construction (e.g. missing parent IDs).
    """
    G = nx.DiGraph()
    parse_errors: list[Violation] = []
    nodes: list[dict] = ddr_data.get("nodes", [])

    node_ids: set[str] = {n["id"] for n in nodes if "id" in n}

    for node in nodes:
        node_id = node.get("id")
        if not node_id:
            parse_errors.append(Violation(
                rule_id="SCHEMA-ID",
                node_id="<unknown>",
                description="A node is missing the required 'id' field.",
                severity="CRITICAL",
            ))
            continue

        G.add_node(
            node_id,
            tier=node.get("tier", ""),
            title=node.get("title", ""),
            status=node.get("status", "DRAFT"),
            version=node.get("version", ""),
        )

        for parent_entry in node.get("parent_ids", []):
            parent_id = parent_entry.get("id")
            edge_type = parent_entry.get("edge_type", "derives")

            if parent_id not in node_ids:
                parse_errors.append(Violation(
                    rule_id="CIT-R1",
                    node_id=node_id,
                    description=(
                        f"parent_id '{parent_id}' referenced by '{node_id}' "
                        "does not correspond to any defined node."
                    ),
                    severity="CRITICAL",
                ))
                continue

            G.add_edge(parent_id, node_id, edge_type=edge_type)

    return G, parse_errors


# ---------------------------------------------------------------------------
# Individual invariant checks
# ---------------------------------------------------------------------------

def _check_mandatory_tiers(
    ddr_data: dict[str, Any],
    tier_meta: dict[str, Any],
) -> list[Violation]:
    """
    Check that all mandatory tiers are declared in active_tiers (§3.5).

    Parameters
    ----------
    ddr_data : dict
        Parsed DDR YAML.
    tier_meta : dict
        Output of _extract_tier_metadata().

    Returns
    -------
    list of Violation
        One ERROR per missing mandatory tier.
    """
    active: set[str] = set(ddr_data.get("active_tiers", []))
    mandatory: set[str] = tier_meta.get("mandatory_tiers", set(_DEFAULT_MANDATORY_TIERS))

    return [
        Violation(
            rule_id="INV-MANDATORY",
            node_id="active_tiers",
            description=(
                f"Mandatory tier '{tier_id}' is absent from active_tiers. "
                "DDR v4.0 requires 7 mandatory tiers: "
                "SIL, GPCL, FCL, SAL, ICL, CDL, ISL."
            ),
            severity="ERROR",
        )
        for tier_id in sorted(mandatory)
        if tier_id not in active
    ]


def _check_acyclicity(G: nx.DiGraph) -> list[Violation]:
    """Check AX-7: no cycles permitted at any path length."""
    if nx.is_directed_acyclic_graph(G):
        return []
    cycles = list(nx.simple_cycles(G))
    return [Violation(
        rule_id="AX-7",
        node_id=" -> ".join(cycles[0]) if cycles else "<cycle>",
        description=(
            f"Cycle detected involving nodes: {cycles[0]}. "
            "Causality must flow in one direction only (AX-7)."
        ),
        severity="CRITICAL",
    )]


def _check_orphans(
    G: nx.DiGraph,
    active_tiers: list[str],
) -> list[Violation]:
    """
    Check CIT-R1 / AX-1: every non-root node must have ≥1 parent_id.

    Root tier is XPD when active, otherwise SIL (§3.5 INV-6, §3.4).
    """
    root_tiers: set[str] = {"XPD"} if "XPD" in active_tiers else {"SIL"}
    violations = []

    for node_id, attrs in G.nodes(data=True):
        tier = attrs.get("tier", "")
        if tier not in root_tiers and G.in_degree(node_id) == 0:
            violations.append(Violation(
                rule_id="CIT-R1",
                node_id=node_id,
                description=(
                    f"Orphaned non-root node '{node_id}' (tier: {tier}) "
                    "has no parent citations. Violates AX-1 traceability."
                ),
                severity="ERROR",
            ))
    return violations


def _check_tier_skipping(G: nx.DiGraph) -> list[Violation]:
    """
    Check §3.5 INV-2: no tier-skipping in the derivation path.

    The FCL→SAL always-edge (Audit C-2) is encoded in TIER_SKIP_EXCEPTIONS
    and will never trigger a violation regardless of CL activation state.
    """
    violations = []
    for parent_id, child_id in G.edges():
        parent_tier = G.nodes[parent_id].get("tier", "")
        child_tier  = G.nodes[child_id].get("tier", "")

        if (parent_tier, child_tier) in TIER_SKIP_EXCEPTIONS:
            continue

        parent_rank = TIER_ORDER.get(parent_tier, -1)
        child_rank  = TIER_ORDER.get(child_tier, -1)

        if parent_rank < 0 or child_rank < 0:
            continue  # unknown tier — caught by schema validation

        if child_rank - parent_rank > 1:
            violations.append(Violation(
                rule_id="INV-TIER-SKIP",
                node_id=f"{parent_id} -> {child_id}",
                description=(
                    f"Tier-skip: {parent_tier} (rank {parent_rank}) → "
                    f"{child_tier} (rank {child_rank}), gap="
                    f"{child_rank - parent_rank}. §3.5 INV-2 requires each "
                    "citation to reference exactly one active tier above."
                ),
                severity="ERROR",
            ))
    return violations


def _check_edge_types(G: nx.DiGraph) -> list[Violation]:
    """Check §3.2: all edges must carry a valid edge_type."""
    return [
        Violation(
            rule_id="EDGE-TYPE",
            node_id=f"{p} -> {c}",
            description=(
                f"Edge from '{p}' to '{c}' has invalid "
                f"edge_type='{attrs.get('edge_type', '')}'. "
                f"Valid types: {sorted(VALID_EDGE_TYPES)}."
            ),
            severity="ERROR",
        )
        for p, c, attrs in G.edges(data=True)
        if attrs.get("edge_type", "") not in VALID_EDGE_TYPES
    ]


def _check_merge_nodes(
    G: nx.DiGraph,
    active_tiers: list[str],
    tier_meta: dict[str, Any],
) -> list[Violation]:
    """
    Check SAL-R6: merge nodes must cite all required parents.

    When CL is active, SAL must carry both FCL (derives) and CL
    (constrains) as parents. Merge tiers are derived dynamically from
    tier_meta; falls back to SAL per the DDR v4.0 spec.

    Parameters
    ----------
    G : nx.DiGraph
        The DDR DAG.
    active_tiers : list of str
        Active tier identifiers.
    tier_meta : dict
        Output of _extract_tier_metadata().

    Returns
    -------
    list of Violation
    """
    if "CL" not in active_tiers:
        return []

    merge_tiers: set[str] = tier_meta.get("merge_tiers", set(_DEFAULT_MERGE_TIERS))
    violations: list[Violation] = []

    for merge_tier in merge_tiers:
        merge_nodes = [
            n for n, d in G.nodes(data=True) if d.get("tier") == merge_tier
        ]

        for node_id in merge_nodes:
            in_edges = [
                (p, G.edges[p, node_id]["edge_type"])
                for p in G.predecessors(node_id)
            ]
            parent_tiers: dict[str, str] = {
                G.nodes[p].get("tier", ""): et for p, et in in_edges
            }

            if "FCL" not in parent_tiers:
                violations.append(Violation(
                    rule_id="SAL-R6",
                    node_id=node_id,
                    description=(
                        f"Merge node '{node_id}' (tier: {merge_tier}) is "
                        "missing a 'derives' edge from an FCL parent. "
                        "SAL-R6 requires FCL (derives) + CL (constrains) "
                        "when CL is active."
                    ),
                    severity="ERROR",
                ))

            if "CL" not in parent_tiers:
                violations.append(Violation(
                    rule_id="SAL-R6",
                    node_id=node_id,
                    description=(
                        f"Merge node '{node_id}' (tier: {merge_tier}) is "
                        "missing a 'constrains' edge from a CL parent. "
                        "CL is active but not cited. Violates SAL-R6."
                    ),
                    severity="ERROR",
                ))
            elif parent_tiers.get("CL") != "constrains":
                violations.append(Violation(
                    rule_id="SAL-R6",
                    node_id=node_id,
                    description=(
                        f"Merge node '{node_id}' has CL parent but "
                        f"edge_type='{parent_tiers['CL']}' instead of "
                        "'constrains'. CL→SAL must use 'constrains' per §3.2."
                    ),
                    severity="ERROR",
                ))
    return violations


def _check_status_values(G: nx.DiGraph) -> list[Violation]:
    """Check §3.1: all node status values must be within the defined set."""
    return [
        Violation(
            rule_id="SCHEMA-STATUS",
            node_id=node_id,
            description=(
                f"Node '{node_id}' has invalid status="
                f"'{attrs.get('status', '')}'. "
                f"Valid values: {sorted(VALID_STATUSES)}."
            ),
            severity="ERROR",
        )
        for node_id, attrs in G.nodes(data=True)
        if attrs.get("status", "") not in VALID_STATUSES
    ]


def _check_leaf_nodes(
    G: nx.DiGraph,
    tier_meta: dict[str, Any],
) -> list[Violation]:
    """
    Check Glossary / §7.2: in a CLEAN DAG, only terminal leaf tiers
    (ISL by default; derived from tier_meta when available) may be leaves.

    Parameters
    ----------
    G : nx.DiGraph
        The DDR DAG.
    tier_meta : dict
        Output of _extract_tier_metadata().

    Returns
    -------
    list of Violation
    """
    terminal_tiers: set[str] = tier_meta.get(
        "terminal_tiers", set(_DEFAULT_TERMINAL_TIERS)
    )
    violations: list[Violation] = []

    for node_id, attrs in G.nodes(data=True):
        tier   = attrs.get("tier", "")
        status = attrs.get("status", "")

        if tier in terminal_tiers:
            continue
        if status in ("DEPRECATED", "SUPERSEDED"):
            continue
        if G.out_degree(node_id) == 0:
            violations.append(Violation(
                rule_id="LEAF-NODE",
                node_id=node_id,
                description=(
                    f"Non-terminal node '{node_id}' (tier: {tier}) is a "
                    "leaf with no children. Only terminal-leaf-tier nodes "
                    f"({sorted(terminal_tiers)}) are valid leaves in a CLEAN "
                    "DAG. This node may be incomplete."
                ),
                severity="WARNING",
            ))
    return violations


# ---------------------------------------------------------------------------
# Top-level VERIFY
# ---------------------------------------------------------------------------

def verify(G: nx.DiGraph, ddr_data: dict[str, Any]) -> VerifyResult:
    """
    Execute the DDR VERIFY operation against the graph (§7.1).

    Traverses the full DAG and validates all structural invariants defined
    in DDR v4.0 §2–§7. Tier metadata is loaded dynamically from
    tier_definitions when present, enabling both system-definition and
    project-instance file support.

    Parameters
    ----------
    G : nx.DiGraph
        The DDR DAG built via build_graph().
    ddr_data : dict
        The original parsed YAML data.

    Returns
    -------
    VerifyResult
        Aggregated validation result with violations and statistics.
    """
    active_tiers: list[str] = ddr_data.get(
        "active_tiers", list(TIER_ORDER.keys())
    )
    tier_meta = _extract_tier_metadata(ddr_data)
    violations: list[Violation] = []

    # Order reflects severity: structural > schema > semantic > advisory
    violations.extend(_check_acyclicity(G))
    violations.extend(_check_mandatory_tiers(ddr_data, tier_meta))
    violations.extend(_check_orphans(G, active_tiers))
    violations.extend(_check_tier_skipping(G))
    violations.extend(_check_edge_types(G))
    violations.extend(_check_merge_nodes(G, active_tiers, tier_meta))
    violations.extend(_check_status_values(G))
    violations.extend(_check_leaf_nodes(G, tier_meta))

    tier_counts:   dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for _, attrs in G.nodes(data=True):
        t = attrs.get("tier",   "UNKNOWN")
        s = attrs.get("status", "UNKNOWN")
        tier_counts[t]   = tier_counts.get(t, 0)   + 1
        status_counts[s] = status_counts.get(s, 0) + 1

    clean = (
        len(violations) == 0
        and status_counts.get("DIRTY", 0) == 0
    )

    return VerifyResult(
        clean=clean,
        violations=violations,
        node_count=G.number_of_nodes(),
        tier_counts=tier_counts,
        status_counts=status_counts,
    )


def generate_report(
    result: VerifyResult,
    ddr_data: dict[str, Any],
) -> tuple[str, dict]:
    """
    Generate human-readable Markdown and machine-readable JSON reports
    from a VerifyResult.

    Parameters
    ----------
    result : VerifyResult
        Output of verify().
    ddr_data : dict
        Original parsed DDR YAML for project metadata.

    Returns
    -------
    md_report : str
        Formatted Markdown validation report.
    json_report : dict
        Structured JSON-serializable report.
    """
    project    = ddr_data.get("project", {})
    sys_meta   = ddr_data.get("system_metadata", {})
    # System-definition files use system_metadata; project-instance files use project.
    name       = project.get("name") or sys_meta.get("authority", "Unnamed DDR Definition")
    version    = ddr_data.get("ddr_version", "4.0")
    status_str = "✅ CLEAN" if result.clean else "❌ DIRTY"

    severity_order = {"CRITICAL": 0, "ERROR": 1, "WARNING": 2}
    sorted_v = sorted(
        result.violations,
        key=lambda v: (severity_order.get(v.severity, 3), v.rule_id),
    )

    lines = [
        f"# DDR VERIFY Report — {name}",
        "",
        "| Property | Value |",
        "|---|---|",
        f"| DDR Version | {version} |",
        f"| Overall Status | {status_str} |",
        f"| Total Nodes | {result.node_count} |",
        f"| Violations | {len(result.violations)} |",
        "",
        "## Node Statistics",
        "",
        "| Tier | Count |",
        "|---|---|",
    ]
    for tier in TIER_ORDER:
        count = result.tier_counts.get(tier, 0)
        if count:
            lines.append(f"| {tier} | {count} |")

    lines += ["", "| Status | Count |", "|---|---|"]
    for s in sorted(result.status_counts):
        lines.append(f"| {s} | {result.status_counts[s]} |")

    lines += ["", "## Violations"]
    if not sorted_v:
        lines += ["", "_No violations detected. DAG is structurally CLEAN._"]
    else:
        for v in sorted_v:
            icon = {"CRITICAL": "⛔", "ERROR": "🔴", "WARNING": "🟡"}.get(v.severity, "•")
            lines.append(f"\n### {icon} [{v.severity}] `{v.rule_id}` — `{v.node_id}`")
            lines.append(f"\n{v.description}")

    md_report   = process_document("\n".join(lines))
    json_report = {
        "project":         name,
        "ddr_version":     version,
        "clean":           result.clean,
        "node_count":      result.node_count,
        "tier_counts":     result.tier_counts,
        "status_counts":   result.status_counts,
        "violation_count": len(result.violations),
        "violations":      [asdict(v) for v in sorted_v],
    }
    return md_report, json_report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """
    Command-line entry point for standalone validation.

    Returns
    -------
    int
        Exit code: 0 = CLEAN, 1 = violations found, 2 = fatal error.
    """
    if len(sys.argv) < 2:
        print("Usage: python validate.py <ddr_yaml_file>", file=sys.stderr)
        return 2

    try:
        ddr_data = load_ddr_yaml(sys.argv[1])
    except (FileNotFoundError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    G, parse_errors = build_graph(ddr_data)
    result          = verify(G, ddr_data)
    result.violations = parse_errors + result.violations

    md_report, json_report = generate_report(result, ddr_data)
    print(md_report)
    print("\n--- JSON ---")
    print(json.dumps(json_report, indent=2))

    return 0 if result.clean else 1


if __name__ == "__main__":
    sys.exit(main())
