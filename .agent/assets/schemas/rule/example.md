---
name: strict-python-architecture
description: Enforces deterministic type safety, non-blocking asynchronous I/O patterns, and explicit exception handling for all Python modules.
trigger: glob
globs: "*.py, src/**/*.py, scripts/**/*.py"
priority: critical
# HUMAN CONTEXT: This example demonstrates advanced agentic capabilities
# by utilizing progressive disclosure (injecting only when Python files are active via globs),
# deterministic conflict resolution (using critical priority to override generalized suggestions),
# and cognitive optimization (forcing Gemini 3.1 Pro into a silent reasoning loop to guarantee code compliance before output).
---

<constraints>
- **Type Safety Mandate:** All function signatures, including internal helpers and class methods, must have comprehensive type hints. Explicitly type `*args` and `**kwargs`. The use of implicit `Any` is prohibited.
- **Concurrency Protocol:** Do not use blocking synchronous libraries (e.g., `requests`, `time.sleep`) inside asynchronous event loops. You must utilize their asynchronous equivalents (e.g., `aiohttp`, `asyncio.sleep`).
- **Exception Handling:** Bare `except:` or `except Exception:` blocks are strictly prohibited. You must catch explicitly anticipated exception classes (e.g., `KeyError`, `aiohttp.ClientError`) and implement deterministic logging.
- **Data Validation:** All incoming external payloads or API responses must be parsed through `pydantic` BaseModel classes rather than raw dictionary manipulation.
- **No Elided Code:** Never generate placeholder comments like `# TODO: implement logic`. All emitted code must be production-ready, complete, and contextually aware of the surrounding implementation.
</constraints>

<verification_step>
SILENT VERIFICATION INSTRUCTIONS:
Before emitting the final codebase modification, you must internally evaluate your generated code against the following matrix:

1. Scan all newly generated `def` and `async def` statements to confirm complete and accurate type annotations.
2. Check the AST logic for any blocking I/O calls mistakenly placed within `async` blocks.
3. Verify that all `try/except` blocks target specific, named error classes.
4. Ensure no placeholder code or "dummy" variables have been utilized.

If any check fails, silently regenerate the code to correct the violation before finalizing the output artifact. Do not output your reasoning process or these validation steps to the user.
</verification_step>
