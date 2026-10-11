@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run run-GW2-VLM-COPILOT.cmd first to complete source setup.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" "tools\run_gui.py" --vision-review
pause
