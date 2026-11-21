from __future__ import annotations

import os
import tempfile
from datetime import datetime

TMP_DIR = tempfile.mkdtemp(prefix="raee_tests_")
os.environ["RAEE_DB_PATH"] = os.path.join(TMP_DIR, "raee.db")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.config import AUTHOR  # noqa: E402
from app.database import Base, SessionLocal, create_tables, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Entidad, Ingreso, Item  # noqa: E402
from app.seed import seed_catalogos  # noqa: E402
from app.services.codigos import next_code  # noqa: E402
from app.services.inventario import crear_items  # noqa: E402


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    create_tables()
    with SessionLocal() as db:
        seed_catalogos(db)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db() -> Session:
    with SessionLocal() as session:
        yield session


def make_entidad(nombre: str = "Entidad de prueba", tipo: str = "Generador", activa: bool = True) -> int:
    with SessionLocal() as session:
        entidad = Entidad(
            razon_social=nombre,
            nombre_corto=nombre,
            cuit="30-00000000-0",
            tipo=tipo,
            provincia="Tucumán",
            localidad="San Miguel de Tucumán",
            activa=activa,
        )
        session.add(entidad)
        session.commit()
        session.refresh(entidad)
        return entidad.id


def make_ingreso(generador_id: int | None = None, fecha: datetime | None = None) -> int:
    fecha = fecha or datetime(2026, 10, 14, 9, 30)
    with SessionLocal() as session:
        if generador_id is None:
            generador_id = make_entidad()
        ingreso = Ingreso(
            codigo=next_code(session, "ING", 5, fecha.year),
            generador_id=generador_id,
            fecha_retiro=fecha,
            remito="R-TEST",
            peso_declarado=100.0,
            resumen="Prueba",
            operarios=[],
        )
        session.add(ingreso)
        session.commit()
        session.refresh(ingreso)
        return ingreso.id


def make_item(
    categoria: str = "Monitores",
    estado: str = "En recepción",
    peso: float = 2.0,
    marca: str = "Marca",
    modelo: str = "Modelo",
    fecha: datetime | None = None,
    ingreso_id: int | None = None,
    **ficha,
) -> int:
    fecha = fecha or datetime(2026, 10, 14, 9, 30)
    with SessionLocal() as session:
        if ingreso_id is None:
            ingreso_id = make_ingreso(fecha=fecha)
        ingreso = session.get(Ingreso, ingreso_id)
        items = crear_items(
            session,
            ingreso=ingreso,
            categoria=categoria,
            marca=marca,
            modelo=modelo,
            cantidad=1,
            peso_unitario=peso,
            estado=estado,
            fecha=fecha,
            ficha_storage=ficha,
        )
        session.commit()
        return items[0].id
