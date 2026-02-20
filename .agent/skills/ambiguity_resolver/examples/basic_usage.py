"""
Basic usage examples for the ambiguity_resolver skill.

Demonstrates:
- Simple fragment classification
- Batch processing
- Different output formats
- Context-aware classification
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from resolver import AmbiguityResolver, Tier
from utils import format_detailed_output, format_rst_output


def example_1_simple_classification():
    """Example 1: Simple fragment classification."""
    print("=" * 70)
    print("EXAMPLE 1: Simple Classification")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    fragment = (
        "System must aggregate all log messages into a single file "
        "with automatic rotation every 50MB and retain logs for 30 days"
    )

    print(f"Fragment: {fragment}")
    print()

    result = resolver.resolve(fragment)

    print(format_detailed_output(result))
    print()


def example_2_with_candidate_tiers():
    """Example 2: Pre-identified candidate tiers."""
    print("=" * 70)
    print("EXAMPLE 2: With Candidate Tiers")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    fragment = "IPC dispatch must be sub-millisecond for metadata-only messages"

    # Decision tree already identified NFR and ICD as candidates
    candidate_tiers = [Tier.NFR, Tier.ICD]

    print(f"Fragment: {fragment}")
    print(f"Candidates: {[t.value for t in candidate_tiers]}")
    print()

    result = resolver.resolve(fragment, candidate_tiers)

    print(f"Assigned Tier: {result.assigned_tier.value}")
    print(f"Confidence: {result.confidence:.3f}")
    print()
    print("Scores:")
    for tier, score in result.scores.items():
        marker = " ← SELECTED" if tier == result.assigned_tier else ""
        print(f"  {tier.value}: {score}{marker}")
    print()


def example_3_batch_processing():
    """Example 3: Batch classification of multiple fragments."""
    print("=" * 70)
    print("EXAMPLE 3: Batch Processing")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    fragments = [
        "System must respond within 1 second average latency",
        "Hub-and-Spoke messaging pattern with Core as central router",
        "User receives visual feedback within 100ms of voice input",
        "CoreProcess class orchestrates IPC between services",
        "def run(self) -> None: pass"
    ]

    print(f"Processing {len(fragments)} fragments...")
    print()

    results = resolver.resolve_batch(fragments)

    for i, (fragment, result) in enumerate(zip(fragments, results), 1):
        print(f"{i}. {fragment[:60]}...")
        print(f"   → {result.assigned_tier.value} (confidence: {result.confidence:.2f})")
        print()


def example_4_with_context():
    """Example 4: Context-aware classification."""
    print("=" * 70)
    print("EXAMPLE 4: Context-Aware Classification")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    fragment = "Voice interaction pipeline processes wake word detection"

    # Provide context for validation
    context = {
        'existing_brd_tags': ['BRD-1', 'BRD-2', 'BRD-5', 'BRD-5.7'],
        'existing_nfr_tags': ['NFR-1', 'NFR-4', 'NFR-4.1'],
        'project_domain': 'voice-ai'
    }

    print(f"Fragment: {fragment}")
    print(f"Context: {context['project_domain']}")
    print(f"Available BRD tags: {len(context['existing_brd_tags'])}")
    print()

    result = resolver.resolve(fragment, context=context)

    print(f"Assigned Tier: {result.assigned_tier.value}")
    print(f"Validation: {'PASSED' if result.validation_passed else 'FAILED'}")
    print()
    print("Validation Notes:")
    for note in result.validation_notes:
        print(f"  - {note}")
    print()


def example_5_output_formats():
    """Example 5: Different output formats."""
    print("=" * 70)
    print("EXAMPLE 5: Output Formats")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    fragment = "Logs must be aggregated to single unified file"

    result = resolver.resolve(fragment)

    # Format 1: Detailed report
    print("Format 1: DETAILED REPORT")
    print("-" * 70)
    print(format_detailed_output(result))
    print()

    # Format 2: RST directive
    print("Format 2: RST DIRECTIVE")
    print("-" * 70)
    print(format_rst_output(result))
    print()


def example_6_tie_breaker():
    """Example 6: Tie-breaker scenario."""
    print("=" * 70)
    print("EXAMPLE 6: Tie-Breaker Scenario")
    print("=" * 70)
    print()

    resolver = AmbiguityResolver()

    # Fragment that could be BRD or FSD
    fragment = "Enable real-time voice interaction for accessibility"

    print(f"Fragment: {fragment}")
    print()

    result = resolver.resolve(fragment)

    print(f"Assigned Tier: {result.assigned_tier.value}")
    print()
    print("Scores:")
    sorted_scores = sorted(result.scores.items(), key=lambda x: x[1], reverse=True)
    for tier, score in sorted_scores:
        marker = " ← SELECTED" if tier == result.assigned_tier else ""
        print(f"  {tier.value}: {score}{marker}")
    print()

    if result.tie_breaker_applied:
        print("⚠️  Tie-breaker applied: Higher abstraction selected")
    print()


def main():
    """Run all examples."""
    examples = [
        ("Simple Classification", example_1_simple_classification),
        ("With Candidate Tiers", example_2_with_candidate_tiers),
        ("Batch Processing", example_3_batch_processing),
        ("Context-Aware", example_4_with_context),
        ("Output Formats", example_5_output_formats),
        ("Tie-Breaker", example_6_tie_breaker)
    ]

    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AMBIGUITY RESOLVER EXAMPLES" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()

        if i < len(examples):
            input("Press Enter to continue to next example...")
            print("\n\n")

    print()
    print("All examples completed!")
    print()


if __name__ == "__main__":
    main()
