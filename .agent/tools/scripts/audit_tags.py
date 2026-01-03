import os
import re
from pathlib import Path

def audit_tags():
    docs_dir = Path("docs")
    tag_counts = {}

    # Regex for needs tags: :id: TYPE-NUMBER
    id_pattern = re.compile(r':id:\s+([A-Z]+)-[\d\.]+')

    print("Starting Audit...")

    for root, dirs, files in os.walk(docs_dir):
        if "_build" in root:
            continue

        folder_name = Path(root).name
        # We only care about main doc folders (01_, 02_, etc) or root
        if not (folder_name.startswith("0") or folder_name == "docs"):
             # check if parent is docs
             if Path(root).parent.name != "docs" and folder_name != "docs":
                 continue

        local_counts = {}

        for file in files:
            if not file.endswith(".rst"):
                continue

            path = Path(root) / file
            if "reconciliation_manifest" in file:
                continue

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = id_pattern.findall(content)
                for tag_type in matches:
                    local_counts[tag_type] = local_counts.get(tag_type, 0) + 1

        if local_counts:
            print(f"\nFolder: {folder_name}")
            total = sum(local_counts.values())
            print(f"Total Tags: {total}")
            for tag, count in local_counts.items():
                print(f"  {tag}: {count}")

if __name__ == "__main__":
    audit_tags()
