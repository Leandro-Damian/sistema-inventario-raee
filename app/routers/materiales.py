from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.constants import TIPO_MOVIMIENTO_ALTA, TIPO_MOVIMIENTO_SALIDA
from app.database import get_db
from app.models import Entidad, MovimientoMaterial, TipoMaterial
from app.templating import page

router = APIRouter(prefix="/materiales")


@router.get("")
def listado(request: Request, db: Session = Depends(get_db)):
    tipos = db.scalars(select(TipoMaterial).order_by(TipoMaterial.nombre)).all()
    altas = dict(
        db.execute(
            select(MovimientoMaterial.tipo_material_id, func.coalesce(func.sum(MovimientoMaterial.kg), 0.0))
            .where(MovimientoMaterial.tipo == TIPO_MOVIMIENTO_ALTA)
            .group_by(MovimientoMaterial.tipo_material_id)
        ).all()
    )
    salidas = dict(
        db.execute(
            select(MovimientoMaterial.tipo_material_id, func.coalesce(func.sum(MovimientoMaterial.kg), 0.0))
            .where(MovimientoMaterial.tipo == TIPO_MOVIMIENTO_SALIDA)
            .group_by(MovimientoMaterial.tipo_material_id)
        ).all()
    )
    filas = []
    for t in tipos:
        entrada = altas.get(t.id, 0.0)
        salida = salidas.get(t.id, 0.0)
        filas.append({"tipo": t, "entradas": entrada, "salidas": salida, "stock": entrada - salida})

    movimientos = db.scalars(
        select(MovimientoMaterial).order_by(MovimientoMaterial.fecha.desc()).limit(50)
    ).all()
    recicladores = db.scalars(
        select(Entidad).where(Entidad.activa.is_(True)).order_by(Entidad.razon_social)
    ).all()
    return page(
        request,
        "materiales/lista.html",
        filas=filas,
        movimientos=movimientos,
        recicladores=recicladores,
    )


@router.post("/tipos")
async def crear_tipo(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    nombre = str(form.get("nombre") or "").strip()
    try:
        factor = float(str(form.get("factor_co2e") or "0").replace(",", "."))
    except ValueError:
        factor = 0.0
    if not nombre:
        return RedirectResponse(
            "/materiales?error=" + quote("El nombre del material es obligatorio"), status_code=303
        )
    existe = db.scalar(select(TipoMaterial).where(TipoMaterial.nombre == nombre))
    if existe is not None:
        return RedirectResponse(
            "/materiales?error=" + quote("Ese tipo de material ya existe"), status_code=303
        )
    db.add(TipoMaterial(nombre=nombre, factor_co2e=factor, activo=True))
    db.commit()
    return RedirectResponse(
        "/materiales?ok=" + quote("Tipo de material creado"), status_code=303
    )


@router.post("/movimientos")
async def crear_movimiento(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    tipo = txt("tipo")
    if tipo not in (TIPO_MOVIMIENTO_ALTA, TIPO_MOVIMIENTO_SALIDA):
        return RedirectResponse("/materiales?error=" + quote("Movimiento inválido"), status_code=303)
    try:
        tipo_material_id = int(txt("tipo_material_id"))
        kg = float(txt("kg").replace(",", "."))
        fecha = datetime.fromisoformat(txt("fecha")) if txt("fecha") else datetime.now()
    except (TypeError, ValueError):
        return RedirectResponse(
            "/materiales?error=" + quote("Revisá el material, el peso y la fecha"), status_code=303
        )
    if db.get(TipoMaterial, tipo_material_id) is None or kg <= 0:
        return RedirectResponse(
            "/materiales?error=" + quote("Material inexistente o peso inválido"), status_code=303
        )

    reciclador_id = int(txt("reciclador_id")) if txt("reciclador_id") else None
    db.add(
        MovimientoMaterial(
            tipo_material_id=tipo_material_id,
            tipo=tipo,
            kg=kg,
            fecha=fecha,
            referencia=txt("referencia"),
            observacion=txt("observacion"),
            reciclador_id=reciclador_id,
        )
    )
    db.commit()
    return RedirectResponse(
        "/materiales?ok=" + quote("Movimiento registrado"), status_code=303
    )
