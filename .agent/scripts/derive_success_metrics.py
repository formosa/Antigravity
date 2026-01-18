"""
Derive Success Metrics Tool.

Generates quantifiable success metrics from business objectives.

Meta
----
Tool Definition : .agent/tools/brd_derive_success_metrics.md
Knowledge Source: .agent/knowledge/sources/constraints/brd_measurable_metrics.md
Architect       : Antigravity IDE

Usage
-----
    python derive_success_metrics.py --objective "System must be fast and reliable"

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import sys

# Metric categories (brd_measurable_metrics.md)
PATTERNS: dict[str, dict] = {
    "performance": {
        "keywords": ["fast", "quick", "responsive", "efficient", "speed", "latency", "throughput"],
        "metrics": ["Response time < X seconds", "Throughput > X ops/min", "Latency < X ms"]
    },
    "reliability": {
        "keywords": ["available", "reliable", "uptime", "stable", "fault", "recover", "resilient"],
        "metrics": ["Availability > 99.X%", "MTBF > X hours", "Recovery time < X seconds"]
    },
    "usability": {
        "keywords": ["easy", "intuitive", "simple", "user-friendly", "accessible", "learn"],
        "metrics": ["Task completion > X%", "User satisfaction > X/10", "Learning time < X min"]
    },
    "scalability": {
        "keywords": ["scale", "grow", "concurrent", "load", "capacity", "elastic"],
        "metrics": ["Support X concurrent users", "Linear scaling to X nodes", "Handle X% load increase"]
    },
    "security": {
        "keywords": ["secure", "protect", "encrypt", "authenticate", "authorize", "safe"],
        "metrics": ["Zero critical vulnerabilities", "Authentication time < X ms", "Encryption coverage 100%"]
    },
    "maintainability": {
        "keywords": ["maintain", "update", "extend", "modular", "refactor", "document"],
        "metrics": ["Code coverage > X%", "Deployment time < X min", "Mean time to fix < X hours"]
    },
}


def derive(objective: str) -> dict:
    objective_lower = objective.lower()
    detected = []
    suggested = []

    for category, data in PATTERNS.items():
        for kw in data["keywords"]:
            if kw in objective_lower:
                detected.append(category)
                suggested.extend(data["metrics"])
                break

    return {"objective": objective, "detected_categories": list(set(detected)),
            "suggested_metrics": list(set(suggested))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--objective", required=True)
    args = parser.parse_args()

    print(json.dumps(derive(args.objective), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
