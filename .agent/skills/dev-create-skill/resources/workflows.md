<document_purpose>
This document establishes the patterns for authoring deterministic workflows for Gemini 3.1 Pro inside the Antigravity IDE v1.20.3.
</document_purpose>

<decision_tree_patterns>
For complex tasks with branching logic, you MUST implement Explicit Decision Trees. This prevents the LLM from hallucinating fallbacks.

Example implementation inside a `<how_to_use>` block:

1. **Analyze Dependency Tree:**
   - **IF** the package is missing, **THEN** execute the installation script and log the change.
   - **IF** the package exists but is outdated, **THEN** prompt the human developer for upgrade approval.
   - **IF** the package is current, **THEN** proceed to Step 2.
</decision_tree_patterns>

<silent_reasoning_patterns>
To force Gemini 3.1 Pro to evaluate its own work before modifying the codebase, implement a silent verification loop using the `<verification_step>` tag.

Example implementation:
<verification_step>
SILENT AUDIT: Before emitting the final code block, silently review your AST structure. If any synchronous blocking I/O calls are detected within the `async` function, silently rewrite the function to use `aiohttp` before presenting the final output to the user.
</verification_step>
</silent_reasoning_patterns>
