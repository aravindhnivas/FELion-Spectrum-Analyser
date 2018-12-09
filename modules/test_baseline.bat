@echo off

REM set root=C:\ProgramData\Anaconda3
REM set file=C:\FELion-GUI
REM call %root%\Scripts\activate.bat %root%

call activate base
call python GUI_Baseline.py

pause