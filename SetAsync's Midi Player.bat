@echo off
:start
color 3
py core.py
color 4
echo The main python file has closed. Hit return to restart.
pause
goto start
