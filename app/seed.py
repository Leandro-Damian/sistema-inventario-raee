from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import TIPOS_MATERIAL_BASE
from app.models import (
    BorradoSeguro,
    Donacion,
    Entidad,
    Ingreso,
    Item,
    ItemEspecificacion,
    MovimientoMaterial,
    TipoMaterial,
)


def seed_catalogos(db: Session) -> None:
    """Catálogos y factores base. Idempotente, sin registros ficticios."""
    existentes = set(db.scalars(select(TipoMaterial.nombre)).all())
    for nombre, factor in TIPOS_MATERIAL_BASE:
        if nombre not in existentes:
            db.add(TipoMaterial(nombre=nombre, factor_co2e=factor, activo=True))
    db.commit()


def seed_demo(db: Session) -> None:
    """Datos de ejemplo para demostración. No se usa con --no-demo."""
    if db.scalar(select(Entidad).limit(1)) is not None:
        return

    generador = Entidad(
        razon_social="Municipalidad de San Miguel de Tucumán",
        nombre_corto="Municipalidad SMT",
        cuit="30-60000000-1",
        tipo="Generador",
        provincia="Tucumán",
        localidad="San Miguel de Tucumán",
        contacto_nombre="María Gómez",
        contacto_cargo="Responsable de Residuos",
        contacto_email="residuos@municipalidad.gob.ar",
        contacto_telefono="0381 400-0000",
    )
    receptor = Entidad(
        razon_social="Fundación Escuelas Digitales del Norte",
        nombre_corto="Fundación EDN",
        cuit="30-61111111-2",
        tipo="Receptor de donaciones",
        provincia="Tucumán",
        localidad="Yerba Buena",
        contacto_nombre="Carlos Pérez",
        contacto_cargo="Director de Programas",
        contacto_email="programas@fundacion-edn.org",
        contacto_telefono="0381 411-1111",
    )
    reciclador = Entidad(
        razon_social="Recicladora del Norte S.R.L.",
        nombre_corto="Recicladora Norte",
        cuit="30-62222222-3",
        tipo="Operador / Reciclador",
        provincia="Tucumán",
        localidad="Cerrillo",
        contacto_nombre="Ana Torres",
        contacto_cargo="Supervisora de Planta",
        contacto_email="planta@recicladoranorte.com.ar",
        contacto_telefono="0381 422-2222",
    )
    db.add_all([generador, receptor, reciclador])
    db.flush()

    base = datetime(2026, 10, 14, 9, 30)
    ingreso1 = Ingreso(
        codigo="ING-2026-00001",
        generador_id=generador.id,
        fecha_retiro=base,
        remito="R-0001-2026",
        peso_declarado=610.0,
        resumen="Retiro de equipos informáticos y cables de oficinas municipales.",
        camion="Ford F-100 3.5",
        patente="AB123CD",
        empresa_transporte="Transportes del Sur S.R.L.",
        chofer_nombre="Juan Ramírez",
        chofer_telefono="0381 433-3333",
        operarios=[
            {"nombre": "Lucas Fernández", "telefono": "0381 400-1111"},
            {"nombre": "Nicolás Díaz", "telefono": "0381 400-2222"},
        ],
    )
    ingreso2 = Ingreso(
        codigo="ING-2026-00002",
        generador_id=generador.id,
        fecha_retiro=base + timedelta(days=9),
        remito="R-0002-2026",
        peso_declarado=58.0,
        resumen="Periféricos y memorias RAM.",
        camion="Fiat Ducato 2.3",
        patente="XY987ZT",
        empresa_transporte="Transportes del Sur S.R.L.",
        chofer_nombre="Juan Ramírez",
        chofer_telefono="0381 433-3333",
        operarios=[{"nombre": "Lucas Fernández", "telefono": "0381 400-1111"}],
    )
    db.add_all([ingreso1, ingreso2])
    db.flush()

    def item(codigo, categoria, marca, modelo, peso, estado, ingreso, fecha, **extra):
        return Item(
            codigo=codigo,
            ingreso_id=ingreso.id,
            categoria=categoria,
            marca=marca,
            modelo=modelo,
            peso_unitario=peso,
            estado=estado,
            fecha=fecha,
            **extra,
        )

    items = [
        item("RAEE-2026-000001", "Computadoras de escritorio (Gabinete)", "HP", "Compaq 6000 Pro", 9.5, "En revisión", ingreso1, base),
        item("RAEE-2026-000002", "Monitores", "Samsung", "SyncMaster 740N", 5.2, "Para donar", ingreso1, base),
        item("RAEE-2026-000003", "Cables", "Genérico", "VGA", 0.2, "En recepción", ingreso1, base, subcategoria="VGA"),
        item("RAEE-2026-000004", "Impresoras y Escáneres", "HP", "LaserJet P1102w", 7.1, "Recuperado", ingreso1, base),
        item("RAEE-2026-000005", "Unidades de Almacenamiento", "Seagate", "Barracuda 500 GB", 0.6, "Recuperado", ingreso1, base,
             numero_serie="SN-DEMO-001", tipo_unidad="HDD", factor_forma='3.5"', interfaz="SATA", capacidad="500 GB",
             salud_smart="Saludable", disposicion="Para donar"),
        item("RAEE-2026-000006", "Memorias RAM", "Kingston", "KVR16N11/8", 0.05, "Recuperado", ingreso2, base + timedelta(days=9)),
        item("RAEE-2026-000007", "Procesadores (CPU)", "Intel", "Core i5-3470", 0.1, "Recuperado", ingreso2, base + timedelta(days=9)),
    ]
    db.add_all(items)
    db.flush()

    for esp in [
        ItemEspecificacion(item_id=items[5].id, clave="Tipo (DDR1/DDR2/DDR3/DDR4/DDR5)", valor="DDR3"),
        ItemEspecificacion(item_id=items[5].id, clave="Capacidad (GB)", valor="8"),
        ItemEspecificacion(item_id=items[5].id, clave="Frecuencia", valor="1600 MHz"),
        ItemEspecificacion(item_id=items[6].id, clave="Marca (Intel/AMD)", valor="Intel"),
        ItemEspecificacion(item_id=items[6].id, clave="Familia / Modelo", valor="Core i5-3470"),
        ItemEspecificacion(item_id=items[6].id, clave="Socket", valor="LGA1155"),
    ]:
        db.add(esp)

    donacion = Donacion(
        codigo="DON-2026-00001",
        entidad_id=receptor.id,
        fecha=base + timedelta(days=12),
        observaciones="Entrega de equipos reacondicionados a escuela técnica.",
    )
    db.add(donacion)
    db.flush()
    for it in (items[1], items[4]):
        it.estado = "Donado"
        it.donacion_id = donacion.id
        it.fecha_donacion = donacion.fecha

    db.add(
        BorradoSeguro(
            item_id=items[3].id,
            entidad_origen_id=generador.id,
            tipo="Impresora",
            capacidad="—",
            interfaz="USB",
            salud_smart="—",
            numero_serie_verificado="SN-DEMO-imp",
            modalidad="Borrado por software",
            herramienta="Blancco Drive Eraser",
            metodo="Sobrescritura de 3 pasos sobre memoria interna.",
            fecha_hora=base + timedelta(days=10),
            estandar="NIST SP 800-88",
        )
    )

    cobre = db.scalar(select(TipoMaterial).where(TipoMaterial.nombre == "Cobre de cables"))
    plastico = db.scalar(select(TipoMaterial).where(TipoMaterial.nombre == "Plástico"))
    db.add_all([
        MovimientoMaterial(tipo_material_id=cobre.id, tipo="alta", kg=12.5, fecha=base + timedelta(days=11),
                           referencia="Desarme ING-2026-00001", observacion="Cableado RJ45 y VGA."),
        MovimientoMaterial(tipo_material_id=plastico.id, tipo="alta", kg=8.0, fecha=base + timedelta(days=11),
                           referencia="Desarme ING-2026-00001", observacion="Carkasas de gabinete."),
        MovimientoMaterial(tipo_material_id=cobre.id, tipo="salida", kg=4.0, fecha=base + timedelta(days=15),
                           referencia="Remito RC-77", observacion="Entrega a reciclador.", reciclador_id=reciclador.id),
    ])
    db.commit()
