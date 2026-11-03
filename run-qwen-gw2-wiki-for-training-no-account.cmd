@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python setup is missing. Run run-GW2-VLM-COPILOT.cmd first.
  pause
  exit /b 1
)
set "PYTHONPATH=%~dp0src"
".venv\Scripts\python.exe" -m waypoint.experiments.ocr_landmarks.text_training --hours 8 --turns 5 --sessions 1000 %*
set "QWEN_TEST_EXIT=%ERRORLEVEL%"
pause
exit /b %QWEN_TEST_EXIT%
