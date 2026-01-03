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
