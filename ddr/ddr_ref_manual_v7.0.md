<!--
generated_by: .agent/scripts/generate_ddr_release_docs.py
source_system: ddr/ddr_system_v7.0.yaml
source_schema: ddr/ddr_node_schema_v7.0.yaml
surface_role: explanatory_reference_manual
authority: explanatory_only_yaml_pair_governs
-->

# DDR System v7.0 Reference Manual

This manual is generated from the authoritative v7.0 YAML pair and remains explanatory only.

## Orientation

| Field            | Value                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| document_profile | system_definition                                                                                                                    |
| schema_title     | DDR System v7.0 Machine Contract                                                                                                     |
| corpus_root      | ddr/conformance/v7.0                                                                                                                 |
| migration_scope  | Migration is limited to v6.3 -> v7.0 authority uplift, generated release surfaces, conformance assets, and governed release tooling. |

## Profile Matrix

| Use Case                   | System Class     | Maturity              | Assurance      | Readiness Gates                   |
| -------------------------- | ---------------- | --------------------- | -------------- | --------------------------------- |
| developer_tools            | developer_tool   | local_only            | standard       | design_complete                   |
| games                      | game_system      | managed_release       | standard       | design_complete, production_ready |
| enterprise_platforms       | service_platform | continuously_operated | elevated       | design_complete, production_ready |
| hardware_aware_deployments | hardware_aware   | managed_release       | elevated       | design_complete, production_ready |
| medical_government_banking | regulated_system | continuously_operated | high_assurance | design_complete, production_ready |

## Tier Quick Starts

| Tier | Label                              | Quick Start                                                                                                                  |
| ---- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| XPD  | Existential Purpose Document       | Example: state the human need, harm boundaries, and success criteria without naming technology.                              |
| SIL  | Strategic Intent Layer             | Example: define the strategic objective, stakeholder value, scope boundaries, and success metrics in plain language.         |
| GPCL | Governance, Policy & Quality Layer | Example: declare latency, reliability, security, retention, and residency thresholds with no technology commitments.         |
| FCL  | Functional Capability Layer        | Example: describe the user-visible behavior, state transitions, and data entities touched by the capability.                 |
| CL   | Constraint Layer                   | Example: target_platforms [local_tool, desktop]; hardware_envelope CPU 4 cores, RAM 16 GB, storage 1 GB, network local-only. |
| SAL  | System Architecture Layer          | Example: name the major subsystems, ownership boundaries, communication pattern, and resilience boundaries.                  |
| ICL  | Interface & Contracts Layer        | Example: define request, response, error, versioning, and retry expectations for one machine-parseable contract.             |
| CDL  | Component Design Layer             | Example: declare one component's responsibilities, interfaces, state, dependencies, and lifecycle hooks.                     |
| ISL  | Implementation Scaffold Layer      | Example: generate a class or module skeleton with docstrings citing CDL parents and stubbed method bodies only.              |

## Compliance Guidance

- design_complete is the minimum gate for local-only and developer-tool objectives.
- production_ready is required for managed_release and continuously_operated objectives.
- High-assurance regulated objectives require XPD activation and immutable evidence for readiness claims.

## Conformance and Migration

- Generated markdown surfaces must match provenance expectations for the current v7.0 YAML pair.
- Valid corpus cases must validate successfully against ddr_node_schema_v7.0.yaml.
- Invalid corpus cases must fail for the expected structural reason.

- Migration source: 6.3
- Migration target: 7.0
- Migration owner: DDR Architecture Board via the owned v7.0 release toolchain.

## Reference Generators

| Generator          | Script                                      | Outputs                    |
| ------------------ | ------------------------------------------- | -------------------------- |
| canonical_markdown | .agent/scripts/generate_ddr_release_docs.py | ddr/DDR System(v7.0).md    |
| reference_manual   | .agent/scripts/generate_ddr_release_docs.py | ddr/ddr_ref_manual_v7.0.md |
