from __future__ import annotations

from collections.abc import Mapping

from starlette.datastructures import FormData

from app.schemas import OperarioInterviniente


def desde_formulario(form: FormData, cantidad: int) -> list[dict[str, str]]:
    """Convierte las filas del formulario en la estructura persistida.

    Formato actual: ``operario_nombre_{i}`` y ``operario_telefono_{i}``.
    Formato histórico: ``operario_{i}`` con solo el nombre; se conserva para
    no perder ingresos cargados antes de este cambio.
    """

    def txt(name: str) -> str:
        return str(form.get(name) or "").strip()

    operarios: list[dict[str, str]] = []
    for i in range(max(0, cantidad)):
        nombre = txt(f"operario_nombre_{i}")
        telefono = txt(f"operario_telefono_{i}")
        if not nombre and not telefono:
            nombre = txt(f"operario_{i}")
        if not nombre and not telefono:
            continue
        operarios.append(
            OperarioInterviniente(nombre=nombre, telefono=telefono).model_dump()
        )
    return operarios


def normalizar(op: object) -> dict[str, str]:
    """Devuelve un operario en el esquema actual, sea dict o texto histórico."""
    if isinstance(op, Mapping):
        return OperarioInterviniente.model_validate(op).model_dump()
    return OperarioInterviniente(nombre=str(op or "").strip()).model_dump()
