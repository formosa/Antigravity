---
description: Apply comprehensive Numpy-style docstrings to a targeted Python script with programmatic integrity verification.
---

# Workflow: `/document-script`

**Invocation**: `/document-script <target_file.py>`

## Goal
Apply comprehensive **Numpy-style docstrings** to a targeted Python script with programmatic integrity verification and legacy content preservation.

---

## Workflow Steps

### 0. Pre-Flight Check
1. Verify target file exists.
2. Verify `.py` extension.
3. Verify parseable Python:
// turbo
```powershell
.venv\Scripts\python -m py_compile <target_file>
```
4. **On Failure**: HALT, notify user.

---

### 1. Backup Original
1. Create temp directory if needed:
// turbo
```powershell
New-Item -ItemType Directory -Force -Path ".agent/workflows/temp"
```
2. Copy target → `.agent/workflows/temp/<script-name>(original).py`
// turbo
```powershell
Copy-Item <target_file> ".agent/workflows/temp/<script-name>(original).py"
```
3. **Example**: `audit-report.py` → `.agent/workflows/temp/audit-report(original).py`

---

### 2. Sanitize Existing Docstrings
1. Remove all existing docstrings from the target file.
2. **Scope**: Only triple-quoted strings in docstring positions (first statement of module/class/function/method).
3. **Preserve**: All `#` code comments must remain intact.
4. **NEVER** modify the backup copy.
5. Verify syntax after sanitization:
// turbo
```powershell
.venv\Scripts\python -m py_compile <target_file>
```
6. **On Failure**: Restore from backup, HALT, notify user.

---

### 3. Load Reference & Apply Docstrings
1. **Reference**: Read `.agent/workflows/assets/numpy-style-doc-example.py`
2. **Action**: Generate/overwrite all docstrings per reference standard.
3. **Policy**: Existing docstrings are **EXPIRED/UNVERIFIED** → **OVERWRITE**.
4. **Processing Order**: Document items in the order listed in the *Applicable Sections* table below.
5. **Type Hints Policy**: ALWAYS include types in Parameters section, regardless of whether function signatures have type hints.

**Applicable Sections by Item Type**:
> Generate sections **only when applicable** to the target code. Omit sections that would be empty or require fabrication. If uncertain about applicability, ASK USER.

| Item Type | Section | Condition |
| :--- | :--- | :--- |
| **Module** | Summary | Always |
| | Notes | If implementation details warrant explanation |
| | See Also | If related modules/packages exist |
| | References | If algorithms have academic citations |
| | Examples | If usage patterns are non-obvious |
| **Exception** | Summary | Always |
| | Parameters | If `__init__` accepts arguments |
| | Attributes | If custom attributes are defined |
| | Examples | If usage is non-obvious |
| **Abstract Class** | Summary | Always |
| | Methods | Always (documents interface contract) |
| | Notes | If usage constraints exist |
| **Dataclass** | Summary | Always |
| | Attributes | Always (documents fields) |
| | Examples | If instantiation is non-trivial |
| **Class** | Summary | Always |
| | Parameters | If `__init__` accepts arguments |
| | Attributes | If instance attributes are documented |
| | Raises | If `__init__` raises exceptions |
| | See Also | If related classes exist |
| | Notes | If internal behavior warrants explanation |
| | Examples | If usage is non-obvious |
| **Property** | Summary | Always |
| | Returns | Always |
| | Notes | If behavior differs from simple getter |
| **Method/Function** | Summary | Always |
| | Parameters | If function accepts arguments |
| | Returns | If function returns a value (not `None`-only) |
| | Raises | If function explicitly raises exceptions |
| | Warns | If function uses `warnings.warn()` |
| | See Also | If related functions exist |
| | Notes | If algorithm/complexity warrants explanation |
| | Examples | If usage is non-obvious |
| **Generator** | Summary | Always |
| | Parameters | If generator accepts arguments |
| | Yields | Always (defines generator contract) |
| | Raises | If generator raises exceptions |

---

### 4. Programmatic Verification (AST Diff)
1. **Tool**: Use `/ast_compare` custom tool (`.agent/tools/ast_compare.mdt`)
2. Compare AST structures (ignoring docstrings) between backup and target.
3. **Criteria**: Zero code logic changes allowed.
4. **On Failure**: Restore code from backup, reapply docstrings.
5. **Max Attempts**: 3 → then HALT, notify user.
6. **On Success**: Mark **PROGRAMMATICALLY VERIFIED**.

// turbo
```powershell
.venv\Scripts\python .agent\tools\scripts\ast_compare.py ".agent/workflows/temp/<script-name>(original).py" "<target_file>"
```

**Exit Codes**: 0=match (proceed), 1=mismatch (restore & retry), 2=error (HALT)

---

### 5. Legacy Content Merge
1. Analyze original file's comments/docstrings for:
   - Cross-file relationships
   - Application behavior notes
   - Reference information
2. **Merge Criteria** (all must be true):
   - Technically accurate (if unverifiable, ASK USER)
   - Not already present in new docstrings
   - Relevant and useful
3. **Insertion Rules**:
   - Cross-file references → `See Also` section
   - Usage warnings → `Warns` section or inline comments
   - **General Capture** → `Notes` section (Use as catch-all for any other relevant info like algorithm details, behavioral context, or historical notes)

---

### 6. Final Validation Audit
1. **Review**: Comprehensively audit all docstrings for accuracy and Numpy formatting.
2. **Action**:
   - **If Issues Found**: PERFORM FIX immediately.
   - **If No Issues**: Proceed to Cleanup.
3. **Loop Control**:
   - Repeat Review/Fix cycle max **2 times**.
   - **HALT Condition**: If issues persist after 2 cycles, STOP and notify user for manual review (prevents infinite loops).

---

### 7. Cleanup
1. **On Success**: Delete backup from `.agent/workflows/temp/`
2. **On Failure**: Preserve backup, notify user of location.

---

> [!IMPORTANT]
> **Agent Protocol**: You are explicitly encouraged to PAUSE and consult the user if encountering conflicting information, processing errors, or ambiguity. Seek clarification or resolution confirmation rather than making assumptions.

---

## Verification Plan

### Automated
1. **Syntax**: `py_compile` passes.
2. **AST Diff**: Structures match (excluding docstrings).

### Manual
1. User reviews final docstring content.
