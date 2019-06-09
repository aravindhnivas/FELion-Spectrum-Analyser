@echo off

set file=C:\FELion-GUI\software
IF EXIST C:\FELion_update_cache rmdir /Q /S C:\FELion_update_cache

call activate base
call python %file%\FELion_GUI_v3.py

pause