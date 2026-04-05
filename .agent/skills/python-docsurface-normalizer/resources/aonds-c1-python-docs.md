# AONDS-C1 — Agent-Optimized Python Documentation Generation Specification

## Purpose

Generate or rewrite Python module docstrings, class docstrings, function or method docstrings, and code comments so they are maximally useful as machine-recoverable execution context.

Optimize for:

- semantic density
- structural consistency
- low ambiguity
- low token noise
- side-effect visibility
- boundary visibility
- invariant visibility
- coupling visibility
- failure-surface visibility
- compatibility with Python `__doc__`
- compatibility with NumPy docstring structure

Do not optimize for:

- friendliness
- pedagogy
- narrative flow
- tutorial prose
- human skimmability

## Non-Negotiable Principles

1. Every generated statement must be factual and grounded in code, tests, schema, or enforced contract.
2. Prefer terse structured clauses over prose paragraphs.
3. Omit unsupported claims instead of hedging.
4. Use comments only when they encode semantics not cheaply recoverable from syntax.
5. Do not insert workflow policy, repository policy, or tool-usage policy into code documentation unless the code itself enforces it.

## Global Generation Behavior

For each target object:

1. Inspect the actual implementation.
2. Infer only what is strongly supported.
3. Generate the densest truthful wording that preserves precision.
4. Omit low-signal sections rather than padding them.
5. Preserve Python and NumPy docstring compatibility.

If uncertainty exists:

- omit the claim
- do not use vague language such as `likely`, `probably`, `appears`, `seems`, or `presumably`

## Coverage Rules

Generate docstrings or comments for:

- non-trivial modules
- public classes
- public functions
- public methods
- private helpers that cross a boundary, mutate nonlocal state, perform validation or normalization, perform filesystem or network or subprocess I/O, encode invariants, or are likely to be invoked directly by tooling or agents

Do not force docstrings onto trivial one-line helpers unless the semantics are non-obvious.

## Output Constraints

Hard constraints:

- use valid Markdown inside docstrings
- use valid NumPy-style section headers when sections are present
- keep generated text semantically compressed
- no decorative headings inside docstrings
- no emojis
- no conversational phrasing
- no human-oriented framing
- no filler such as `This function ...` unless grammar requires it

Compression rules:

- one proposition per line when practical
- prefer labels over sentences
- prefer direct nouns and verbs over padded explanation
- remove articles unless precision suffers
- avoid examples unless behavior cannot be expressed more compactly

## Module Docstring Rules

Every non-trivial module should receive a module docstring.

Required shape:

1. one-line summary
2. extended semantic block

Use these fields when strongly supported:

- `role:`
- `entrypoints:`
- `reads:`
- `writes:`
- `external_io:`
- `state_model:`
- `failure_surface:`
- `coupling:`
- `determinism:`
- `concurrency:`

Template:

```python
"""
<one-line semantic summary>

role: <module role>
entrypoints: <exported entrypoints or "none">
reads: <files/env/config/services/state or "none">
writes: <files/db/state/log/artifacts or "none">
external_io: <network/subprocess/fs/watchers/none>
state_model: <stateless|cached|mutable shared state|singleton|session-scoped|other>
failure_surface: <primary failure classes or "minimal">
coupling: <protocol/schema/api/dependency coupling or "minimal">
determinism: <deterministic|input-dependent|external-state-dependent|nondeterministic>
concurrency: <thread-safe|not thread-safe|async-only|process-local|unknown>
"""
```

Do not include author text, changelog text, or tutorial prose.

## Class Docstring Rules

Generate class docstrings for every public class and for private classes with non-trivial state or lifecycle behavior.

Use supported fields only:

- `role:`
- `lifecycle:`
- `mutability:`
- `ownership:`
- `concurrency:`
- `cache_behavior:`
- `serialization:`
- `coupling:`
- `failure_surface:`

Sections:

