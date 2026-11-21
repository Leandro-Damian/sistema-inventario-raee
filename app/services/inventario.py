from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Ingreso, Item, ItemEspecificacion
from app.services.codigos import next_code


def crear_items(
    db: Session,
    ingreso: Ingreso,
    categoria: str,
    marca: str,
    modelo: str,
    cantidad: int,
    peso_unitario: float,
    atributos: list[tuple[str, str]] | None = None,
    subcategoria: str = "",
    estado: str = "En recepción",
    origen_id: int | None = None,
    fecha: datetime | None = None,
    ficha_storage: dict | None = None,
) -> list[Item]:
    """Crea N ítems unitarios correlativos a partir de una carga rápida."""
    cantidad = max(1, int(cantidad))
    fecha = fecha or ingreso.fecha_retiro
    ficha_storage = ficha_storage or {}
    creados: list[Item] = []

    for _ in range(cantidad):
        item = Item(
            codigo=next_code(db, "RAEE", 6, fecha.year),
            ingreso_id=ingreso.id,
            categoria=categoria,
            subcategoria=subcategoria or "",
            marca=marca or "",
            modelo=modelo or "",
            peso_unitario=float(peso_unitario or 0),
            estado=estado,
            fecha=fecha,
            origen_id=origen_id,
            numero_serie=ficha_storage.get("numero_serie", ""),
            tipo_unidad=ficha_storage.get("tipo_unidad", ""),
            factor_forma=ficha_storage.get("factor_forma", ""),
            interfaz=ficha_storage.get("interfaz", ""),
            capacidad=ficha_storage.get("capacidad", ""),
            salud_smart=ficha_storage.get("salud_smart", ""),
            disposicion=ficha_storage.get("disposicion", ""),
        )
        db.add(item)
        db.flush()
        for clave, valor in atributos or []:
            if clave and clave.strip():
                db.add(ItemEspecificacion(item_id=item.id, clave=clave.strip(), valor=(valor or "").strip()))
        creados.append(item)

    db.flush()
    return creados
