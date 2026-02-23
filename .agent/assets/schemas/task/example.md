---
task_id: "TASK-MAGGIE-003"
title: "Implement QThreadPool for background data fetching"
priority: "high"
target_model: "gemini-3-flash"
task_dependencies: ["TASK-MAGGIE-001"]
file_dependencies: ["src/ui/main_window.py"]
# HUMAN CONTEXT: This task artifact functions as the agent's dynamic state tracker.
# It enforces pre-execution dependency checks and explicit rollback procedures
# to ensure atomic execution without corrupting existing workspace files.
---

<expected_output>
A fully functional `src/core/worker.py` module containing a `QRunnable` subclass and a custom `QObject` signal class.
</expected_output>

<constraints>
- Use `logging` instead of `print()` statements for all background thread monitoring.
- Do not modify `src/ui/main_window.py` during this task; only establish the core worker logic.
</constraints>

<pre_check>
Verify that `PySide6` is actively installed in the current virtual environment and that `src/ui/main_window.py` exists as declared in the file dependencies.
</pre_check>

<acceptance_criteria>

- The `WorkerSignals` class defines at least `finished`, `error`, and `result` signals.
- The `Worker` class successfully inherits from `QRunnable` and implements the `@Slot()` decorator on its `run()` method.
- The file passes `ruff` static analysis without formatting errors.
</acceptance_criteria>

<rollback_procedure>
If `ruff` validation fails or syntax errors are detected, delete the newly created `src/core/worker.py` file, log the specific syntax failure, and halt the workflow to await human intervention.
</rollback_procedure>
