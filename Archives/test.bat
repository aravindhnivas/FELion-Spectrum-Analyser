for /F "tokens=1,3 delims=. " %%a in ("%string%") do (
   echo %%a
   echo %%b
)