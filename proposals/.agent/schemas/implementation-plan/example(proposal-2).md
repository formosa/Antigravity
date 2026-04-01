---
task: "Architect and implement the main dashboard layout for Maggie"
model: "gemini-3.1-pro-preview"
version: "1.0.0"
thinking_level: "HIGH"
# HUMAN CONTEXT: This artifact enforces split-step verification by requiring the agent
# to blueprint the Maggie PySide6 dashboard architecture and explicitly await
# human approval before initiating any code generation or file modifications.
# Stored at: .agent/plans/20260401-143022-a3f7c12b-IMPLEMENTATION_PLAN.md
---

<objective>
Construct the primary PySide6 dashboard interface for the Maggie application, establishing a non-blocking UI architecture utilizing QGridLayout and dynamic widget loading.
</objective>

<phases>
- phase_id: "PHASE_1_UI_SCAFFOLD"
  objectives: ["Establish base QMainWindow", "Configure QGridLayout for dynamic resizing"]
  task_references: ["TASK-MAGGIE-001", "TASK-MAGGIE-002"]
  entry_criteria: ["PySide6 environment verified"]
  exit_criteria: ["Base window renders without errors"]
  assigned_model: "gemini-3.1-pro-preview"
- phase_id: "PHASE_2_ASYNC_WORKERS"
  objectives: ["Implement QThreadPool for background data fetching"]
  task_references: ["TASK-MAGGIE-003"]
  entry_criteria: ["PHASE_1_UI_SCAFFOLD complete"]
  exit_criteria: ["Background tasks update UI without blocking the main event loop"]
  assigned_model: "gemini-3-flash"
</phases>

<atomic_steps>

### PHASE 1 — UI Scaffold

- [ ] Step 1 — CREATE `src/ui/main_window.py` containing the `MaggieDashboard` class inheriting from `QMainWindow`.
- [ ] Step 2 — MODIFY `MaggieDashboard` to implement `setup_ui()`, instantiating a responsive `QGridLayout`.

### PHASE 2 — Async Workers

- [ ] Step 3 — CREATE `src/core/worker.py` subclassing `QRunnable` for asynchronous event handling.
- [ ] Step 4 — MODIFY `MaggieDashboard` to bind signals from the worker to slots, enabling safe UI updates from background threads.

</atomic_steps>

<verification>

1. Verify `main_window.py` contains valid PySide6 imports and passes syntax check (`python -m py_compile src/ui/main_window.py`).
2. Verify grid layout parameters scale correctly during window resize events via manual inspection of resize behavior.
3. Verify `QRunnable` instances successfully execute external bound methods via unit test assertion.
4. Verify signal emission triggers UI updates without raising `QThread` cross-thread violation exceptions during a 30-second integration run.

</verification>

<risks_and_mitigations>

- **Risk:** Cross-thread UI updates causing application crashes.
  **Mitigation:** Strictly enforce the use of Qt Signals and Slots for all data passed from background threads to the main GUI thread.

</risks_and_mitigations>

<!-- LARGE-CONTEXT ANCHOR: Objective restatement for executor attention -->
<!-- Task: Construct the primary PySide6 dashboard for Maggie using QMainWindow + QGridLayout + QThreadPool. -->
<!-- All steps must remain scoped to src/ui/main_window.py and src/core/worker.py. -->
