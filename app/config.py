from __future__ import annotations

import os
from pathlib import Path

# Metadato interno del proyecto. No se muestra en la interfaz.
AUTHOR = "Leandro Damian Chumbita - Técnico Superior en Programación"
AUTHOR_META_CONTENT = AUTHOR

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ATTACHMENTS_DIR = DATA_DIR / "adjuntos"
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

DB_PATH = Path(os.getenv("RAEE_DB_PATH", str(DATA_DIR / "raee.db")))

APP_NAME = "Electrogreem - Inventario"
APP_SUBTITLE = "Gestión integral de RAEE"
APP_LOCALITY = "Tucumán, Argentina"
HOST = "0.0.0.0"
PORT = 8000
MAX_UPLOAD_MB = 10
