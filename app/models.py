from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Secuencia(Base):
    __tablename__ = "secuencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prefijo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ultimo: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Entidad(Base):
    __tablename__ = "entidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    razon_social: Mapped[str] = mapped_column(String(200), nullable=False)
    nombre_corto: Mapped[str] = mapped_column(String(80), default="", nullable=False)
    cuit: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    tipo: Mapped[str] = mapped_column(String(60), nullable=False)
    provincia: Mapped[str] = mapped_column(String(80), default="", nullable=False)
    localidad: Mapped[str] = mapped_column(String(80), default="", nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Bloque único de contacto: exactamente cuatro campos.
    contacto_nombre: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    contacto_cargo: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    contacto_email: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    contacto_telefono: Mapped[str] = mapped_column(String(60), default="", nullable=False)

    ingresos: Mapped[list["Ingreso"]] = relationship(back_populates="generador")
    donaciones: Mapped[list["Donacion"]] = relationship(back_populates="entidad")
    movimientos: Mapped[list["MovimientoMaterial"]] = relationship(back_populates="reciclador")
    borrados: Mapped[list["BorradoSeguro"]] = relationship(back_populates="entidad_origen")


class Ingreso(Base):
    __tablename__ = "ingresos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    generador_id: Mapped[int] = mapped_column(ForeignKey("entidades.id"), nullable=False)
    fecha_retiro: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    remito: Mapped[str] = mapped_column(String(80), default="", nullable=False)
    peso_declarado: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    resumen: Mapped[str] = mapped_column(Text, default="", nullable=False)

    camion: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    patente: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    empresa_transporte: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    chofer_nombre: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    chofer_telefono: Mapped[str] = mapped_column(String(60), default="", nullable=False)
    operarios: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    generador: Mapped["Entidad"] = relationship(back_populates="ingresos")
    items: Mapped[list["Item"]] = relationship(back_populates="ingreso", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    ingreso_id: Mapped[int] = mapped_column(ForeignKey("ingresos.id"), nullable=False)
    categoria: Mapped[str] = mapped_column(String(80), nullable=False)
    subcategoria: Mapped[str] = mapped_column(String(80), default="", nullable=False)
    marca: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    modelo: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    peso_unitario: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estado: Mapped[str] = mapped_column(String(40), nullable=False, index=True)

    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    fecha_donacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Ficha estructurada de unidades de almacenamiento
    numero_serie: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    tipo_unidad: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    factor_forma: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    interfaz: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    capacidad: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    salud_smart: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    disposicion: Mapped[str] = mapped_column(String(60), default="", nullable=False)

    # Trazabilidad de desguace y donación
    origen_id: Mapped[int | None] = mapped_column(ForeignKey("items.id"), nullable=True)
    donacion_id: Mapped[int | None] = mapped_column(ForeignKey("donaciones.id"), nullable=True)

    ingreso: Mapped["Ingreso"] = relationship(back_populates="items")
    donacion: Mapped["Donacion | None"] = relationship(back_populates="items")
    origen: Mapped["Item | None"] = relationship(
        remote_side="Item.id",
        back_populates="componentes",
        foreign_keys=[origen_id],
    )
    componentes: Mapped[list["Item"]] = relationship(
        back_populates="origen",
        foreign_keys=[origen_id],
    )
    especificaciones: Mapped[list["ItemEspecificacion"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )
    borrados: Mapped[list["BorradoSeguro"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )


class ItemEspecificacion(Base):
    __tablename__ = "item_especificaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    clave: Mapped[str] = mapped_column(String(120), nullable=False)
    valor: Mapped[str] = mapped_column(String(250), default="", nullable=False)

    item: Mapped["Item"] = relationship(back_populates="especificaciones")


class Donacion(Base):
    __tablename__ = "donaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    entidad_id: Mapped[int] = mapped_column(ForeignKey("entidades.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    observaciones: Mapped[str] = mapped_column(Text, default="", nullable=False)

    entidad: Mapped["Entidad"] = relationship(back_populates="donaciones")
    items: Mapped[list["Item"]] = relationship(back_populates="donacion")


class TipoMaterial(Base):
    __tablename__ = "tipos_material"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    factor_co2e: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    movimientos: Mapped[list["MovimientoMaterial"]] = relationship(back_populates="tipo_material")


class MovimientoMaterial(Base):
    __tablename__ = "movimientos_material"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_material_id: Mapped[int] = mapped_column(ForeignKey("tipos_material.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    kg: Mapped[float] = mapped_column(Float, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    referencia: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    observacion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    reciclador_id: Mapped[int | None] = mapped_column(ForeignKey("entidades.id"), nullable=True)

    tipo_material: Mapped["TipoMaterial"] = relationship(back_populates="movimientos")
    reciclador: Mapped["Entidad | None"] = relationship(back_populates="movimientos")


class BorradoSeguro(Base):
    __tablename__ = "borrados_seguros"
    __table_args__ = (UniqueConstraint("item_id", name="uq_borrado_item"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    entidad_origen_id: Mapped[int | None] = mapped_column(ForeignKey("entidades.id"), nullable=True)

    tipo: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    capacidad: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    interfaz: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    salud_smart: Mapped[str] = mapped_column(String(40), default="", nullable=False)
    numero_serie_verificado: Mapped[str] = mapped_column(String(100), default="", nullable=False)

    modalidad: Mapped[str] = mapped_column(String(60), nullable=False)
    herramienta: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    metodo: Mapped[str] = mapped_column(Text, default="", nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estandar: Mapped[str] = mapped_column(String(60), nullable=False)
    comprobante_path: Mapped[str] = mapped_column(String(300), default="", nullable=False)

    item: Mapped["Item"] = relationship(back_populates="borrados")
    entidad_origen: Mapped["Entidad | None"] = relationship(back_populates="borrados")
