from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.constants import ESTADOS, ESTADOS_STOCK_ACTIVO
from app.database import get_db
from app.models import Donacion, Ingreso, Item, MovimientoMaterial
from app.services.impacto import calcular_impacto
from app.templating import page

router = APIRouter()


@router.get("/")
def panel(request: Request, db: Session = Depends(get_db)):
    total_items = db.scalar(select(func.count(Item.id))) or 0
    stock_activo = (
        db.scalar(select(func.count(Item.id)).where(Item.estado.in_(ESTADOS_STOCK_ACTIVO))) or 0
    )
    peso_total = db.scalar(select(func.coalesce(func.sum(Item.peso_unitario), 0.0))) or 0.0
    donados = db.scalar(select(func.count(Item.id)).where(Item.estado == "Donado")) or 0
    materiales_kg = (
        db.scalar(
            select(func.coalesce(func.sum(MovimientoMaterial.kg), 0.0)).where(
                MovimientoMaterial.tipo == "alta"
            )
        )
        or 0.0
    )
    impacto = calcular_impacto(db)

    por_estado_raw = dict(db.execute(select(Item.estado, func.count(Item.id)).group_by(Item.estado)).all())
    por_estado = [{"estado": e, "cantidad": por_estado_raw.get(e, 0)} for e in ESTADOS]

    top_categorias = [
        {"categoria": c or "Sin categoría", "cantidad": n}
        for c, n in db.execute(
            select(Item.categoria, func.count(Item.id))
            .group_by(Item.categoria)
            .order_by(func.count(Item.id).desc())
            .limit(6)
        ).all()
    ]

    ultimos_ingresos = db.scalars(
        select(Ingreso).order_by(Ingreso.fecha_retiro.desc()).limit(5)
    ).all()
    ultimas_donaciones = db.scalars(
        select(Donacion).order_by(Donacion.fecha.desc()).limit(5)
    ).all()

    return page(
        request,
        "panel.html",
        total_items=total_items,
        stock_activo=stock_activo,
        peso_total=peso_total,
        donados=donados,
        materiales_kg=materiales_kg,
        impacto=impacto,
        por_estado=por_estado,
        top_categorias=top_categorias,
        ultimos_ingresos=ultimos_ingresos,
        ultimas_donaciones=ultimas_donaciones,
    )
