from app.models import TipoMaterial


def test_crear_tipo_material_y_movimientos(client, db):
    response = client.post(
        "/materiales/tipos",
        data={"nombre": "Plata", "factor_co2e": "45.5"},
        follow_redirects=False,
    )
    assert response.status_code == 303

    tipo = db.query(TipoMaterial).filter(TipoMaterial.nombre == "Plata").one()
    assert tipo.factor_co2e == 45.5

    client.post(
        "/materiales/movimientos",
        data={
            "tipo": "alta",
            "tipo_material_id": str(tipo.id),
            "kg": "10",
            "fecha": "2026-10-20T10:00",
            "referencia": "Desarme lote 1",
            "observacion": "Contactos recuperados",
        },
        follow_redirects=False,
    )
    client.post(
        "/materiales/movimientos",
        data={
            "tipo": "salida",
            "tipo_material_id": str(tipo.id),
            "kg": "3",
            "fecha": "2026-10-22T10:00",
            "referencia": "Remito 123",
            "observacion": "",
        },
        follow_redirects=False,
    )

    html = client.get("/materiales").text
    assert "Plata" in html
    assert "10.00 kg" in html
    assert "3.00 kg" in html
    assert "7.00 kg" in html
    assert "Desarme lote 1" in html


def test_tipos_base_cargados(client, db):
    nombres = {t.nombre for t in db.query(TipoMaterial).all()}
    assert "Cobre de cables" in nombres
    assert "Aluminio" in nombres
    assert "Placas electrónicas" in nombres
