@echo off
echo [Antigravity Architecture] Scanning for orphaned Python server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    if not "%%a"=="0" (
        echo Targeted Process ID identified: %%a. Executing termination sequence...
        taskkill /F /PID %%a
        echo Process %%a successfully terminated. Port 8000 is now free.
        goto :EOF
    )
)
echo No active process found binding to port 8000. Workspace is clean.
pause
