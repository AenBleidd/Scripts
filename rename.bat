echo off
set /a NUMBER=1
for /r %%i in (*.jpg) do call :RENAME "%%i"
goto :END

:RENAME
set NEWNAME=000%NUMBER%
set NEWNAME=%NEWNAME:~-4%.tmpjpg
ren %1 %NEWNAME%
set /a NUMBER=NUMBER+1
goto :EOF

:END
ren *.tmpjpg *.jpg

:EOF