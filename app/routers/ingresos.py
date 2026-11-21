from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import (
    CATEGORIAS,
    DISPOSICIONES,
    FACTORES_FORMA,
    INTERFACES_ALMACENAMIENTO,
    PLANTILLAS_ATRIBUTOS,
    SALUD_SMART,
    TIPOS_CABLE,
    TIPOS_UNIDAD_ALMACENAMIENTO,
)
from app.database import get_db
from app.models import Entidad, Ingreso
from app.services.codigos import next_code
from app.services.inventario import crear_items
from app.services.operarios import desde_formulario, normalizar
from app.templating import page

router = APIRouter(prefix="/ingresos")


@router.get("")
def listado(request: Request, db: Session = Depends(get_db)):
    q = (request.query_params.get("q") or "").strip()
    stmt = select(Ingreso)
    if q:
        stmt = stmt.where(
            Ingreso.codigo.like(f"%{q}%")
            | Ingreso.remito.like(f"%{q}%")
            | Ingreso.patente.like(f"%{q}%")
        )
    ingresos = db.scalars(stmt.order_by(Ingreso.fecha_retiro.desc())).all()
    return page(request, "ingresos/lista.html", ingresos=ingresos, q=q)


@router.get("/nuevo")
def nuevo(request: Request, db: Session = Depends(get_db)):
    generadores = db.scalars(
        select(Entidad).where(Entidad.activa.is_(True)).order_by(Entidad.razon_social)
    ).all()
    return page(
        request,
        "ingresos/form.html",
        generadores=generadores,
        categorias=CATEGORIAS,
        tipos_cable=TIPOS_CABLE,
        plantillas=PLANTILLAS_ATRIBUTOS,
        tipos_unidad=TIPOS_UNIDAD_ALMACENAMIENTO,
        factores_forma=FACTORES_FORMA,
        interfaces=INTERFACES_ALMACENAMIENTO,
        salud=SALUD_SMART,
        disposiciones=DISPOSICIONES,
        ingreso=None,
    )


@router.post("/nuevo")
async def crear(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    try:
        generador_id = int(txt("generador_id"))
        fecha = datetime.fromisoformat(txt("fecha_retiro"))
    except (TypeError, ValueError):
        return RedirectResponse(
            "/ingresos/nuevo?error=" + quote("Fecha y generador son obligatorios"), status_code=303
        )

    if db.get(Entidad, generador_id) is None:
        return RedirectResponse(
            "/ingresos/nuevo?error=" + quote("Generador no encontrado"), status_code=303
        )

    try:
        peso_declarado = float(txt("peso_declarado") or 0)
    except ValueError:
        peso_declarado = 0.0

    try:
        n_operarios = int(txt("operario_count") or 0)
    except ValueError:
        n_operarios = 0
    operarios = desde_formulario(form, n_operarios)

    ingreso = Ingreso(
        codigo=next_code(db, "ING", 5, fecha.year),
        generador_id=generador_id,
        fecha_retiro=fecha,
        remito=txt("remito"),
        peso_declarado=peso_declarado,
        resumen=txt("resumen"),
        camion=txt("camion"),
        patente=txt("patente"),
        empresa_transporte=txt("empresa_transporte"),
        chofer_nombre=txt("chofer_nombre"),
        chofer_telefono=txt("chofer_telefono"),
        operarios=operarios,
    )
    db.add(ingreso)
    db.flush()

    try:
        n_items = int(txt("item_count") or 0)
    except ValueError:
        n_items = 0

    for i in range(n_items):
        categoria = txt(f"item_categoria_{i}")
        if not categoria:
            continue
        try:
            cantidad = max(1, int(txt(f"item_cantidad_{i}") or 1))
        except ValueError:
            cantidad = 1
        try:
            peso = float(txt(f"item_peso_{i}") or 0)
        except ValueError:
            peso = 0.0

        atributos: list[tuple[str, str]] = []
        try:
            n_attrs = int(txt(f"item_attr_count_{i}") or 0)
        except ValueError:
            n_attrs = 0
        for j in range(n_attrs):
            clave = txt(f"item_attr_clave_{i}_{j}")
            if clave:
                atributos.append((clave, txt(f"item_attr_valor_{i}_{j}")))

        ficha = {}
        if categoria == "Unidades de Almacenamiento":
            ficha = {
                "numero_serie": txt(f"item_numero_serie_{i}"),
                "tipo_unidad": txt(f"item_tipo_unidad_{i}"),
                "factor_forma": txt(f"item_factor_forma_{i}"),
                "interfaz": txt(f"item_interfaz_{i}"),
                "capacidad": txt(f"item_capacidad_{i}"),
                "salud_smart": txt(f"item_salud_smart_{i}"),
                "disposicion": txt(f"item_disposicion_{i}"),
            }

        crear_items(
            db,
            ingreso=ingreso,
            categoria=categoria,
            subcategoria=txt(f"item_subcategoria_{i}") if categoria == "Cables" else "",
            marca=txt(f"item_marca_{i}"),
            modelo=txt(f"item_modelo_{i}"),
            cantidad=cantidad,
            peso_unitario=peso,
            atributos=atributos,
            fecha=fecha,
            ficha_storage=ficha,
        )

    db.commit()
    return RedirectResponse(
        f"/ingresos/{ingreso.id}?ok=" + quote("Ingreso registrado correctamente"), status_code=303
    )


@router.get("/{ingreso_id}")
def detalle(ingreso_id: int, request: Request, db: Session = Depends(get_db)):
    ingreso = db.get(Ingreso, ingreso_id)
    if ingreso is None:
        return RedirectResponse("/ingresos?error=" + quote("Ingreso no encontrado"), status_code=303)
    return page(
        request,
        "ingresos/detalle.html",
        ing=ingreso,
        ingreso=ingreso,
        operarios=[normalizar(op) for op in ingreso.operarios],
    )
