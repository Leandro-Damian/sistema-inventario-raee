#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo "  Electrogreem - Inventario - Gestion integral de RAEE"
echo "  Tucuman, Argentina"
echo "============================================================"
echo

if command -v python3 >/dev/null 2>&1; then
  PYCMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYCMD="python"
else
  echo "[ERROR] No se encontro Python 3."
  exit 1
fi

if ! "$PYCMD" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'; then
  echo "[ERROR] Se requiere Python 3.10 o superior."
  exit 1
fi
echo "[OK] Python detectado: $PYCMD"

if [ ! -x ".venv/bin/python" ]; then
  echo "Creando entorno virtual .venv ..."
  "$PYCMD" -m venv .venv
fi
VPY=".venv/bin/python"

if [ ! -f ".venv/requirements.installed" ] || ! cmp -s requirements.txt .venv/requirements.installed; then
  echo "Instalando dependencias desde requirements.txt ..."
  "$VPY" -m pip install --upgrade pip
  "$VPY" -m pip install -r requirements.txt
  cp requirements.txt .venv/requirements.installed
  echo "[OK] Dependencias instaladas."
else
  echo "[OK] Dependencias ya disponibles."
fi

if [ ! -f "data/raee.db" ]; then
  echo "Inicializando base de datos local (sin datos de demostracion) ..."
  "$VPY" scripts/init_db.py --no-demo
else
  echo "[OK] Base de datos encontrada."
fi

LANIP=$("$VPY" scripts/local_ip.py 2>/dev/null || echo "127.0.0.1")

echo
echo "------------------------------------------------------------"
echo "  Servidor listo en el puerto 8000"
echo "  Acceso local : http://localhost:8000"
echo "  Acceso LAN   : http://${LANIP}:8000"
echo "  Para detener : Ctrl + C"
echo "  Minimice esta ventana; no la cierre con la X."
echo "------------------------------------------------------------"
echo

export PYTHONUNBUFFERED=1
exec "$VPY" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
