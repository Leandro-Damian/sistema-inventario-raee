"""Genera los favicons oficiales a partir de ``electrogreem-logo.jpg``.

Requiere Pillow (solo en el entorno de desarrollo, no en tiempo de ejecución):

    .venv\\Scripts\\python.exe -m pip install Pillow
    .venv\\Scripts\\python.exe scripts/generar_favicons.py

Los archivos se escriben en ``src/static/img`` (copia limpia, por ejemplo para
un acceso directo de Windows) y se replican en ``app/static/img``, que es el
directorio que FastAPI monta en ``/static``.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGEN = BASE_DIR / "electrogreem-logo.jpg"
DESTINO_SRC = BASE_DIR / "src" / "static" / "img"
DESTINO_APP = BASE_DIR / "app" / "static" / "img"
BLANCO = (255, 255, 255)


def recortar_margenes(imagen: Image.Image) -> Image.Image:
    """Recorta el fondo casi blanco y deja el isotipo centrado en un cuadrado."""
    rgb = imagen.convert("RGB")
    pixeles = rgb.load()
    ancho, alto = rgb.size
    min_x, min_y, max_x, max_y = ancho, alto, -1, -1

    for y in range(alto):
        for x in range(ancho):
            rojo, verde, azul = pixeles[x, y]
            if min(rojo, verde, azul) < 245:  # tolera el ruido JPEG del blanco
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x < min_x:  # imagen completamente blanca: no se puede recortar
        return rgb

    recorte = rgb.crop((min_x, min_y, max_x + 1, max_y + 1))
    lado = max(recorte.size) + 8  # pequeño respiro alrededor del isotipo
    lienzo = Image.new("RGB", (lado, lado), BLANCO)
    offset_x = (lado - recorte.width) // 2
    offset_y = (lado - recorte.height) // 2
    lienzo.paste(recorte, (offset_x, offset_y))
    return lienzo


def reducir(imagen: Image.Image, tamano: int) -> Image.Image:
    """Redimensiona con Lanczos y aplica nitidez suave para iconos pequeños."""
    reducida = imagen.resize((tamano, tamano), Image.Resampling.LANCZOS)
    return reducida.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))


def main() -> None:
    if not ORIGEN.exists():
        raise SystemExit(f"No se encontró la imagen de origen: {ORIGEN}")

    DESTINO_SRC.mkdir(parents=True, exist_ok=True)
    DESTINO_APP.mkdir(parents=True, exist_ok=True)

    limpia = recortar_margenes(Image.open(ORIGEN))
    print(f"Isotipo recortado y centrado: {limpia.size[0]}x{limpia.size[1]} px")

    ico = DESTINO_SRC / "favicon.ico"
    limpia.save(
        ico,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    png = DESTINO_SRC / "favicon.png"
    reducir(limpia, 180).save(png, format="PNG", optimize=True)

    for archivo in (ico, png):
        destino = DESTINO_APP / archivo.name
        shutil.copy2(archivo, destino)
        print(f"{archivo.relative_to(BASE_DIR)} -> {destino.relative_to(BASE_DIR)} ({destino.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
