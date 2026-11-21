from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OperarioInterviniente(BaseModel):
    """Esquema de cada operario que intervino en un retiro.

    Se persiste como JSON dentro de ``ingresos.operarios``. No incluye DNI
    ni ningún otro documento personal.
    """

    model_config = ConfigDict(extra="ignore")

    nombre: str = Field(default="", description="Nombre y Apellido")
    telefono: str = Field(default="", description="Teléfono")
