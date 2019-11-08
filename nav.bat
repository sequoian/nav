@echo off

REM This file should be used to call the nav python file

SET PYTHONFILE=navigate.py
SET PYTHONPATH=%~dp0\..\scripts\nav
SET CALLDIR=%CD%

cd %PYTHONPATH%
%PYTHONFILE% %CALLDIR% %*

REM Grab returned dir from file, delete file, and send user to that directory
SET /p FINALDIR= < tmp
del tmp
cd /d %FINALDIR%