from datetime import datetime

import pytest

from app.services.impacto import calcular_impacto
from tests.conftest import make_entidad, make_item
from app.models import MovimientoMaterial, TipoMaterial
from app.database import SessionLocal


def test_calculo_impacto_reutilizacion_y_reciclaje(client, db):
    make_item(categoria="Monitores", estado="Recuperado")
    receptor_id = make_entidad("Fundación Impacto", tipo="Receptor de donaciones")
    donable = make_item(categoria="Computadoras de escritorio (Gabinete)", estado="Para donar")
    client.post(
        "/donaciones/nueva",
        data={
            "entidad_id": str(receptor_id),
            "fecha": "2026-11-05",
            "item_ids": [str(donable)],
        },
        follow_redirects=False,
    )

    cobre = db.query(TipoMaterial).filter(TipoMaterial.nombre == "Cobre de cables").one()
    with SessionLocal() as session:
        session.add(
            MovimientoMaterial(
                tipo_material_id=cobre.id,
                tipo="alta",
                kg=10.0,
                fecha=datetime(2026, 10, 20, 10, 0),
                referencia="Prueba impacto",
            )
        )
        session.commit()

    impacto = calcular_impacto(db)
    assert impacto["items_recuperados"] == 1
    assert impacto["items_donados"] == 1
    assert impacto["reutilizacion"] == pytest.approx(80 + 150)
    assert impacto["reciclaje"] == pytest.approx(26)
    assert impacto["total"] == pytest.approx(256)
    assert impacto["kg_materiales"] == pytest.approx(10)
    assert impacto["arboles"] > 0
    assert impacto["km_auto"] > 0


def test_vistas_impacto_y_filtro_fechas(client, db):
    make_item(categoria="Monitores", estado="Recuperado")
    html = client.get("/impacto?desde=2026-01-01&hasta=2026-12-31").text
    assert "Reutilización y donación" in html
    assert "Reciclaje y valorización" in html
    assert "80.0" in html

    imprimible = client.get("/impacto/imprimir?desde=2026-01-01&hasta=2026-12-31").text
    assert "Vista para gerencia" in imprimible
    assert "CO2e evitado" in imprimible
