@echo off
setlocal
set "RESEARCHCTL_SCRIPT=%~dp0..\scripts\researchctl.py"
python "%RESEARCHCTL_SCRIPT%" %*
exit /b %ERRORLEVEL%
