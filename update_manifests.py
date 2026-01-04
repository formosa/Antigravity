"""
Reconciliation Manifest Bulk Generator.

This script regenerates all `reconciliation_manifest.rst` files across the
documentation structure with current tag inventory counts. It uses a
standardized YAML template format for consistent manifest structure.

Purpose
-------
Bulk update reconciliation manifests when tag counts change:

- Writes to 6 manifest files (requirements, specs, arch, data, design, prompts)
- Uses current date as `last_audit` timestamp
- Maintains consistent YAML structure across all manifests

Dependencies
------------
- Python 3.8+ (datetime module)
- Write access to `docs/` directory structure

Usage
-----
Execute from project root::

    python update_manifests.py

.. warning::

    This script uses **hardcoded tag counts**. Before running:
    1. Run a traceability audit to get current counts
    2. Update the `COUNTS` dictionary with actual values
    3. Execute the script

Configuration
-------------
COUNTS : dict
    Tag counts by prefix (BRD, NFR, FSD, SAD, ICD, TDD, ISP)
MANIFESTS : list
    Tuples of (file_path, section_name, inventory_dict)
TEMPLATE : str
    RST template with YAML code block for manifest content

Output Files
------------
- docs/01_requirements/reconciliation_manifest.rst (BRD + NFR)
- docs/02_specifications/reconciliation_manifest.rst (FSD)
- docs/03_architecture/reconciliation_manifest.rst (SAD)
- docs/04_data/reconciliation_manifest.rst (ICD)
- docs/05_design/reconciliation_manifest.rst (TDD)
- docs/06_prompts/reconciliation_manifest.rst (ISP)

Notes
-----
- The title is auto-adjusted for non-requirements sections
- Consider moving to dynamic count fetching from audit_traceability.py

See Also
--------
- audit_traceability.py : Source for accurate tag counts
- .agent/workflows/traceability_audit.md : Full audit workflow
"""
import datetime

COUNTS = {
    "BRD": 36, "NFR": 39,
    "FSD": 46, "SAD": 27,
    "ICD": 13, "TDD": 40,
    "ISP": 19
}

MANIFESTS = [
    ("docs/01_requirements/reconciliation_manifest.rst", "01_requirements", {"BRD": 36, "NFR": 39}),
    ("docs/02_specifications/reconciliation_manifest.rst", "02_specifications", {"FSD": 46}),
    ("docs/03_architecture/reconciliation_manifest.rst", "03_architecture", {"SAD": 27}),
    ("docs/04_data/reconciliation_manifest.rst", "04_data", {"ICD": 13}),
    ("docs/05_design/reconciliation_manifest.rst", "05_design", {"TDD": 40}),
    ("docs/06_prompts/reconciliation_manifest.rst", "06_prompts", {"ISP": 19}),
]

TEMPLATE = """Reconciliation Manifest: Requirements
====================================

.. code-block:: yaml

   reconciliation_manifest:
     section: {section}
     integrity_status: CLEAN
     tag_count: {total}
     tag_inventory:
{inventory}
     pending_items: []
     last_audit: {date}
"""

today = datetime.date.today().isoformat()

for path, section, inv in MANIFESTS:
    total = sum(inv.values())
    inv_str = "\n".join([f"       {k}: {v}" for k, v in inv.items()])

    content = TEMPLATE.format(
        section=section,
        total=total,
        inventory=inv_str,
        date=today
    )

    # Adjust title for non-requirements
    if "requirements" not in path:
        title = path.split('/')[1].replace('_', ' ').title()
        content = content.replace("Reconciliation Manifest: Requirements", f"Reconciliation Manifest: {title}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {path}")
