---
task: "Architect and implement the main dashboard layout for Maggie"
model: "gemini-3.1-pro"
version: "1.0.0"
# HUMAN CONTEXT: This artifact enforces split-step verification by requiring the agent
# to blueprint the Maggie PySide6 dashboard architecture and explicitly await
# human approval before initiating any code generation or file modifications.
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
  assigned_model: "gemini-3.1-pro"
- phase_id: "PHASE_2_ASYNC_WORKERS"
  objectives: ["Implement QThreadPool for background data fetching"]
  task_references: ["TASK-MAGGIE-003"]
  entry_criteria: ["PHASE_1_UI_SCAFFOLD complete"]
  exit_criteria: ["Background tasks update UI without blocking the main event loop"]
  assigned_model: "gemini-3-flash"
</phases>

<atomic_steps>

1. Generate `src/ui/main_window.py` containing the `MaggieDashboard` class inheriting from `QMainWindow`.
2. Implement `setup_ui()` to instantiate a responsive `QGridLayout`.
3. Create `src/core/worker.py` to subclass `QRunnable` for asynchronous event handling.
4. Bind signals from the worker to slots in `MaggieDashboard` to update UI elements safely.

</atomic_steps>

<verification>

1. Verify `main_window.py` contains valid PySide6 imports and no syntax errors.
2. Verify grid layout parameters scale correctly during window resize events.
3. Verify `QRunnable` instances successfully execute external bound methods.
4. Verify signal emission triggers UI updates without raising `QThread` cross-thread violation exceptions.

</verification>

<risks_and_mitigations>

- **Risk:** Cross-thread UI updates causing application crashes.
  **Mitigation:** Strictly enforce the use of Qt Signals and Slots for all data passed from background threads to the main GUI thread.

</risks_and_mitigations>
