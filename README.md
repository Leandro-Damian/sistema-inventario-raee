# Electrogreem - Inventario — Gestión integral de RAEE

Aplicación web local para gestión, inventario y trazabilidad de Residuos de Aparatos Eléctricos y Electrónicos. Funciona en red local (LAN) en Windows 10/11 y Linux, sin conexión a internet en tiempo de ejecución.

## Arranque rápido (Windows 10 / 11)

1. Copiá la carpeta del proyecto donde quieras (por ejemplo `C:\Electrogreem`).
2. Doble clic en **`iniciar.bat`**.
3. Esperá a que la consola muestre la IP de red local y abrí en un navegador:

```
http://localhost:8000
http://<IP-LAN>:8000
```

El script crea automáticamente `.venv`, instala dependencias si faltan, genera `data/raee.db` con catálogos base (sin datos ficticios) y levanta el servidor en `0.0.0.0:8000`.

Para detener: `Ctrl + C` en la consola.

## Linux

```bash
chmod +x iniciar.sh
./iniciar.sh
```

## Base de datos

```bash
python scripts/init_db.py --no-demo   # solo catálogos y factores base
python scripts/init_db.py             # catálogos + datos de demostración
python scripts/init_db.py --reset     # recrear desde cero (pide confirmación)
```

## Tests

```bash
python -m pytest -q
```

## Estructura

- `app/`: backend FastAPI, modelos SQLAlchemy, servicios, routers, plantillas Jinja2 y estáticos.
- `app/static/css/app.css`: Tailwind compilado localmente (sin CDN).
- `app/static/js/alpine.min.js`: Alpine.js vendorizado (sin CDN).
- `scripts/`: inicialización de base de datos.
- `tests/`: suite completa de pytest.
- `MANUAL_USUARIO.md`: manual de operatoria diaria (también accesible desde el menú lateral).

## Datos

Toda la información queda en `data/raee.db` y los comprobantes adjuntos en `data/adjuntos/`. Realizá copias de seguridad de la carpeta `data/` completa.
