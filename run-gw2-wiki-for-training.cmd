@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python setup is missing. Run run-GW2-VLM-COPILOT.cmd first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" "tools\run_text_sessions.py" --account-mode saved --game "Guild Wars 2" --hours 3 --turns 5 --sessions 1000
pause
