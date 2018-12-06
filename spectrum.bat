@echo off
set root=C:\ProgramData\Anaconda3
set file=D:\Work\RU\pythonScripts\FELion-Spectrum-Analyser
call %root%\Scripts\activate.bat %root%
call pushd %cd%
start python %file%\GUI_Baseline.py
start python %file%\GUI_NormAvg.py

pause