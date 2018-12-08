@echo off

set root=C:\ProgramData\Anaconda3
set file=C:\FELion-GUI
call %root%\Scripts\activate.bat %root%
call python %file%\GUI_NormAvg.py

pause