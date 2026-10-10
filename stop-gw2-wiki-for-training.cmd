@echo off
if not exist "%~dp0local-data\text-playtests" mkdir "%~dp0local-data\text-playtests"
type nul > "%~dp0local-data\text-playtests\STOP"
echo Stop requested. The active inference will finish before the owned engines close.
pause
