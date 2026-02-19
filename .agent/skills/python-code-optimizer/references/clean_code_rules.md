# Clean Code Enforcement Rules

Rules derived from Robert C. Martin's *Clean Code* (2009).

## N: Naming

- **N1 — Descriptive Names**: Use `SECONDS_PER_DAY` not `d`. Names must reveal intent.
- **N2 — Abstraction Level**: `get_user()` not `fetch_sql_row()`. Names match abstraction.
- **N3 — No Single Letters**: Except `i,j,k` (loops), `x,y,z` (coords), `e` (exceptions).
- **N4 — No Encodings**: `users` not `list_of_users`. No Hungarian notation.
- **N7 — Side-Effect Naming**: `get_or_create()` if function may create. Name must warn.

## F: Functions

- **F1 — Max Arguments**: Limit to 5 (enterprise target), aspirational target 3. Above 5 → refactor to dataclass.
- **F2 — No Output Arguments**: Return values instead of mutating arguments.
- **F3 — No Boolean Flags**: Split `render(is_html: bool)` into `render_text()` and `render_html()`.
- **F4 — Small & Focused**: Each function does one thing. Max 50 lines.

## C: Comments

- **C1 — No Obsolete Comments**: Delete comments that describe code that no longer exists.
- **C2 — No Redundant Comments**: `i += 1  # increment i` adds no value.
- **C4 — No Commented-Out Code**: Delete it. Version control preserves history.

## G: General

- **G5 — DRY**: No duplicated code blocks (>3 lines). Extract to shared utilities.
- **G9 — Dead Code**: Delete unused functions, variables, imports. Use `ruff --select F401,F841`.
- **G25 — No Magic Numbers**: Replace literals (except -1, 0, 1) with named `UPPER_CASE` constants.
- **G30 — Single Responsibility**: Classes and functions have one reason to change.
- **G36 — Law of Demeter**: Max attribute access depth 3 (`a.b.c` OK, `a.b.c.d` violation).

## S: Security

- **S1 — No `exec()` / `eval()`**: Never execute dynamically constructed code.
- **S2 — No Wildcard Imports**: `from x import *` pollutes namespace and obscures dependencies.
- **S3 — No Hardcoded Secrets**: API keys, passwords, tokens must use environment variables.
