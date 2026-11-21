import re

from app.models import Ingreso, Item
from tests.conftest import make_entidad, make_ingreso


def test_formulario_ingreso_dos_operarios_por_defecto_y_sin_dni(client):
    html = client.get("/ingresos/nuevo").text
    assert "DNI" not in html
    assert "Operador activo" not in html
    assert "chofer_nombre" in html
    assert "Cantidad" in html

    # Alpine inicializa con dos filas visibles y métodos reactivos para agregar/quitar.
    assert 'operarios: [{ nombre: "", telefono: "" }, { nombre: "", telefono: "" }]' in html
    assert "agregarOperario()" in html
    assert "quitarOperario(i)" in html
    assert "operario_nombre_" in html
    assert "operario_telefono_" in html
    # El atributo x-data usa comillas simples: el tojson con comillas dobles no debe romperlo.
    assert "x-data='{" in html


def test_crear_ingreso_con_lotes_y_codigos_correlativos(client, db):
    generador_id = make_entidad("Municipalidad de prueba")
    datos = {
        "generador_id": str(generador_id),
        "fecha_retiro": "2026-10-14T09:30",
        "remito": "R-999",
        "peso_declarado": "100",
        "resumen": "26 cables VGA y 1 disco",
        "camion": "Ford F-100",
        "patente": "AA123BB",
        "empresa_transporte": "Transportes Test",
        "chofer_nombre": "Juan Ramírez",
        "chofer_telefono": "0381 400-0000",
        "operario_count": "2",
        "operario_nombre_0": "Lucas Fernández",
        "operario_telefono_0": "0381 400-1111",
        "operario_nombre_1": "Nicolás Díaz",
        "operario_telefono_1": "0381 400-2222",
        "item_count": "2",
        "item_categoria_0": "Cables",
        "item_subcategoria_0": "VGA",
        "item_marca_0": "Genérico",
        "item_modelo_0": "VGA 1.5m",
        "item_cantidad_0": "26",
        "item_peso_0": "0.2",
        "item_attr_count_0": "1",
        "item_attr_clave_0_0": "Largo",
        "item_attr_valor_0_0": "1.5 m",
        "item_categoria_1": "Unidades de Almacenamiento",
        "item_marca_1": "Seagate",
        "item_modelo_1": "Barracuda",
        "item_cantidad_1": "1",
        "item_peso_1": "0.6",
        "item_attr_count_1": "0",
        "item_numero_serie_1": "SN-TEST-001",
        "item_tipo_unidad_1": "HDD",
        "item_factor_forma_1": '3.5"',
        "item_interfaz_1": "SATA",
        "item_capacidad_1": "500 GB",
        "item_salud_smart_1": "Saludable",
        "item_disposicion_1": "Para donar",
    }
    response = client.post("/ingresos/nuevo", data=datos, follow_redirects=False)
    assert response.status_code == 303
    Location = response.headers["location"]
    ingreso_id = int(re.search(r"/ingresos/(\d+)", Location).group(1))

    ingreso = db.get(Ingreso, ingreso_id)
    assert ingreso.codigo == "ING-2026-00001"
    assert ingreso.operarios == [
        {"nombre": "Lucas Fernández", "telefono": "0381 400-1111"},
        {"nombre": "Nicolás Díaz", "telefono": "0381 400-2222"},
    ]
    assert ingreso.chofer_nombre == "Juan Ramírez"

    items = db.query(Item).filter(Item.ingreso_id == ingreso_id).order_by(Item.codigo).all()
    assert len(items) == 27
    assert items[0].codigo == "RAEE-2026-000001"
    assert items[-1].codigo == "RAEE-2026-000027"
    assert all(i.peso_unitario == 0.2 for i in items[:26])
    assert items[0].subcategoria == "VGA"
    assert items[0].especificaciones[0].clave == "Largo"

    disco = items[-1]
    assert disco.categoria == "Unidades de Almacenamiento"
    assert disco.numero_serie == "SN-TEST-001"
    assert disco.interfaz == "SATA"
    assert disco.capacidad == "500 GB"

    html = client.get(f"/ingresos/{ingreso_id}").text
    assert "ING-2026-00001" in html
    assert "RAEE-2026-000027" in html
    assert "Lucas Fernández" in html
    assert "0381 400-1111" in html
    assert "Nicolás Díaz" in html
    assert "0381 400-2222" in html
    assert "Tel.:" in html
    assert "DNI" not in html


def test_detalle_admite_operarios_historicos_como_texto(client, db):
    ingreso_id = make_ingreso()
    ingreso = db.get(Ingreso, ingreso_id)
    ingreso.operarios = ["Operario Histórico"]
    db.commit()

    html = client.get(f"/ingresos/{ingreso_id}").text
    assert "Operario Histórico" in html
    assert "DNI" not in html


def test_ingreso_requiere_fecha_y_generador(client):
    response = client.post("/ingresos/nuevo", data={"generador_id": ""}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/ingresos/nuevo?error=")