- `Parameters` when constructor semantics matter
- `Attributes` when exposed or operationally relevant state matters
- `Notes` only for invariants, lifecycle constraints, ownership, or resource semantics not encoded elsewhere

Template:

```python
"""
<one-line semantic summary>

role: <semantic role>
lifecycle: <construction/use/disposal model>
mutability: <immutable|partially mutable|mutable>
ownership: <owned resources/state>
concurrency: <thread-safe|not thread-safe|async-confined|process-local|unknown>
cache_behavior: <none|read-through|write-through|manual invalidation|other>
serialization: <serializable|non-serializable|schema-coupled|other>
coupling: <external schema/api/protocol/version coupling or "minimal">
failure_surface: <primary failure conditions or "minimal">

Parameters
----------
<parameter entries only when meaningful>

Attributes
----------
<attribute entries only when meaningful>

Notes
-----
<non-trivial lifecycle, invariant, or ownership detail>
"""
```

## Function and Method Docstring Rules

Generate function or method docstrings for:

- all public functions or methods
- private helpers with meaningful boundary, mutation, or validation behavior

Minimum sections:

- summary line
- extended semantic block
- `Parameters`
- `Returns` or `Yields` when applicable

Conditional sections:

- `Raises` only when the trigger is non-obvious and operationally relevant
- `Notes` only when residual nonlocal semantics remain
- `Examples` only when compact edge-case encoding materially reduces ambiguity

Use the extended semantic block fields in this order when supported:

- `purpose:`
- `preconditions:`
- `postconditions:`
- `mutates:`
- `reads:`
- `writes:`
- `external_io:`
- `network:`
- `subprocess:`
- `determinism:`
- `idempotency:`
- `concurrency:`
- `ordering:`
- `aliasing:`
- `security:`
- `complexity:`
- `coupling:`

Template:

```python
"""
<one-line semantic summary>

purpose: <semantic transformation or effect>
preconditions: <required caller-visible state or "none">
postconditions: <guaranteed resulting state or "none">
mutates: <internal or nonlocal state or "none">
reads: <env/config/files/global state/services/input state or "none">
writes: <files/db/cache/log/state/artifacts or "none">
external_io: <fs/network/subprocess/none>
network: <details or "none">
subprocess: <details or "none">
determinism: <deterministic|input-dependent|state-dependent|nondeterministic>
idempotency: <yes|no|conditional: ...>
concurrency: <thread-safe|not thread-safe|reentrant|not reentrant|async-only|unknown>
ordering: <ordering guarantees or "none">
aliasing: <returned object aliasing or ownership semantics or "none">
security: <validation or trust-boundary semantics or "none">
complexity: <only if meaningful and defensible>
coupling: <external schema/api/version/protocol coupling or "minimal">

Parameters
----------
name : type
    <semantic role; constraints; units/encoding/shape; default semantics>

Returns
-------
type
    <semantic meaning; nullability; ordering; aliasing; stability>

Raises
------
ExceptionType
    <trigger condition when operationally meaningful>

Notes
-----
<invariants, side effects, cache semantics, or coupling not captured above>
"""
```

### Summary-Line Rules

The first line must:

- be descriptive or imperative
- encode the real semantic effect
- not merely restate the function name or signature
- avoid `This function ...`
- avoid `Return ...` unless the primary effect truly is value selection or computation

Prefer:

- `Canonicalize request payload and persist normalized records.`
- `Resolve repository-relative paths into validated absolute targets.`
- `Merge policy overlays into an immutable execution configuration.`

Avoid:

- `This function processes the file.`
- `Handle request.`
- `Validate data.`
- `Compute result.`

## Parameter Documentation Rules

For each parameter, include only:

- semantic role
- meaningful type or domain constraints
- units, shape, or encoding when relevant
- legal literal values
- normalization requirements
- default behavior when operationally meaningful

Do not include:

- tautologies
- name restatements
- raw type-hint duplication without new semantics
- conversational filler

Pattern:

