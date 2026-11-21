from __future__ import annotations

from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.config import APP_NAME, TEMPLATES_DIR
from app.constants import CATEGORIAS, ESTADOS, TIPOS_ENTIDAD

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def page(request: Request, name: str, **context) -> _TemplateResponse:
    base = {
        "request": request,
        "app_name": APP_NAME,
        "estados": ESTADOS,
        "categorias": CATEGORIAS,
        "tipos_entidad": TIPOS_ENTIDAD,
        "ok": request.query_params.get("ok", ""),
        "error": request.query_params.get("error", ""),
    }
    base.update(context)
    return templates.TemplateResponse(request=request, name=name, context=base)
