from app.constants import ESTADOS
from app.models import Item, ItemEspecificacion
from tests.conftest import make_item


def test_estados_exactos_en_filtro(client):
    html = client.get("/inventario").text
    for estado in ESTADOS:
        assert estado in html
    assert len(ESTADOS) == 7


def test_listado_filtros_y_exportar_csv(client):
    make_item(categoria="Monitores", estado="Para donar", marca="Samsung", modelo="SyncMaster")
    make_item(categoria="Cables", estado="En recepción", marca="Genérico", modelo="VGA")

    html = client.get("/inventario?estado=Para+donar").text
    assert "Para donar" in html
    assert "SyncMaster" in html

    csv_response = client.get("/inventario?estado=Para+donar&export=csv")
    assert csv_response.status_code == 200
    assert "text/csv" in csv_response.headers["content-type"]
    assert "RAEE-2026-000001" in csv_response.text
    assert "Samsung" in csv_response.text


def test_cambiar_estado_y_especificaciones(client, db):
    item_id = make_item()
    response = client.post(
        f"/inventario/{item_id}/estado", data={"estado": "Recuperado"}, follow_redirects=False
    )
    assert response.status_code == 303
    assert db.get(Item, item_id).estado == "Recuperado"

    client.post(
        f"/inventario/{item_id}/especificaciones",
        data={"clave": "Tipo (DDR1/DDR2/DDR3/DDR4/DDR5)", "valor": "DDR4"},
        follow_redirects=False,
    )
    item = db.get(Item, item_id)
    assert any(e.clave.startswith("Tipo") and e.valor == "DDR4" for e in item.especificaciones)

    esp = item.especificaciones[0]
    client.post(f"/inventario/{item_id}/especificaciones/{esp.id}/eliminar", follow_redirects=False)
    assert db.query(ItemEspecificacion).filter(ItemEspecificacion.item_id == item_id).count() == 0


def test_ficha_almacenamiento_y_borrado(client, db):
    item_id = make_item(
        categoria="Unidades de Almacenamiento",
        estado="Recuperado",
        numero_serie="SN-ABC",
        tipo_unidad="SSD",
        factor_forma="2.5\"",
        interfaz="SATA",
        capacidad="240 GB",
        salud_smart="Saludable",
        disposicion="Pendiente de borrado/destrucción",
    )
    html = client.get(f"/inventario/{item_id}").text
    assert "SN-ABC" in html
    assert "240 GB" in html
    assert "Borrado seguro / Destrucción" in html
