@echo off

set file=C:\FELion-GUI\software
::IF EXIST C:\FELion_update_cache del C:\FELion_update_cache
call activate base
call python %file%\FELion_GUI_Baseline_v2.py

pause