---
type: evaluation
name: "Manifest Accuracy"
target_agent: "@manifest_manager"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan all .rst files in docs/ and compare against needs.json"
  - "Add a mock tag to a .rst file and verify manifest manager detects the addition"
  - "Modify an existing tag ID and verify manifest manager flags the integrity violation"
rubric:
  - "Verification of 1:1 mapping between .rst tags and needs.json entries"
  - "Detection of orphan tags with 0 false negatives"
  - "Validation of integrity_status field accuracy"
---

# Evaluation: Manifest Accuracy

## Test Procedure

1. Execute:

   ```powershell
   python scripts/reconcile_manifest.py --check-only
   ```

2. Parse output for `MISMATCH` or `ORPHAN`.
3. Verify that the manifest manager correctly identifies all out-of-sync tags.

## Success Criteria

- 100% agreement between physical files and logical manifest.
- Zero undocumented tags in `needs.json`.
- All `pending_items` correctly categorized.