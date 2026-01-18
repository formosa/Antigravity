"""
Route to Specialist Tool.

Maps a DDR tier to its corresponding specialist persona handle.
This tool supports the orchestrator's delegation workflow by providing
tier-to-agent routing information.

Meta
----
Tool Definition : .agent/tools/ddr_route_to_specialist.md
Knowledge Source: .agent/knowledge/sources/concepts/tier_hierarchy.md
Architect       : Antigravity IDE

Usage
-----
    python route_to_specialist.py --tier <TIER>
    python route_to_specialist.py --tier FSD

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Invalid tier or error (Details printed to stderr)
"""

import argparse
import json
import sys
from typing import Optional

# Tier-to-Specialist mapping derived from Phase 2.2 agent personas
TIER_SPECIALIST_MAP: dict[str, dict[str, str]] = {
    "BRD": {
        "handle": "@brd_strategist",
        "persona_path": ".agent/personas/brd_strategist.mdc",
        "description": "Business Requirements Specialist"
    },
    "NFR": {
        "handle": "@nfr_enforcer",
        "persona_path": ".agent/personas/nfr_enforcer.mdc",
        "description": "Non-Functional Requirements Enforcer"
    },
    "FSD": {
        "handle": "@fsd_analyst",
        "persona_path": ".agent/personas/fsd_analyst.mdc",
        "description": "Feature Specification Analyst"
    },
    "SAD": {
        "handle": "@sad_architect",
        "persona_path": ".agent/personas/sad_architect.mdc",
        "description": "System Architecture Designer"
    },
    "ICD": {
        "handle": "@icd_dataengineer",
        "persona_path": ".agent/personas/icd_dataengineer.mdc",
        "description": "Interface Contract Data Engineer"
    },
    "TDD": {
        "handle": "@tdd_designer",
        "persona_path": ".agent/personas/tdd_designer.mdc",
        "description": "Technical Design Document Designer"
    },
    "ISP": {
        "handle": "@isp_codegenerator",
        "persona_path": ".agent/personas/isp_codegenerator.mdc",
        "description": "Implementation Stub Producer"
    }
}

VALID_TIERS = list(TIER_SPECIALIST_MAP.keys())


def route_to_specialist(tier: str) -> Optional[dict]:
    """
    Look up the specialist agent for a given DDR tier.

    Parameters
    ----------
    tier : str
        The DDR tier code (BRD, NFR, FSD, SAD, ICD, TDD, ISP).
        Case-insensitive.

    Returns
    -------
    dict or None
        Dictionary containing 'tier', 'handle', 'persona_path', 'description'.
        None if the tier is invalid.
    """
    tier_upper = tier.upper().strip()
    if tier_upper not in TIER_SPECIALIST_MAP:
        return None

    specialist = TIER_SPECIALIST_MAP[tier_upper]
    return {
        "tier": tier_upper,
        "handle": specialist["handle"],
        "persona_path": specialist["persona_path"],
        "description": specialist["description"]
    }


def main() -> int:
    """
    CLI entry point for routing tier to specialist.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Route a DDR tier to its specialist persona."
    )
    parser.add_argument(
        "--tier",
        required=True,
        help=f"DDR tier code. Valid values: {', '.join(VALID_TIERS)}"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_all",
        help="List all tier-to-specialist mappings"
    )

    args = parser.parse_args()

    # Handle list mode
    if args.list_all:
        output = {
            "tiers": VALID_TIERS,
            "mappings": {
                tier: route_to_specialist(tier)
                for tier in VALID_TIERS
            }
        }
        print(json.dumps(output, indent=2))
        return 0

    # Route single tier
    result = route_to_specialist(args.tier)
    if result is None:
        print(
            f"Error: Invalid tier '{args.tier}'. "
            f"Valid tiers: {', '.join(VALID_TIERS)}",
            file=sys.stderr
        )
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
