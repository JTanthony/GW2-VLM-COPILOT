@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" goto setup_environment
".venv\Scripts\python.exe" -c "import tkinter, numpy, cv2, windows_capture" >nul 2>&1
if errorlevel 1 goto setup_environment
:launch
".venv\Scripts\python.exe" "tools\run_gui.py"
if errorlevel 1 (
  echo.
  echo GW2 VLM COPILOT could not start. See the error above.
  pause
)
exit /b

:setup_environment
echo First-time source setup requires Python 3.12 and an internet connection.
echo This will create a project-local Python environment and install
echo the dependencies listed in requirements.txt. No models are downloaded.
choice /c YN /n /m "Set up this source project now? [Y/N] "
if errorlevel 2 exit /b 0
if exist ".venv\Scripts\python.exe" goto install_dependencies
py -3.12 -c "import tkinter" >nul 2>&1
if errorlevel 1 goto missing_python
py -3.12 -m venv .venv
if errorlevel 1 goto setup_failed
:install_dependencies
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto setup_failed
".venv\Scripts\python.exe" -c "import tkinter, numpy, cv2, windows_capture"
if errorlevel 1 goto setup_failed
goto launch

:missing_python
echo Install 64-bit Python 3.12 from https://www.python.org/downloads/windows/
echo Include the Python launcher and Tcl/Tk, then run this file again.
echo Alternatively, use GW2-VLM-COPILOT.exe from the Windows release ZIP.
pause
exit /b 1

:setup_failed
echo Setup did not finish. See the error above and docs\SETUP.md.
pause
exit /b 1
