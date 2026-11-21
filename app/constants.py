from __future__ import annotations

# ---------------------------------------------------------------------------
# Catálogos cerrados y factores base del sistema
# ---------------------------------------------------------------------------

ESTADOS = [
    "En recepción",
    "En revisión",
    "Recuperado",
    "Para donar",
    "Donado",
    "Reciclado",
    "Desguazado",
]

ESTADOS_STOCK_ACTIVO = [
    "En recepción",
    "En revisión",
    "Recuperado",
    "Para donar",
]

TIPOS_ENTIDAD = [
    "Generador",
    "Receptor de donaciones",
    "Operador / Reciclador",
    "Otro",
]

CATEGORIAS = [
    "Computadoras de escritorio (Gabinete)",
    "Notebooks",
    "Monitores",
    "Impresoras y Escáneres",
    "Periféricos",
    "Cables",
    "Unidades de Almacenamiento",
    "Memorias RAM",
    "Procesadores (CPU)",
    "Placas Madre",
    "Fuentes de Alimentación",
    "Placas de Expansión / Video",
    "Redes y Telecomunicaciones",
    "Electrodomésticos menores",
    "Baterías y UPS",
    "Otros RAEE",
]

TIPOS_CABLE = [
    "RJ45 / Red",
    "VGA",
    "HDMI",
    "Power C13",
    "USB",
    "Jack / Audio",
    "Impresora / Datos",
    "Otros",
]

# Plantillas sugeridas: el usuario siempre puede agregar, editar o borrar filas.
PLANTILLAS_ATRIBUTOS = {
    "Memorias RAM": [
        "Tipo (DDR1/DDR2/DDR3/DDR4/DDR5)",
        "Capacidad (GB)",
        "Frecuencia",
    ],
    "Procesadores (CPU)": [
        "Marca (Intel/AMD)",
        "Familia / Modelo",
        "Socket",
    ],
}

TIPOS_UNIDAD_ALMACENAMIENTO = ["HDD", "SSD", "NVMe", "USB", "Otro"]
FACTORES_FORMA = ['3.5"', '2.5"', "M.2", "Otro"]
INTERFACES_ALMACENAMIENTO = ["SATA", "IDE", "NVMe / PCIe", "USB", "SAS"]
SALUD_SMART = ["Saludable", "En observación", "Dañado / No funcional"]
DISPOSICIONES = [
    "Uso propio",
    "Para donar",
    "Reciclado",
    "Pendiente de borrado/destrucción",
]

MODALIDADES_BORRADO = ["Destrucción física", "Borrado por software"]
ESTANDARES_BORRADO = ["NIST SP 800-88", "IEEE 2883", "DoD 5220.22-M", "Físico"]

TIPO_MOVIMIENTO_ALTA = "alta"
TIPO_MOVIMIENTO_SALIDA = "salida"

# Materiales base: solo catálogos y factores, sin registros ficticios.
TIPOS_MATERIAL_BASE = [
    ("Cobre de cables", 2.6),
    ("Aluminio", 8.0),
    ("Hierro / Chatarra ferrosa", 0.6),
    ("Plástico", 1.5),
    ("Placas electrónicas", 12.0),
    ("Cables sin pelar", 1.2),
]

# kg CO2e evitados por unidad reutilizada/donada, según categoría.
FACTORES_CO2E_POR_CATEGORIA = {
    "Computadoras de escritorio (Gabinete)": 150.0,
    "Notebooks": 120.0,
    "Monitores": 80.0,
    "Impresoras y Escáneres": 50.0,
    "Periféricos": 5.0,
    "Cables": 1.0,
    "Unidades de Almacenamiento": 20.0,
    "Memorias RAM": 3.0,
    "Procesadores (CPU)": 10.0,
    "Placas Madre": 8.0,
    "Fuentes de Alimentación": 5.0,
    "Placas de Expansión / Video": 10.0,
    "Redes y Telecomunicaciones": 8.0,
    "Electrodomésticos menores": 40.0,
    "Baterías y UPS": 15.0,
    "Otros RAEE": 10.0,
}

# Equivalencias comprensibles
KG_CO2E_POR_ARBOL_ANIO = 21.0
KG_CO2E_POR_KM_AUTO = 0.17
