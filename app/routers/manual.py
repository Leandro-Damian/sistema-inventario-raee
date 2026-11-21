from __future__ import annotations

import html

from fastapi import APIRouter, Request

from app.config import BASE_DIR
from app.templating import page

router = APIRouter()

MANUAL_PATH = BASE_DIR / "MANUAL_USUARIO.md"


def _a_html(texto: str) -> str:
    try:
        import markdown

        return markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])
    except ImportError:
        # Fallback mínimo y offline si no está instalado markdown.
        partes = [html.escape(linea) for linea in texto.split("\n")]
        salida: list[str] = []
        en_lista = False
        for p in partes:
            if p.startswith("## "):
                salida.append(f"<h2>{p[3:]}</h2>")
            elif p.startswith("### "):
                salida.append(f"<h3>{p[4:]}</h3>")
            elif p.startswith("# "):
                salida.append(f"<h1>{p[2:]}</h1>")
            elif p.startswith("- "):
                if not en_lista:
                    salida.append("<ul>")
                    en_lista = True
                salida.append(f"<li>{p[2:]}</li>")
            else:
                if en_lista:
                    salida.append("</ul>")
                    en_lista = False
                if p.strip():
                    salida.append(f"<p>{p}</p>")
        if en_lista:
            salida.append("</ul>")
        return "".join(salida)


@router.get("/manual")
def manual(request: Request):
    texto = MANUAL_PATH.read_text(encoding="utf-8") if MANUAL_PATH.exists() else "# Manual de uso"
    return page(request, "manual.html", contenido=_a_html(texto))
