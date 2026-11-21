from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.constants import TIPOS_ENTIDAD
from app.database import get_db
from app.models import Entidad
from app.templating import page

router = APIRouter(prefix="/entidades")


@router.get("")
def listado(request: Request, db: Session = Depends(get_db)):
    q = (request.query_params.get("q") or "").strip()
    stmt = select(Entidad)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Entidad.razon_social.like(like),
                Entidad.nombre_corto.like(like),
                Entidad.cuit.like(like),
                Entidad.localidad.like(like),
            )
        )
    entidades = db.scalars(stmt.order_by(Entidad.razon_social)).all()
    return page(request, "entidades/lista.html", entidades=entidades, q=q)


@router.get("/nueva")
def nueva(request: Request):
    return page(
        request,
        "entidades/form.html",
        entidad=None,
        tipos=TIPOS_ENTIDAD,
        accion="/entidades/nueva",
    )


@router.post("/nueva")
async def crear(request: Request, db: Session = Depends(get_db)):
    return await _guardar(request, db, None)


@router.get("/{entidad_id}/editar")
def editar(entidad_id: int, request: Request, db: Session = Depends(get_db)):
    entidad = db.get(Entidad, entidad_id)
    if entidad is None:
        return RedirectResponse("/entidades?error=Entidad+no+encontrada", status_code=303)
    return page(
        request,
        "entidades/form.html",
        entidad=entidad,
        tipos=TIPOS_ENTIDAD,
        accion=f"/entidades/{entidad_id}/editar",
    )


@router.post("/{entidad_id}/editar")
async def actualizar(entidad_id: int, request: Request, db: Session = Depends(get_db)):
    entidad = db.get(Entidad, entidad_id)
    if entidad is None:
        return RedirectResponse("/entidades?error=Entidad+no+encontrada", status_code=303)
    return await _guardar(request, db, entidad)


@router.post("/{entidad_id}/toggle")
def toggle(entidad_id: int, request: Request, db: Session = Depends(get_db)):
    entidad = db.get(Entidad, entidad_id)
    if entidad is None:
        return RedirectResponse("/entidades?error=Entidad+no+encontrada", status_code=303)
    entidad.activa = not entidad.activa
    db.commit()
    return RedirectResponse("/entidades?ok=Estado+actualizado", status_code=303)


async def _guardar(request: Request, db: Session, entidad: Entidad | None):
    form = await request.form()
    razon_social = (form.get("razon_social") or "").strip()
    tipo = (form.get("tipo") or "").strip()
    if not razon_social or tipo not in TIPOS_ENTIDAD:
        destino = "/entidades?error=La+razón+social+y+el+tipo+son+obligatorios"
        return RedirectResponse(destino, status_code=303)

    if entidad is None:
        entidad = Entidad()
        db.add(entidad)

    entidad.razon_social = razon_social
    entidad.nombre_corto = (form.get("nombre_corto") or "").strip()
    entidad.cuit = (form.get("cuit") or "").strip()
    entidad.tipo = tipo
    entidad.provincia = (form.get("provincia") or "").strip()
    entidad.localidad = (form.get("localidad") or "").strip()
    entidad.contacto_nombre = (form.get("contacto_nombre") or "").strip()
    entidad.contacto_cargo = (form.get("contacto_cargo") or "").strip()
    entidad.contacto_email = (form.get("contacto_email") or "").strip()
    entidad.contacto_telefono = (form.get("contacto_telefono") or "").strip()
    db.commit()
    return RedirectResponse("/entidades?ok=Entidad+guardada", status_code=303)
