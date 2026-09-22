@echo off
REM Doble clic para transcribir todo lo que haya en la carpeta Entrada.
REM Sin tildes a proposito: los .bat no las manejan bien en la consola.

chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"
title Transcriptor

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo  No se encontro Python en este computador.
    echo  Haga doble clic en "instalar (primera vez).bat" y siga las instrucciones.
    echo.
    pause
    exit /b 1
)

python transcribir.py %*
set CODIGO=%errorlevel%

echo.
echo ========================================
if not "%CODIGO%"=="0" (
    echo  Termino con avisos. Revise los mensajes de arriba.
)
pause
exit /b %CODIGO%
