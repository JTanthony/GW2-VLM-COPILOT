@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" "tools\run_text_sessions.py" --account-mode saved
pause
