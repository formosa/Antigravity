"""
Abstract to Business Value Tool.

Converts technology-specific terminology to business-appropriate language
for BRD tier compliance.

Meta
----
Tool Definition : .agent/tools/brd_abstract_to_business_value.md
Knowledge Source: .agent/knowledge/sources/constraints/brd_technology_agnostic.md
Architect       : Antigravity IDE

Usage
-----
    python abstract_to_business.py --text "Use Python REST API with Redis cache"

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Error (Details printed to stderr)
"""
import argparse
import json
import re
import sys

# Technology terms → business replacements (brd_technology_agnostic.md §Detection)
TRANSFORMS: dict[str, str] = {
    # Languages/frameworks → [REMOVE]
    "python": "[REMOVE]", "javascript": "[REMOVE]", "java": "[REMOVE]",
    "react": "[REMOVE]", "typescript": "[REMOVE]", "golang": "[REMOVE]",
    "zeromq": "[REMOVE]", "pyside6": "[REMOVE]", "pvporcupine": "[REMOVE]",
    "flask": "[REMOVE]", "django": "[REMOVE]", "fastapi": "[REMOVE]",
    # Hardware → generic
    "gpu": "hardware acceleration", "cpu": "processing resource",
    "rtx": "graphics processing", "cuda": "parallel computing",
    "amd": "processing hardware", "nvidia": "graphics hardware",
    # Protocols → generic
    "tcp": "network communication", "mqtt": "message protocol",
    "rest": "service interface", "api": "system interface",
    "grpc": "service interface", "websocket": "real-time connection",
    # Databases → generic
    "postgresql": "relational storage", "redis": "caching layer",
    "sqlite": "local storage", "mongodb": "document storage",
    # Formats → generic
    "json": "data format", "yaml": "configuration format", "protobuf": "binary format",
    # Infrastructure
    "microservice": "modular component", "kubernetes": "orchestration platform",
    "docker": "containerization", "aws": "cloud platform", "azure": "cloud platform",
    "latency": "response time", "throughput": "processing capacity",
    "database": "data storage", "cache": "performance layer", "bandwidth": "transfer capacity",
}


def transform(text: str) -> dict:
    """
    Transform technology-specific text to business language.

    Parameters
    ----------
    text : str
        Input text with potential technology terms.

    Returns
    -------
    dict
        Keys: original, transformed, changes, warnings.
    """
    result = text
    changes = []
    warnings = []

    for term, replacement in TRANSFORMS.items():
        pattern = rf"\b{term}\b"
        if re.search(pattern, result, re.I):
            if replacement == "[REMOVE]":
                result = re.sub(pattern, "", result, flags=re.I)
                changes.append(f"Removed '{term}'")
            else:
                result = re.sub(pattern, replacement, result, flags=re.I)
                changes.append(f"'{term}' -> '{replacement}'")

    # Check for unhandled tech terms
    unhandled = re.findall(r"\b(SQL|MongoDB|Redis|Kubernetes|Docker|AWS|Azure)\b", result, re.I)
    for u in set(unhandled):
        warnings.append(f"Unhandled tech term: {u}")

    return {"original": text, "transformed": result.strip(), "changes": changes, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    print(json.dumps(transform(args.text), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
