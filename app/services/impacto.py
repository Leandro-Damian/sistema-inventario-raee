from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import (
    FACTORES_CO2E_POR_CATEGORIA,
    KG_CO2E_POR_ARBOL_ANIO,
    KG_CO2E_POR_KM_AUTO,
)
from app.models import Item, MovimientoMaterial, TipoMaterial


def _en_rango(fecha: datetime | None, desde: datetime | None, hasta: datetime | None) -> bool:
    if fecha is None:
        return False
    if desde is not None and fecha < desde:
        return False
    if hasta is not None and fecha > hasta:
        return False
    return True


def calcular_impacto(
    db: Session,
    desde: datetime | None = None,
    hasta: datetime | None = None,
) -> dict:
    """CO2e evitado con enfoque de economía circular.

    1) Reutilización y donación: ítems Recuperados o Donados por categoría.
    2) Reciclaje y valorización: kg de materiales recuperados por su factor.
    """
    items = db.scalars(select(Item).where(Item.estado.in_(["Recuperado", "Donado"]))).all()

    reutilizacion = 0.0
    detalle_reutilizacion: dict[str, dict] = {}
    items_donados = 0
    items_recuperados = 0

    for it in items:
        fecha = it.fecha_donacion if it.estado == "Donado" else it.fecha
        if not _en_rango(fecha, desde, hasta):
            continue
        factor = FACTORES_CO2E_POR_CATEGORIA.get(it.categoria, 10.0)
        reutilizacion += factor
        bucket = detalle_reutilizacion.setdefault(
            it.categoria, {"categoria": it.categoria, "cantidad": 0, "co2e": 0.0, "factor": factor}
        )
        bucket["cantidad"] += 1
        bucket["co2e"] += factor
        if it.estado == "Donado":
            items_donados += 1
        else:
            items_recuperados += 1

    movimientos = db.scalars(
        select(MovimientoMaterial).where(MovimientoMaterial.tipo == "alta")
    ).all()
    tipos = {t.id: t for t in db.scalars(select(TipoMaterial)).all()}

    reciclaje = 0.0
    detalle_reciclaje: dict[str, dict] = {}
    kg_materiales = 0.0
    for mov in movimientos:
        if not _en_rango(mov.fecha, desde, hasta):
            continue
        tipo = tipos.get(mov.tipo_material_id)
        if tipo is None:
            continue
        co2e = mov.kg * tipo.factor_co2e
        reciclaje += co2e
        kg_materiales += mov.kg
        bucket = detalle_reciclaje.setdefault(
            tipo.nombre, {"material": tipo.nombre, "kg": 0.0, "co2e": 0.0, "factor": tipo.factor_co2e}
        )
        bucket["kg"] += mov.kg
        bucket["co2e"] += co2e

    total = reutilizacion + reciclaje
    return {
        "desde": desde,
        "hasta": hasta,
        "reutilizacion": reutilizacion,
        "reciclaje": reciclaje,
        "total": total,
        "detalle_reutilizacion": sorted(
            detalle_reutilizacion.values(), key=lambda x: x["co2e"], reverse=True
        ),
        "detalle_reciclaje": sorted(
            detalle_reciclaje.values(), key=lambda x: x["co2e"], reverse=True
        ),
        "items_donados": items_donados,
        "items_recuperados": items_recuperados,
        "kg_materiales": kg_materiales,
        "arboles": total / KG_CO2E_POR_ARBOL_ANIO,
        "km_auto": total / KG_CO2E_POR_KM_AUTO,
    }
