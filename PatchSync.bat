@echo off
set FROM=D:\CPE\
set EXT=*.patch
set TO=D:\YandexDisk\HPE Patches\

for /f "tokens=* delims=" %%a in ('dir "%FROM%%EXT%" /s /b') do (
    call :SYNC "%%a"
)
goto :END

:SYNC
    set DESTFILE=%TO%%~nx1
    if exist "%DESTFILE%" (
        call :UPDATE %1 "%DESTFILE%"
    ) else (
        echo New: %1
        copy %1 "%TO%"
    )      
    goto :EOF   
    
:UPDATE
    set DATEONE=%~t1
    set DATETWO=%~t2
        if "%DATEONE%" == "%DATETWO%" (
            echo Up to date: %1
        ) else (
            echo Updated: %1
            copy %1 "%TO%"            
        ) 
    goto :EOF
    
:END
