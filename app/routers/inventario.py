from __future__ import annotations

import csv
import io
from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.constants import CATEGORIAS, ESTADOS
from app.database import get_db
from app.models import Item, ItemEspecificacion
from app.services.inventario import crear_items
from app.templating import page

router = APIRouter(prefix="/inventario")


@router.get("")
def listado(request: Request, db: Session = Depends(get_db)):
    q = (request.query_params.get("q") or "").strip()
    estado = (request.query_params.get("estado") or "").strip()
    categoria = (request.query_params.get("categoria") or "").strip()

    stmt = select(Item)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Item.codigo.like(like),
                Item.marca.like(like),
                Item.modelo.like(like),
                Item.numero_serie.like(like),
            )
        )
    if estado:
        stmt = stmt.where(Item.estado == estado)
    if categoria:
        stmt = stmt.where(Item.categoria == categoria)

    items = db.scalars(stmt.order_by(Item.codigo.desc())).all()

    if request.query_params.get("export") == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(
            ["Código", "Categoría", "Subcategoría", "Marca", "Modelo", "Estado",
             "Peso unitario (kg)", "Ingreso", "Especificaciones"]
        )
        for it in items:
            specs = "; ".join(f"{s.clave}: {s.valor}" for s in it.especificaciones)
            writer.writerow(
                [it.codigo, it.categoria, it.subcategoria, it.marca, it.modelo, it.estado,
                 f"{it.peso_unitario:.3f}", it.ingreso.codigo if it.ingreso else "", specs]
            )
        return Response(
            content="\ufeff" + buf.getvalue(),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="inventario.csv"'},
        )

    return page(
        request,
        "inventario/lista.html",
        items=items,
        q=q,
        estado=estado,
        categoria=categoria,
        estados=ESTADOS,
        categorias=CATEGORIAS,
    )


@router.get("/{item_id}")
def detalle(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    return page(request, "inventario/detalle.html", item=item, estados=ESTADOS)


@router.post("/{item_id}/estado")
async def cambiar_estado(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    form = await request.form()
    estado = str(form.get("estado") or "").strip()
    if estado not in ESTADOS:
        return RedirectResponse(
            f"/inventario/{item_id}?error=" + quote("Estado inválido"), status_code=303
        )
    item.estado = estado
    if estado != "Donado":
        item.donacion_id = None
        item.fecha_donacion = None
    db.commit()
    return RedirectResponse(
        f"/inventario/{item_id}?ok=" + quote("Estado actualizado"), status_code=303
    )


@router.post("/{item_id}/especificaciones")
async def agregar_especificacion(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    form = await request.form()
    clave = str(form.get("clave") or "").strip()
    valor = str(form.get("valor") or "").strip()
    if clave:
        db.add(ItemEspecificacion(item_id=item.id, clave=clave, valor=valor))
        db.commit()
    return RedirectResponse(
        f"/inventario/{item_id}?ok=" + quote("Especificación agregada"), status_code=303
    )


@router.post("/{item_id}/especificaciones/{esp_id}/eliminar")
def eliminar_especificacion(item_id: int, esp_id: int, request: Request, db: Session = Depends(get_db)):
    esp = db.get(ItemEspecificacion, esp_id)
    if esp is not None and esp.item_id == item_id:
        db.delete(esp)
        db.commit()
    return RedirectResponse(f"/inventario/{item_id}?ok=" + quote("Especificación eliminada"), status_code=303)


@router.get("/{item_id}/desguace")
def desguace_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    return page(
        request,
        "inventario/desguace.html",
        item=item,
        categorias=CATEGORIAS,
    )


@router.post("/{item_id}/desguace")
async def desguace(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    form = await request.form()

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    try:
        n = int(txt("componente_count") or 0)
    except ValueError:
        n = 0

    for i in range(n):
        categoria = txt(f"comp_categoria_{i}")
        if not categoria:
            continue
        try:
            cantidad = max(1, int(txt(f"comp_cantidad_{i}") or 1))
        except ValueError:
            cantidad = 1
        try:
            peso = float(txt(f"comp_peso_{i}") or 0)
        except ValueError:
            peso = 0.0
        crear_items(
            db,
            ingreso=item.ingreso,
            categoria=categoria,
            marca=txt(f"comp_marca_{i}"),
            modelo=txt(f"comp_modelo_{i}"),
            cantidad=cantidad,
            peso_unitario=peso,
            estado="Recuperado",
            origen_id=item.id,
            fecha=datetime.now(),
        )

    estado_final = txt("estado_final")
    if estado_final in ("Desguazado", "Reciclado"):
        item.estado = estado_final
    db.commit()
    return RedirectResponse(
        f"/inventario/{item_id}?ok=" + quote("Desguace registrado"), status_code=303
    )
