# Sistema de Gestión e Inventario RAEE

Aplicación web de arquitectura cliente-servidor diseñada para operar en red local (LAN) sin depender de conexión a internet en tiempo de ejecución. Permite administrar de forma integral la recepción, trazabilidad, reacondicionamiento y valorización de Residuos de Aparatos Eléctricos y Electrónicos (RAEE) bajo un enfoque de economía circular.

## Funcionalidades principales

- **Trazabilidad por lote e ítem:** Registro de ingresos por generador o cliente con asignación automática de códigos correlativos individuales, estado operativo y especificaciones técnicas.
- **Reacondicionamiento y donaciones:** Control de equipos recuperados y emisión de actas formales de entrega institucional.
- **Certificación de borrado seguro:** Registro técnico de unidades de almacenamiento y emisión de constancias de sanitización de datos o destrucción física.
- **Desguace y valorización de materiales:** Inventario en kilogramos de fracciones recuperadas (metales, plásticos, placas electrónicas) con trazabilidad de movimientos.
- **Indicadores de impacto ambiental:** Cálculo automático de emisiones de $\text{CO}_2\text{e}$ evitadas por reutilización y reciclaje, con reportes ejecutivos imprimibles.

## Stack tecnológico

- **Backend:** Python, FastAPI, SQLAlchemy y SQLite.
- **Frontend:** HTML5, Jinja2, Tailwind CSS y Alpine.js (empaquetados localmente).
- **Testing:** Suite de pruebas automatizadas con `pytest`.
