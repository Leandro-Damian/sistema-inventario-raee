#!/usr/bin/env python3
"""Inicializa la base de datos local de RAEE.

Uso:
    python scripts/init_db.py              # catálogos + datos de demostración
    python scripts/init_db.py --no-demo    # solo catálogos y factores base
    python scripts/init_db.py --reset      # recrea la base desde cero
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import DB_PATH  # noqa: E402
from app.database import SessionLocal, create_tables, reset_tables  # noqa: E402
from app.seed import seed_catalogos, seed_demo  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicializar base de datos RAEE")
    parser.add_argument("--no-demo", action="store_true", help="No cargar registros ficticios")
    parser.add_argument("--reset", action="store_true", help="Recrear la base de datos")
    args = parser.parse_args()

    if args.reset:
        respuesta = input(" Esto borrará todos los datos. ¿Continuar? [s/N]: ").strip().lower()
        if respuesta not in ("s", "si", "sí", "y", "yes"):
            print(" Operación cancelada.")
            return 0
        reset_tables()
        print(" Base recreada.")
    else:
        create_tables()

    with SessionLocal() as db:
        seed_catalogos(db)
        if not args.no_demo:
            seed_demo(db)

    print(f" Base lista: {DB_PATH}")
    if args.no_demo:
        print(" Catálogos y factores base cargados (sin datos de demostración).")
    else:
        print(" Datos de demostración cargados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
