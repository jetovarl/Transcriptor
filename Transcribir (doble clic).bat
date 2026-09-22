@echo off
REM Doble clic para transcribir todo lo que haya en la carpeta Entrada.
REM Sin tildes a proposito: los .bat no las manejan bien en la consola.

chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"
title Transcriptor
setlocal enabledelayedexpansion

where python >nul 2>nul
if errorlevel 1 goto sin_python

REM Si le pasaron opciones al .bat, se respetan y no se muestra el menu.
if not "%~1"=="" goto correr_directo

if not exist "Entrada" mkdir "Entrada"
REM El conteo lo hace el propio script, que sabe cuales archivos son audio o video.
set CUANTOS=0
for /f %%N in ('python transcribir.py --contar 2^>nul') do set CUANTOS=%%N
if "%CUANTOS%"=="0" goto entrada_vacia

echo.
echo ============================================================
echo   TRANSCRIPTOR
echo ============================================================
echo.
echo   Audios o videos listos para transcribir: %CUANTOS%
echo.
echo   Que quiere hacer?
echo.
echo     [Enter]   Transcribir ya  -  espanol, rapido
echo        2      Maxima precision  -  mas lento, para audio dificil
echo        3      El audio no esta en espanol
echo        4      Texto con marcas de tiempo  [hh:mm:ss]
echo.

set OPCION=
set /p OPCION=  Escriba el numero y pulse Enter, o solo Enter:

if "%OPCION%"=="2" set EXTRA=--model large-v3& goto listo
if "%OPCION%"=="3" goto pedir_idioma
if "%OPCION%"=="4" set EXTRA=--con-tiempos& goto listo
set EXTRA=
goto listo

:pedir_idioma
echo.
echo   Escriba el codigo del idioma:  en  ingles    pt  portugues
echo                                  fr  frances   it  italiano
echo   o escriba  auto  para que lo detecte solo.
echo.
set IDIOMA=auto
set /p IDIOMA=  Idioma [auto]:
set EXTRA=--lang %IDIOMA%
goto listo

:listo
echo.
echo ------------------------------------------------------------
python transcribir.py %EXTRA%
set CODIGO=%errorlevel%
goto terminar

:correr_directo
python transcribir.py %*
set CODIGO=%errorlevel%
goto terminar

:terminar
echo.
echo ============================================================
if "%CODIGO%"=="0" goto todo_bien
echo   Termino con avisos. Revise los mensajes de arriba.
echo.
pause
exit /b %CODIGO%

:todo_bien
echo   Listo. Se abre la carpeta Salida con los textos.
start "" "%~dp0Salida"
echo.
pause
exit /b 0

:entrada_vacia
echo.
echo ============================================================
echo   No hay audios ni videos en la carpeta Entrada.
echo.
echo   Copie ahi sus grabaciones y vuelva a hacer doble clic.
echo   Se abre la carpeta Entrada.
echo ============================================================
start "" "%~dp0Entrada"
echo.
pause
exit /b 0

:sin_python
echo.
echo   No se encontro Python en este computador.
echo   Haga doble clic en "instalar (primera vez).bat" y siga las instrucciones.
echo.
pause
exit /b 1
