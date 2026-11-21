from app.models import Donacion, Item
from tests.conftest import make_entidad, make_item


def test_donacion_cambia_estado_y_genera_acta(client, db):
    receptor_id = make_entidad("Fundación Test", tipo="Receptor de donaciones")
    item1 = make_item(categoria="Monitores", estado="Para donar", marca="Samsung", modelo="SyncMaster")
    item2 = make_item(categoria="Computadoras de escritorio (Gabinete)", estado="Recuperado", marca="HP", modelo="6000")

    response = client.post(
        "/donaciones/nueva",
        data={
            "entidad_id": str(receptor_id),
            "fecha": "2026-11-05",
            "observaciones": "Entrega a escuela técnica",
            "item_ids": [str(item1), str(item2)],
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    donacion = db.query(Donacion).one()
    assert donacion.codigo == "DON-2026-00001"
    assert len(donacion.items) == 2
    assert db.get(Item, item1).estado == "Donado"
    assert db.get(Item, item2).estado == "Donado"
    assert db.get(Item, item1).donacion_id == donacion.id

    acta = client.get(f"/donaciones/{donacion.id}/acta").text
    assert "Acta de entrega y donación" in acta
    assert "RAEE-2026-000001" in acta
    assert "RAEE-2026-000002" in acta
    assert "Fundación Test" in acta


def test_donacion_sin_items_es_rechazada(client):
    receptor_id = make_entidad("Fundación Test", tipo="Receptor de donaciones")
    response = client.post(
        "/donaciones/nueva",
        data={"entidad_id": str(receptor_id), "fecha": "2026-11-05"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "error=" in response.headers["location"]
