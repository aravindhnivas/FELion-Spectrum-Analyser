@echo off

REM set root=C:\ProgramData\Anaconda3
REM set file=C:\FELion-GUI
REM call %root%\Scripts\activate.bat %root%

::call activate base
FOR /F "tokens=*" %%g IN ('where python') do (SET pythonpath=%%g)
echo %pythonpath%
%pythonpath% %cd%\GUI_Baseline.py

pause