@echo off
REM Instalacion de una sola vez. Doble clic y esperar.
REM Sin tildes a proposito: los .bat no las manejan bien en la consola.

chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"
title Transcriptor - instalacion

echo ============================================================
echo   Transcriptor - instalacion de una sola vez
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 goto sin_python

python -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"
if errorlevel 1 goto version_vieja

echo  Python encontrado:
python --version
echo.
echo  Instalando el motor de transcripcion. Esto baja unos 200 MB
echo  y puede tardar varios minutos. No cierre esta ventana.
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto fallo_pip

echo.
echo ============================================================
echo   Listo.
echo.
echo   Ahora ponga sus audios o videos en la carpeta Entrada
echo   y haga doble clic en "Transcribir (doble clic).bat".
echo.
echo   La primera transcripcion descarga el modelo (cerca de 1 GB)
echo   y por eso demora mas que las siguientes.
echo ============================================================
echo.
pause
exit /b 0

:sin_python
echo  No se encontro Python en este computador.
echo.
echo  1. Abra  https://www.python.org/downloads/
echo  2. Descargue Python para Windows e instalelo.
echo  3. IMPORTANTE: en la primera pantalla del instalador marque
echo     la casilla "Add python.exe to PATH".
echo  4. Cierre esta ventana y vuelva a hacer doble clic aqui.
echo.
pause
exit /b 1

:version_vieja
echo  La version de Python instalada es muy antigua:
python --version
echo.
echo  Instale una version 3.9 o mas nueva desde
echo  https://www.python.org/downloads/  (marque "Add python.exe to PATH").
echo.
pause
exit /b 1

:fallo_pip
echo.
echo  Fallo la instalacion. Copie el mensaje de error de arriba
echo  y pidale ayuda a quien le compartio esta carpeta.
echo.
pause
exit /b 1
