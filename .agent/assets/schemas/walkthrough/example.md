<execution_summary>
The PySide6 asynchronous worker integration for the Maggie application has been successfully completed. The implementation decouples heavy data processing from the main event loop, ensuring the UI remains highly responsive during extended operations.
</execution_summary>

<architectural_changes>

- **Created:** `src/core/worker.py` - Contains the `QRunnable` architecture and custom signal definitions.
- **Modified:** `src/ui/main_window.py` - Instantiated `QThreadPool.globalInstance()` and connected the worker's `result` signal to the UI update slots.
- **Dependencies:** No external `pip` dependencies were added.
</architectural_changes>

<verification_steps>
To verify the implementation meets the required specifications, please perform the following actions:

1. Open the Antigravity Terminal and ensure your virtual environment is active.
2. Execute the application using: `python -m src.main`
3. Click the "Fetch Data" button on the Maggie dashboard.
4. Attempt to resize the application window while the data is fetching.
   - **Expected Result:** The window should resize smoothly without stuttering, and the fetched data should populate the table once the background thread emits the `result` signal.
</verification_steps>
