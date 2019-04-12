@echo off

:: To get Admin Access.

:: BatchGotAdmin
:-------------------------------------
::  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

:: --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:-------------------------------------- 

:: Installation Script

call activate base
call python -m pip install gitpython
call python -m pip install uncertainties

python compile.py
ROBOCOPY %cd%\modules C:\FELion-GUI\software

:: ####################
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "C:\FELion-GUI\software\FELion-GUI.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\FELion-GUI\software\Normline.bat" >> %SCRIPT%
echo oLink.IconLocation = "C:\FELion-GUI\software\FELion_Icon.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%
:: ####################


ROBOCOPY C:\FELion-GUI\software "C:\Users\Public\Desktop" FELion-GUI.lnk
ROBOCOPY C:\FELion-GUI\software "C:\ProgramData\Microsoft\Windows\Start Menu\Programs" FELion-GUI.lnk

echo "######################################################################################"
echo "Installation Completed: Shorcuts created on Desktop and Start Menu"
echo "Program Name: FELion-GUI"
echo "Direct Github latest version: https://github.com/aravindhnivas/FELion-Spectrum-Analyser"
echo "######################################################################################"

pause