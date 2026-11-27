from app.config import APP_NAME, AUTHOR

COMPANY_NAME = "Electrogreem S.R.L."


def test_nombre_del_sistema_en_titulo_head_y_encabezados(client):
    for ruta in ("/", "/ingresos/nuevo", "/manual"):
        html = client.get(ruta).text
        assert APP_NAME in html, ruta

    html = client.get("/").text
    inicio_head = html.find("<head")
    fin_head = html.find("</head>", inicio_head)
    head = html[inicio_head:fin_head]

    assert f"<title>Panel principal · {APP_NAME}</title>" in head
    assert "favicon.ico" in head
    assert "favicon.png" in head
    assert "apple-touch-icon" in head
    assert html.count(AUTHOR) == 1
    assert AUTHOR in head


def test_razon_social_en_pie_y_manual(client):
    for ruta in ("/", "/ingresos/nuevo", "/manual"):
        html = client.get(ruta).text
        assert COMPANY_NAME in html, ruta
        inicio_head = html.find("<head")
        fin_head = html.find("</head>", inicio_head)
        assert COMPANY_NAME not in html[inicio_head:fin_head], ruta


def test_favicons_estan_disponibles_por_http(client):
    for ruta, tipo in (
        ("/static/img/favicon.ico", "image/x-icon"),
        ("/static/img/favicon.png", "image/png"),
    ):
        respuesta = client.get(ruta)
        assert respuesta.status_code == 200, ruta
        assert respuesta.headers["content-type"].startswith(tipo), ruta
        assert len(respuesta.content) > 100, ruta


def test_manual_acceso_y_peso_decimal(client):
    html = client.get("/manual").text
    assert "acceso directo" in html.lower()
    assert "sin mostrar una ventana de consola" in html.lower()
    assert "Administrador de tareas" in html
    assert "0.15" in html
    assert "150 gramos" in html
    assert "1.0" in html
    assert "1 kilogramo" in html
