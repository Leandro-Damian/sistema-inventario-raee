from app.models import Item
from tests.conftest import make_item


def test_desguace_crea_componentes_recuperados_y_cambia_chasis(client, db):
    chasis_id = make_item(categoria="Computadoras de escritorio (Gabinete)", estado="En revisión", peso=9.5)

    response = client.post(
        f"/inventario/{chasis_id}/desguace",
        data={
            "componente_count": "2",
            "comp_categoria_0": "Memorias RAM",
            "comp_marca_0": "Kingston",
            "comp_modelo_0": "KVR16N11",
            "comp_cantidad_0": "2",
            "comp_peso_0": "0.05",
            "comp_categoria_1": "Procesadores (CPU)",
            "comp_marca_1": "Intel",
            "comp_modelo_1": "Core i5",
            "comp_cantidad_1": "1",
            "comp_peso_1": "0.1",
            "estado_final": "Desguazado",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    chasis = db.get(Item, chasis_id)
    assert chasis.estado == "Desguazado"
    assert len(chasis.componentes) == 3  # 2 RAM + 1 CPU

    for componente in chasis.componentes:
        assert componente.estado == "Recuperado"
        assert componente.origen_id == chasis_id
        assert componente.codigo.startswith("RAEE-2026-")

    html = client.get(f"/inventario/{chasis_id}").text
    assert "Componentes recuperados de este equipo" in html
    assert "RAEE-2026-000002" in html
