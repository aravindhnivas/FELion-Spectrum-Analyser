REM It just copy all the files in this directory to a location
REM and add that path into the system variable:

@echo off
ROBOCOPY . C:\FELion-GUI
IF EXIST C:\FELion-GUI set PATH = %PATH%;C:\FELion-GUI

REM ####################
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\FELion-Normline.lnk" >> %SCRIPT%
echo sLinkFile = "C:\FELion-GUI\FELion-Normline.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\FELion-GUI\Normline.bat" >> %SCRIPT%
echo oLink.IconLocation = "C:\FELion-GUI\FELion_Icon.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

REM ####################
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\FELion-Baseline.lnk" >> %SCRIPT%
echo sLinkFile = "C:\FELion-GUI\FELion-Baseline.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\FELion-GUI\Baseline.bat" >> %SCRIPT%
echo oLink.IconLocation = "C:\FELion-GUI\FELion_Icon.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%
REM This will create myshortcut.lnk on the Desktop, pointing to D:\myfile.extension.
REM ####################
pause