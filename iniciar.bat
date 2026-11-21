@echo off
setlocal EnableDelayedExpansion
title Electrogreem - Inventario
cd /d "%~dp0"

echo ============================================================
echo   Electrogreem - Inventario - Gestion integral de RAEE
echo   Tucuman, Argentina
echo ============================================================
echo.

rem ---------- 1. Detectar Python ----------
set "PYCMD="
where py >nul 2>&1
if !errorlevel! EQU 0 (
  py -3 -c "import sys" >nul 2>&1
  if !errorlevel! EQU 0 set "PYCMD=py -3"
)
if not defined PYCMD (
  where python >nul 2>&1
  if !errorlevel! EQU 0 (
    python -c "import sys" >nul 2>&1
    if !errorlevel! EQU 0 set "PYCMD=python"
  )
)
if not defined PYCMD (
  echo [ERROR] No se encontro Python 3.
  echo Instale Python 3.10 o superior desde https://www.python.org/downloads/
  echo y asegurese de marcar "Add Python to PATH" durante la instalacion.
  pause
  exit /b 1
)

%PYCMD% -c "import sys;sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if !errorlevel! EQU 1 (
  echo [ERROR] Se requiere Python 3.10 o superior.
  pause
  exit /b 1
)
echo [OK] Python detectado: %PYCMD%

rem ---------- 2. Entorno virtual ----------
if not exist ".venv\Scripts\python.exe" (
  echo Creando entorno virtual .venv ...
  %PYCMD% -m venv .venv
  if !errorlevel! NEQ 0 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
  )
)
set "VPY=.venv\Scripts\python.exe"

rem ---------- 3. Dependencias (solo si faltan o cambio requirements.txt) ----------
set "NEED_INSTALL=0"
if not exist ".venv\requirements.installed" set "NEED_INSTALL=1"
if "%NEED_INSTALL%"=="0" (
  fc /b requirements.txt .venv\requirements.installed >nul 2>&1
  if !errorlevel! NEQ 0 set "NEED_INSTALL=1"
)
if "%NEED_INSTALL%"=="1" (
  echo Instalando dependencias desde requirements.txt ...
  "%VPY%" -m pip install --upgrade pip
  "%VPY%" -m pip install -r requirements.txt
  if !errorlevel! NEQ 0 (
    echo [ERROR] No se pudieron instalar las dependencias.
    echo Si no hay conexion a internet, instale los paquetes manualmente en .venv.
    pause
    exit /b 1
  )
  copy /y requirements.txt .venv\requirements.installed >nul
  echo [OK] Dependencias instaladas.
) else (
  echo [OK] Dependencias ya disponibles.
)

rem ---------- 4. Base de datos ----------
if not exist "data\raee.db" (
  echo Inicializando base de datos local ^(sin datos de demostracion^) ...
  "%VPY%" scripts/init_db.py --no-demo
  if !errorlevel! NEQ 0 (
    echo [ERROR] No se pudo inicializar la base de datos.
    pause
    exit /b 1
  )
) else (
  echo [OK] Base de datos encontrada.
)

rem ---------- 5. IP de red local ----------
set "LANIP=127.0.0.1"
for /f "delims=" %%i in ('"%VPY%" scripts/local_ip.py 2^>nul') do set "LANIP=%%i"

echo.
echo ------------------------------------------------------------
echo   Servidor listo en el puerto 8000
echo   Acceso local : http://localhost:8000
echo   Acceso LAN   : http://%LANIP%:8000
echo   Para detener : Ctrl + C
echo   Minimice esta ventana; no la cierre con la X.
echo ------------------------------------------------------------
echo.

set "PYTHONUNBUFFERED=1"
"%VPY%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000

echo.
echo El servidor se ha detenido.
pause
