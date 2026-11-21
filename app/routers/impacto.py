from __future__ import annotations

from datetime import date, datetime, time

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.impacto import calcular_impacto
from app.templating import page

router = APIRouter(prefix="/impacto")


def _rango(request: Request) -> tuple[datetime | None, datetime | None, str, str]:
    desde_s = (request.query_params.get("desde") or "").strip()
    hasta_s = (request.query_params.get("hasta") or "").strip()
    desde = datetime.combine(date.fromisoformat(desde_s), time.min) if desde_s else None
    hasta = datetime.combine(date.fromisoformat(hasta_s), time.max) if hasta_s else None
    return desde, hasta, desde_s, hasta_s


@router.get("")
def index(request: Request, db: Session = Depends(get_db)):
    try:
        desde, hasta, desde_s, hasta_s = _rango(request)
    except ValueError:
        desde = hasta = None
        desde_s = hasta_s = ""
    impacto = calcular_impacto(db, desde, hasta)
    return page(
        request,
        "impacto/index.html",
        impacto=impacto,
        desde=desde_s,
        hasta=hasta_s,
    )


@router.get("/imprimir")
def imprimir(request: Request, db: Session = Depends(get_db)):
    try:
        desde, hasta, desde_s, hasta_s = _rango(request)
    except ValueError:
        desde = hasta = None
        desde_s = hasta_s = ""
    impacto = calcular_impacto(db, desde, hasta)
    return page(
        request,
        "impacto/imprimir.html",
        impacto=impacto,
        desde=desde_s,
        hasta=hasta_s,
    )
