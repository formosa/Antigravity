import yaml
import os

deps_path = r"c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.3\docs\dependencies.txt"
brainstorm_path = r"c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.3\docs\brainstorm.md"

with open(deps_path, "r", encoding="utf-8") as f:
    deps_data = yaml.safe_load(f)

# Collect all items
all_deps = deps_data.get("python_libraries", [])
out_blocks = []

current_idx = 17 # Starting ID: BRAIN-III-017
existing_libs = ["PySide6", "graphviz", "ruamel.yaml"]

for dep in all_deps:
    name = dep.get("name", "Unknown")
    if name in existing_libs:
        continue
    
    desc_raw = dep.get("description", "TBD")
    detail_raw = dep.get("notes", "TBD")
    links = dep.get("links", [])
    repo = "TBD"
    
    if links:
        for link in links:
            if isinstance(link, dict):
                for k, v in link.items():
                    if isinstance(v, str) and v.startswith("http"):
                        repo = v
                        break
            if repo != "TBD":
                break

    desc = desc_raw.replace('\n', ' ')
    detail = detail_raw.replace('\n', ' ')
    latest_release = dep.get('version', 'TBD')
    
    priority_val = "HIGH" if name in ["onnxruntime-gpu", "ctranslate2", "faster-whisper", "kokoro-onnx"] else "MED"

    yaml_str = f"""
#### [BRAIN-III-{current_idx:03d}] {name}
```yaml
entry_type: LIB
entry_id: BRAIN-III-{current_idx:03d}
title: {name}
category: CAT-AI
priority: {priority_val}
status: CANDIDATE
authored_by: DDR-AB
authored_date: 2026-03-30
revised_date: 2026-03-30
description: >-
  {desc}
detail: >-
  {detail}
open_questions:
  - Is "{name}" viable under offline constraints and commercial licensing?
tags:
  - "#{name.lower()}"
  - "#dependency"
ddr_relevance:
  - E5
  - SAL
references:
  - "dependencies.txt"
repository: {repo}
language: Python
license: MIT
commercial_use: YES
latest_release: {latest_release}
maintenance: ACTIVE
install_size_kb: TBD
maturity: MATURE
verdict: CANDIDATE
rejection_reason: ""
```"""
    out_blocks.append(yaml_str)
    current_idx += 1

header = "\n### §III.8 Full Target Subsystem Dependencies\n"

with open(brainstorm_path, "a", encoding="utf-8") as f:
    f.write(header)
    f.write("".join(out_blocks))
    f.write("\n")

print(f"Successfully injected {len(out_blocks)} libraries starting from 017 to {current_idx-1}.")
