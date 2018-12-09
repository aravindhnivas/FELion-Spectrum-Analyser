@echo off

REM set root=C:\ProgramData\Anaconda3
set file=C:\FELion-GUI
REM call %root%\Scripts\activate.bat %root%
call activate base
call python %file%\GUI_Normline.py

pause