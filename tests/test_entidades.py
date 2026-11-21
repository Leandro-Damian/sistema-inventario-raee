from app.models import Entidad
from tests.conftest import make_entidad


def test_crear_entidad_con_contacto_de_cuatro_campos(client, db):
    response = client.post(
        "/entidades/nueva",
        data={
            "razon_social": "Escuela Técnica N° 1",
            "nombre_corto": "ET1",
            "cuit": "30-11111111-1",
            "tipo": "Receptor de donaciones",
            "provincia": "Tucumán",
            "localidad": "Concepción",
            "contacto_nombre": "Laura Martínez",
            "contacto_cargo": "Directora",
            "contacto_email": "laura@escuela.edu.ar",
            "contacto_telefono": "0381 499-0000",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    entidad = db.query(Entidad).filter(Entidad.razon_social == "Escuela Técnica N° 1").one()
    assert entidad.contacto_nombre == "Laura Martínez"
    assert entidad.contacto_cargo == "Directora"
    assert entidad.contacto_email == "laura@escuela.edu.ar"
    assert entidad.contacto_telefono == "0381 499-0000"
    assert entidad.activa is True

    html = client.get("/entidades").text
    assert "Escuela Técnica N° 1" in html
    assert "DNI" not in html


def test_formulario_no_tiene_dni_ni_operador_activo(client):
    html = client.get("/entidades/nueva").text
    assert "DNI" not in html
    assert "Operador activo" not in html
    for campo in ["contacto_nombre", "contacto_cargo", "contacto_email", "contacto_telefono"]:
        assert f'name="{campo}"' in html


def test_editar_y_buscar_entidad(client, db):
    entidad_id = make_entidad("Generador Original")
    response = client.post(
        f"/entidades/{entidad_id}/editar",
        data={
            "razon_social": "Generador Modificado",
            "nombre_corto": "GM",
            "cuit": "",
            "tipo": "Generador",
            "provincia": "Tucumán",
            "localidad": "Tafí Viejo",
            "contacto_nombre": "Pedro Gómez",
            "contacto_cargo": "",
            "contacto_email": "",
            "contacto_telefono": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert db.get(Entidad, entidad_id).razon_social == "Generador Modificado"

    html = client.get("/entidades?q=Modificado").text
    assert "Generador Modificado" in html
    assert "Generador Original" not in html


def test_activar_desactivar_entidad(client, db):
    entidad_id = make_entidad("Entidad temporal")
    client.post(f"/entidades/{entidad_id}/toggle", follow_redirects=False)
    assert db.get(Entidad, entidad_id).activa is False
    client.post(f"/entidades/{entidad_id}/toggle", follow_redirects=False)
    assert db.get(Entidad, entidad_id).activa is True
