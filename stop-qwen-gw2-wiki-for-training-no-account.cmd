@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Project Python environment is missing.
  pause
  exit /b 1
)
set "PYTHONPATH=%~dp0src"
".venv\Scripts\python.exe" -m waypoint.experiments.ocr_landmarks.text_training --stop
set "QWEN_TEST_EXIT=%ERRORLEVEL%"
pause
exit /b %QWEN_TEST_EXIT%
