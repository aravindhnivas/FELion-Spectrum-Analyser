@echo off

IF EXIST C:\ProgramData\Anaconda3 (
    ECHO Anaconda3 exist: Success.
    call activate base
    python %cd%\GUI_Baseline.py
) ELSE echo Anaconda3 is not installed

pause