```text
name : type
    <semantic role>; <constraints>; <units/encoding/shape>; <default semantics>
```

## Return and Yield Rules

Always encode:

- semantic meaning
- shape or structure
- nullability
- emptiness semantics
- ordering guarantees
- aliasing or ownership
- stability when relevant

Avoid boilerplate such as `Returned value`.

## Raises Rules

Generate `Raises` only when:

- the exception trigger is non-obvious
- operational handling depends on it
- the function enforces a domain-specific contract
- an external boundary failure materially affects callers

Omit `Raises` when exceptions are trivial propagation from obvious library calls or too uncertain to document precisely.

## Notes Rules

Use `Notes` only for information not efficiently encoded elsewhere, such as:

- invariants
- cache invalidation rules
- lifecycle caveats
- resource ownership
- trust-boundary behavior
- schema or protocol compatibility
- mutation subtleties

Do not use `Notes` for tutorial prose, history, vague philosophy, or unsupported performance claims.

## Code Comment Rules

Generate comments only when they encode non-trivial semantics not cheaply recoverable from syntax.

Allowed prefixes:

- `# INVARIANT:`
- `# PRECONDITION:`
- `# POSTCONDITION:`
- `# RATIONALE:`
- `# SIDE-EFFECT:`
- `# SAFETY:`
- `# ASSUMPTION:`
- `# WORKAROUND:`
- `# COUPLING:`

Do not invent extra prefixes.

Preferred placement:

- normalization boundaries
- validation gates
- state transitions
- mutation hotspots
- caching logic
- retry logic
- concurrency boundaries
- external calls
- protocol translation
- lossy transforms
- security-sensitive operations

Forbidden comment content:

- line narration
- obvious syntax restatements
- unsupported claims like `safe`, `correct`, `fast`, or `robust`
- duplicated docstring text without new semantics
- `TODO` or `FIXME` unless explicitly requested
- personal voice

## Semantic Priority Order

When deciding what to keep under token pressure, prefer this order:

1. externally observable side effects
2. boundary conditions and preconditions
3. postconditions
4. mutation semantics
5. invariants
6. external dependency coupling
7. determinism or nondeterminism
8. idempotency
9. ordering guarantees
10. aliasing or ownership
11. concurrency or reentrancy
12. security or trust-boundary behavior
13. failure surface
14. complexity when real and relevant

## Truthfulness Rules

Do not generate unsupported claims about:

- complexity
- thread safety
- determinism
- idempotency
- security
- ownership
- invariants
- rationale

Prefer omission over speculative explanation.

## Rewrite Procedure

For each target object:

1. inspect the signature
2. inspect type hints
3. inspect control flow
4. inspect mutation sites
5. inspect reads and writes to globals, env, files, network, subprocesses, caches, logs, metrics, and locks
6. inspect validation and normalization logic
7. infer determinism, idempotency, concurrency, and security properties only when strongly supported
8. generate the minimal truthful summary line
9. generate the supported semantic block fields
10. generate `Parameters` and `Returns` or `Yields`
11. generate `Raises` only when operationally meaningful
12. add controlled-prefix comments only at non-obvious semantic boundaries
13. remove low-signal or stale comments

## Validation Checklist

Generated documentation is acceptable only if all of the following hold:

- NumPy-style section headers are valid where used
- parameter names exactly match the signature
- defaults do not contradict code
- return semantics do not contradict implementation
- raised exceptions are defensible
- side-effect claims are supported
- safety claims are supported
- concurrency claims are supported
- no speculative rationale is present
- no human-oriented filler is present
- comments add information not cheaply inferable from syntax
- the rewritten documentation is denser, not merely longer

## Final Rewrite Boundary

When applying this specification:

- modify only docstrings and comments unless explicitly instructed otherwise
- preserve runtime behavior
- preserve signatures
- preserve non-documentation formatting unless necessary for the documentation change
- prefer structure over prose
- prefer omission over speculation
