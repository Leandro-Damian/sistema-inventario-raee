from pathlib import Path

from app.config import APP_NAME
from app.models import BorradoSeguro
from tests.conftest import make_item


def test_borrado_seguro_con_adjunto_y_certificado(client, db):

    item_id = make_item(
        categoria="Unidades de Almacenamiento",
        numero_serie="SN-SEGURO-001",
        tipo_unidad="HDD",
        interfaz="SATA",
        capacidad="1 TB",
        salud_smart="Saludable",
        estado="Recuperado",
    )
    response = client.post(
        f"/inventario/{item_id}/borrado",
        data={
            "entidad_origen_id": "",
            "tipo": "HDD",
            "capacidad": "1 TB",
            "interfaz": "SATA",
            "salud_smart": "Saludable",
            "numero_serie_verificado": "SN-SEGURO-001",
            "modalidad": "Borrado por software",
            "herramienta": "Blancco",
            "metodo": "Sobrescritura de 3 pasos",
            "fecha_hora": "2026-11-01T10:00",
            "estandar": "NIST SP 800-88",
        },
        files={"comprobante": ("comprobante.txt", b"contenido de prueba", "text/plain")},
        follow_redirects=False,
    )
    assert response.status_code == 303

    borrado = db.query(BorradoSeguro).filter(BorradoSeguro.item_id == item_id).one()
    assert borrado.numero_serie_verificado == "SN-SEGURO-001"
    assert borrado.estandar == "NIST SP 800-88"
    assert borrado.comprobante_path
    archivo = Path(borrado.comprobante_path)
    assert archivo.exists()
    archivo.unlink(missing_ok=True)

    html = client.get(f"/borrado/{borrado.id}/certificado").text
    assert "Constancia de borrado seguro" in html
    assert "SN-SEGURO-001" in html
    assert "NIST SP 800-88" in html
    assert APP_NAME in html


def test_borrado_rechaza_modalidad_invalida(client):
    item_id = make_item(categoria="Unidades de Almacenamiento", numero_serie="SN-X")
    response = client.post(
        f"/inventario/{item_id}/borrado",
        data={"modalidad": "Inventada", "estandar": "Físico", "numero_serie_verificado": "SN-X"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "error=" in response.headers["location"]
