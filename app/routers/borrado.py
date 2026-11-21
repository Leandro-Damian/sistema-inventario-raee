from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import ATTACHMENTS_DIR, MAX_UPLOAD_MB
from app.constants import (
    DISPOSICIONES,
    ESTANDARES_BORRADO,
    MODALIDADES_BORRADO,
    SALUD_SMART,
)
from app.database import get_db
from app.models import BorradoSeguro, Entidad, Item
from app.templating import page

router = APIRouter()


@router.get("/inventario/{item_id}/borrado")
def formulario(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    entidades = db.scalars(select(Entidad).order_by(Entidad.razon_social)).all()
    return page(
        request,
        "inventario/borrado.html",
        item=item,
        entidades=entidades,
        modalidades=MODALIDADES_BORRADO,
        estandares=ESTANDARES_BORRADO,
        salud=SALUD_SMART,
        disposiciones=DISPOSICIONES,
        borrado=item.borrados[0] if item.borrados else None,
    )


@router.post("/inventario/{item_id}/borrado")
async def guardar(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        return RedirectResponse("/inventario?error=" + quote("Ítem no encontrado"), status_code=303)
    form = await request.form()

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    modalidad = txt("modalidad")
    estandar = txt("estandar")
    if modalidad not in MODALIDADES_BORRADO or estandar not in ESTANDARES_BORRADO:
        return RedirectResponse(
            f"/inventario/{item_id}/borrado?error=" + quote("Modalidad o estándar inválido"),
            status_code=303,
        )
    try:
        fecha = datetime.fromisoformat(txt("fecha_hora"))
    except ValueError:
        fecha = datetime.now()

    borrado = item.borrados[0] if item.borrados else None
    if borrado is None:
        borrado = BorradoSeguro(item_id=item.id)
        db.add(borrado)

    borrado.entidad_origen_id = int(txt("entidad_origen_id")) if txt("entidad_origen_id") else None
    borrado.tipo = txt("tipo") or item.tipo_unidad
    borrado.capacidad = txt("capacidad") or item.capacidad
    borrado.interfaz = txt("interfaz") or item.interfaz
    borrado.salud_smart = txt("salud_smart") or item.salud_smart
    borrado.numero_serie_verificado = txt("numero_serie_verificado") or item.numero_serie
    borrado.modalidad = modalidad
    borrado.herramienta = txt("herramienta")
    borrado.metodo = txt("metodo")
    borrado.fecha_hora = fecha
    borrado.estandar = estandar

    comprobante = form.get("comprobante")
    if isinstance(comprobante, UploadFile) and comprobante.filename:
        datos = await comprobante.read()
        if len(datos) > MAX_UPLOAD_MB * 1024 * 1024:
            return RedirectResponse(
                f"/inventario/{item_id}/borrado?error=" + quote("El adjunto supera el tamaño permitido"),
                status_code=303,
            )
        ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
        sufijo = Path(comprobante.filename).name
        destino = ATTACHMENTS_DIR / f"{uuid.uuid4().hex}_{sufijo}"
        destino.write_bytes(datos)
        if borrado.comprobante_path:
            anterior = Path(borrado.comprobante_path)
            if anterior.exists() and anterior.is_file():
                anterior.unlink(missing_ok=True)
        borrado.comprobante_path = str(destino)

    db.commit()
    return RedirectResponse(
        f"/inventario/{item_id}?ok=" + quote("Borrado seguro registrado"), status_code=303
    )


@router.get("/borrado/{borrado_id}/certificado")
def certificado(borrado_id: int, request: Request, db: Session = Depends(get_db)):
    borrado = db.get(BorradoSeguro, borrado_id)
    if borrado is None:
        return RedirectResponse("/inventario?error=" + quote("Certificado no encontrado"), status_code=303)
    return page(request, "borrado/certificado.html", borrado=borrado)
