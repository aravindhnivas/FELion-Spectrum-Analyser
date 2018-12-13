@echo off

IF EXIST C:\ProgramData\Anaconda3 (
    ECHO Anaconda3 exist: Success.
    call activate base
    python ..\GUI_Normline.py
) ELSE echo Anaconda3 is not installed

pause
