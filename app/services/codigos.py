from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Secuencia


def next_code(db: Session, prefijo: str, digitos: int, anio: int | None = None) -> str:
    """Genera un correlativo atómico por prefijo y año: ING-2026-00001."""
    anio = anio or datetime.now().year
    clave = f"{prefijo}-{anio}"
    seq = db.execute(select(Secuencia).where(Secuencia.prefijo == clave)).scalar_one_or_none()
    if seq is None:
        seq = Secuencia(prefijo=clave, ultimo=0)
        db.add(seq)
        db.flush()
    seq.ultimo += 1
    db.flush()
    return f"{clave}-{seq.ultimo:0{digitos}d}"
