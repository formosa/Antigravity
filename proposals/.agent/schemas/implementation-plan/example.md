---
task: "Architect and implement the main dashboard layout for Maggie"
model: "gemini-3.1-pro-preview"
version: "1.0.0"
output_path: ".agent/plans/20260401-090000-c7f3a1b2-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260401-090000-c7f3a1b2-IMPLEMENTATION_PLAN.md"
# HUMAN CONTEXT: This artifact enforces split-step verification by requiring the agent
# to blueprint the Maggie PySide6 dashboard architecture and explicitly await
# human approval before initiating any code generation or file modifications.
# Upon executor confirmation of all steps and verification checks, this file
# must be relocated to the processed_path above.
---

<objective>
Construct the primary PySide6 dashboard interface for the Maggie application, establishing a non-blocking UI architecture utilizing QGridLayout and dynamic widget loading.
</objective>

<phases>
- phase_id: "PHASE_1_UI_SCAFFOLD"
  objectives:
    - "Establish base QMainWindow"
    - "Configure QGridLayout for dynamic resizing"
  task_references: ["TASK-MAGGIE-001", "TASK-MAGGIE-002"]
  entry_criteria:
    - "PySide6 environment verified"
  exit_criteria:
    - "Base window renders without errors"
  assigned_model: "gemini-3.1-pro-preview"

- phase_id: "PHASE_2_ASYNC_WORKERS"
  objectives:
  - "Implement QThreadPool for background data fetching"
  - "Bind worker signals to dashboard slots"
  task_references: ["TASK-MAGGIE-003"]
  entry_criteria:
  - "PHASE_1_UI_SCAFFOLD complete and exit criteria verified"
  exit_criteria:
  - "Background tasks update UI without blocking the main event loop"
  assigned_model: "gemini-3-flash"
</phases>

<atomic_steps>

#### Group 1 — UI Scaffold (PHASE_1_UI_SCAFFOLD)

- [ ] 1. CREATE `src/ui/main_window.py` containing the `MaggieDashboard` class inheriting from `QMainWindow`, establishing the application's primary window surface.
- [ ] 2. MODIFY `MaggieDashboard.__init__` to call `setup_ui()`, which instantiates a `QGridLayout` with column and row stretch factors configured for dynamic resizing.

#### Group 2 — Async Worker Infrastructure (PHASE_2_ASYNC_WORKERS)

- [ ] 3. CREATE `src/core/worker.py` subclassing `QRunnable` to encapsulate asynchronous background tasks; define a `WorkerSignals` class for type-safe signal emission.
- [ ] 4. MODIFY `MaggieDashboard` to accept and connect `WorkerSignals` slots, ensuring all UI update calls originate from the main thread via Qt's signal-slot mechanism.

</atomic_steps>

<verification>

1. Inspect `src/ui/main_window.py`: confirm valid PySide6 imports, `MaggieDashboard(QMainWindow)` class definition, and zero syntax errors via `python -m py_compile src/ui/main_window.py`.
2. Launch the application and manually resize the window; verify `QGridLayout` columns and rows scale proportionally without clipping or overflow.
3. Inspect `src/core/worker.py`: confirm `QRunnable` subclass, `WorkerSignals(QObject)` definition, and at least one typed signal (e.g., `result = Signal(object)`).
4. Run the application and trigger a background task; verify `WorkerSignals` emission updates the target UI widget without raising a `QThread` cross-thread violation exception in the console.

</verification>

<risks_and_mitigations>

- **Risk:** Cross-thread UI updates causing application crashes or silent data corruption.
  **Mitigation:** Strictly enforce the Qt Signals and Slots mechanism for all data passed from `QRunnable` workers to the main GUI thread. Direct attribute mutation from a worker thread is prohibited.

- **Risk:** `QGridLayout` stretch configuration producing layout instability on high-DPI displays.
  **Mitigation:** Validate layout behavior at 100%, 125%, and 150% DPI scaling during PHASE_1 exit verification before proceeding to PHASE_2.

</risks_and_mitigations>
