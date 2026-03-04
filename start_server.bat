@echo off
echo [Antigravity Architecture] Starting local development server...
echo Launching browser to view the workspace...
start http://localhost:8000/file-type-styling.html
echo Booting Python HTTP Server on port 8000.
echo IMPORTANT: Press Ctrl+C in this window to terminate gracefully when finished.
python -m http.server 8000
pause
