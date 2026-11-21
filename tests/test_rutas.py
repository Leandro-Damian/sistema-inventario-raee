from app.models import BorradoSeguro, Donacion
from tests.conftest import make_entidad, make_item


def test_todas_las_vistas_renderizan(client, db):
    entidad_id = make_entidad("Entidad Smoke", tipo="Receptor de donaciones")
    generador_id = make_entidad("Generador Smoke")
    item_simple = make_item(categoria="Monitores", estado="Para donar")
    item_storage = make_item(
        categoria="Unidades de Almacenamiento",
        estado="Recuperado",
        numero_serie="SN-SMOKE",
    )

    client.post(
        "/donaciones/nueva",
        data={
            "entidad_id": str(entidad_id),
            "fecha": "2026-11-10",
            "item_ids": [str(item_simple)],
        },
        follow_redirects=False,
    )
    donacion_id = db.query(Donacion).first().id

    client.post(
        f"/inventario/{item_storage}/borrado",
        data={
            "numero_serie_verificado": "SN-SMOKE",
            "modalidad": "Destrucción física",
            "estandar": "Físico",
            "fecha_hora": "2026-11-11T10:00",
        },
        follow_redirects=False,
    )
    borrado_id = db.query(BorradoSeguro).first().id

    rutas = [
        "/",
        "/entidades",
        "/entidades/nueva",
        f"/entidades/{entidad_id}/editar",
        "/ingresos",
        "/ingresos/nuevo",
        "/inventario",
        f"/inventario/{item_simple}",
        f"/inventario/{item_simple}/desguace",
        f"/inventario/{item_storage}/borrado",
        f"/borrado/{borrado_id}/certificado",
        "/materiales",
        "/donaciones",
        "/donaciones/nueva",
        f"/donaciones/{donacion_id}",
        f"/donaciones/{donacion_id}/acta",
        "/impacto",
        "/impacto/imprimir",
        "/manual",
    ]
    for ruta in rutas:
        respuesta = client.get(ruta)
        assert respuesta.status_code == 200, f"Error {respuesta.status_code} en {ruta}"
        assert "<html" in respuesta.text, ruta
