from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, STATIC_DIR
from app.database import SessionLocal, create_tables
from app.seed import seed_catalogos
from app.routers import (
    borrado,
    donaciones,
    entidades,
    impacto,
    inventario,
    ingresos,
    manual,
    materiales,
    panel,
)

create_tables()
with SessionLocal() as _db:
    seed_catalogos(_db)

app = FastAPI(title=APP_NAME, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(panel.router)
app.include_router(entidades.router)
app.include_router(ingresos.router)
app.include_router(inventario.router)
app.include_router(borrado.router)
app.include_router(materiales.router)
app.include_router(donaciones.router)
app.include_router(impacto.router)
app.include_router(manual.router)
