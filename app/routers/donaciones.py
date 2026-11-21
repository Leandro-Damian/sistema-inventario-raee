from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Donacion, Entidad, Item
from app.services.codigos import next_code
from app.templating import page

router = APIRouter(prefix="/donaciones")


@router.get("")
def listado(request: Request, db: Session = Depends(get_db)):
    donaciones = db.scalars(select(Donacion).order_by(Donacion.fecha.desc())).all()
    return page(request, "donaciones/lista.html", donaciones=donaciones)


@router.get("/nueva")
def nueva(request: Request, db: Session = Depends(get_db)):
    receptores = db.scalars(
        select(Entidad)
        .where(Entidad.activa.is_(True), Entidad.tipo == "Receptor de donaciones")
        .order_by(Entidad.razon_social)
    ).all()
    candidatos = db.scalars(
        select(Item)
        .where(Item.estado.in_(["Para donar", "Recuperado"]))
        .order_by(Item.codigo)
    ).all()
    return page(
        request,
        "donaciones/form.html",
        receptores=receptores,
        candidatos=candidatos,
    )


@router.post("/nueva")
async def crear(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    try:
        entidad_id = int(txt("entidad_id"))
        fecha = datetime.fromisoformat(txt("fecha")) if txt("fecha") else datetime.now()
    except (TypeError, ValueError):
        return RedirectResponse(
            "/donaciones/nueva?error=" + quote("Receptor o fecha inválidos"), status_code=303
        )
    if db.get(Entidad, entidad_id) is None:
        return RedirectResponse(
            "/donaciones/nueva?error=" + quote("Receptor no encontrado"), status_code=303
        )

    ids = []
    for raw in form.getlist("item_ids"):
        try:
            ids.append(int(raw))
        except (TypeError, ValueError):
            continue
    if not ids:
        return RedirectResponse(
            "/donaciones/nueva?error=" + quote("Seleccioná al menos un equipo"), status_code=303
        )

    items = db.scalars(select(Item).where(Item.id.in_(ids))).all()
    items = [i for i in items if i.estado in ("Para donar", "Recuperado")]
    if not items:
        return RedirectResponse(
            "/donaciones/nueva?error=" + quote("Los equipos seleccionados no están disponibles"),
            status_code=303,
        )

    donacion = Donacion(
        codigo=next_code(db, "DON", 5, fecha.year),
        entidad_id=entidad_id,
        fecha=fecha,
        observaciones=txt("observaciones"),
    )
    db.add(donacion)
    db.flush()
    for it in items:
        it.estado = "Donado"
        it.donacion_id = donacion.id
        it.fecha_donacion = fecha
    db.commit()
    return RedirectResponse(
        f"/donaciones/{donacion.id}?ok=" + quote("Donación registrada"), status_code=303
    )


@router.get("/{donacion_id}")
def detalle(donacion_id: int, request: Request, db: Session = Depends(get_db)):
    donacion = db.get(Donacion, donacion_id)
    if donacion is None:
        return RedirectResponse("/donaciones?error=" + quote("Donación no encontrada"), status_code=303)
    return page(request, "donaciones/detalle.html", donacion=donacion)


@router.get("/{donacion_id}/acta")
def acta(donacion_id: int, request: Request, db: Session = Depends(get_db)):
    donacion = db.get(Donacion, donacion_id)
    if donacion is None:
        return RedirectResponse("/donaciones?error=" + quote("Donación no encontrada"), status_code=303)
    return page(request, "donaciones/acta.html", donacion=donacion)
