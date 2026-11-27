from app.config import AUTHOR
from tests.conftest import make_item, make_entidad


def test_panel_muestra_tarjetas_y_resumenes(client):
    make_item(estado="Recuperado", peso=3.5)
    html = client.get("/").text
    assert "Ítems registrados" in html
    assert "Peso total ingresado" in html
    assert "Equipos donados" in html
    assert "Materiales valorizados" in html
    assert "CO2e evitado" in html
    assert "Inventario por estado" in html
    assert "Top categorías" in html
    assert "Últimos ingresos" in html
    assert "Últimas donaciones" in html


def test_metadato_autor_solo_en_head_y_no_en_interfaz(client):
    html = client.get("/").text
    assert html.count(AUTHOR) == 1
    assert f'<meta name="author" content="{AUTHOR}">' in html

    inicio_footer = html.find("<footer")
    fin_footer = html.find("</footer>", inicio_footer)
    footer = html[inicio_footer:fin_footer]
    assert "© 2027 · Electrogreem S.R.L. · Gestión integral de RAEE · Tucumán, Argentina" in footer
    assert "Leandro" not in footer
    assert "Chumbita" not in footer
    assert "http://" not in footer
    assert "www." not in footer


def test_sin_operador_activo_ni_dni_en_todas_las_pantallas(client):
    rutas = [
        "/", "/entidades", "/entidades/nueva", "/ingresos", "/ingresos/nuevo",
        "/inventario", "/materiales", "/donaciones", "/donaciones/nueva",
        "/impacto", "/manual",
    ]
    for ruta in rutas:
        html = client.get(ruta).text
        assert "Operador activo" not in html, ruta
        assert "DNI" not in html, ruta


def test_manual_de_uso_accesible(client):
    html = client.get("/manual").text
    assert "Manual de usuario" in html
    assert "Ingresos" in html
    assert "Desguace" in html
    assert "Borrado seguro" in html
    assert "dos filas ya visibles" in html
    assert "Nombre y Apellido" in html
    assert "Teléfono" in html
    # El metadato solo puede aparecer en el <head>, nunca en el contenido visible.
    assert html.count(AUTHOR) == 1
    inicio_contenido = html.find("<main")
    fin_contenido = html.find("</main>", inicio_contenido)
    assert AUTHOR not in html[inicio_contenido:fin_contenido]
