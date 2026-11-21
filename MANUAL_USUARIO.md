# Manual de usuario — Electrogreem - Inventario

Gestión integral de RAEE · Tucumán, Argentina

Este manual explica la operatoria diaria del sistema. La aplicación se ejecuta en la red local (LAN), se abre desde un navegador y no requiere conexión a internet.

---

## 1. Acceso

1. En la computadora servidor, ejecutá `iniciar.bat` (Windows) o `iniciar.sh` (Linux).
2. La consola mostrará la **IP local** del equipo, por ejemplo `http://192.168.1.50:8000`.
3. En cualquier dispositivo conectado a la misma red, abrí el navegador y escribí esa dirección.
4. También podés usar `http://localhost:8000` en la propia computadora servidor.
5. **Minimizá la ventana negra de la consola** (botón `─`) mientras el sistema esté en uso en la red local. **Nunca la cierres con la X**: al cerrarla se detiene el servidor y los demás dispositivos pierden acceso.

Al terminar la jornada, **volvé a la consola** (está minimizada en la barra de tareas) y presioná `Ctrl + C`. Recién después podés cerrar la ventana.

> El sistema no solicita usuario ni contraseña: está pensado para uso interno en la red local.

---

## 2. Panel principal

Es la pantalla de inicio. Muestra en tiempo real:

- Ítems registrados y cuántos están en **stock activo**.
- Peso total ingresado en kilogramos.
- Equipos donados.
- Materiales valorizados en kilogramos.
- CO2e total evitado.

Además incluye el inventario por estado, las categorías más frecuentes, los últimos ingresos y las últimas donaciones. Desde aquí podés iniciar un nuevo ingreso con el botón **+ Nuevo ingreso**.

---

## 3. Entidades

Menú **Entidades**. Aquí se cargan empresas e instituciones.

### Alta y edición

1. Presioná **+ Nueva entidad**.
2. Completá razón social (obligatoria), nombre corto, CUIT, tipo, provincia y localidad.
3. En el bloque **Contacto de referencia** cargá exactamente cuatro datos: **Nombre y Apellido**, **Cargo o Función**, **Email** y **Teléfono**.
4. Guardá con **Guardar entidad**.

Para modificar, presioná **Editar** en la fila correspondiente.

### Tipos de entidad

- `Generador`: quien entrega los RAEE.
- `Receptor de donaciones`: escuelas, fundaciones, etc.
- `Operador / Reciclador`: destino de materiales o salidas.
- `Otro`.

### Búsqueda y activación

Usá el cuadro de búsqueda por razón social, nombre corto, CUIT o localidad. El botón **Activar / Desactivar** permite dar de baja una entidad sin borrar su historial.

---

## 4. Ingresos

Menú **Ingresos**. Registra cada retiro o recepción.

### Paso 1 — Datos del retiro

Seleccioná el **Generador**, la **fecha y hora de retiro**, el número de **Remito / Manifiesto**, el **peso total declarado** y un **resumen** de lo retirado.

### Paso 2 — Transporte

Completá marca y modelo del camión, patente, empresa de transporte, y del chofer solo **Nombre y Apellido** y **Teléfono**.

En **Operarios intervinientes** el formulario inicia con **dos filas ya visibles**, ya que habitualmente viajan dos operarios. De cada uno se solicitan **Nombre y Apellido** y **Teléfono**. Podés quitar cualquiera con **Quitar** y agregar más con **+ Agregar operario**. No se solicita ningún documento de identidad.

### Paso 3 — Carga rápida de ítems

Presioná **+ Agregar fila de ítem** por cada tipo de equipo o material.

- **Categoría**: elegila de la lista. Si elegís **Cables**, aparece el selector de tipo (RJ45/Red, VGA, HDMI, Power C13, USB, Jack/Audio, Impresora/Datos, Otros).
- **Marca** y **Modelo**.
- **Cantidad**: por defecto es `1`. Si cargás, por ejemplo, `26` gabinetes, el sistema genera automáticamente 26 códigos `RAEE-AAAA-000001`, `RAEE-AAAA-000002`, etc., con el mismo peso unitario.
- **Peso unitario (kg)**: se multiplica por la cantidad para el peso total del lote.
  > **Nota práctica:** escribí el peso directamente como número decimal. Por ejemplo, `0.15` significa **150 gramos** y `1.0` equivale a **1 kilogramo**. No hace falta usar las flechitas de incremento: avanzan de `0.001` kg en `0.001` kg y son poco prácticas para cargar pesos reales.
- **Atributos opcionales**: usá **+ Agregar fila** para cargar pares clave/valor. Al elegir *Memorias RAM* se sugieren `Tipo (DDR1/DDR2/DDR3/DDR4/DDR5)`, `Capacidad (GB)` y `Frecuencia`; al elegir *Procesadores (CPU)* se sugieren `Marca (Intel/AMD)`, `Familia / Modelo` y `Socket`. Podés editar o borrar estas filas libremente.
- **Unidades de Almacenamiento**: despliega una ficha estructurada con Tipo (HDD, SSD, NVMe, USB, Otro), Factor de forma / Pulgadas, Interfaz, Capacidad, Número de serie, Estado de salud / SMART y Disposición.

No se solicita número de serie ni ubicación física en la carga rápida, salvo en la ficha específica de almacenamiento.

### Paso 4 — Registrar

Presioná **Registrar ingreso**. El sistema genera el código correlativo `ING-AAAA-00001` y te lleva al detalle, donde se listan todos los ítems creados.

---

## 5. Inventario

Menú **Inventario**. Lista todos los ítems unitarios con su código `RAEE-AAAA-000001`.

### Búsqueda, filtros y exportación

Podés filtrar por texto (código, marca, modelo o número de serie), por **estado** y por **categoría**. El botón **Exportar CSV** descarga el resultado con los filtros aplicados.

### Estados

Los estados son exactamente: `En recepción`, `En revisión`, `Recuperado`, `Para donar`, `Donado`, `Reciclado` y `Desguazado`. En la ficha de cada ítem podés cambiar el estado con el selector **Cambiar estado**.

### Especificaciones

En la ficha del ítem, la sección **Especificaciones técnicas** permite agregar cualquier par clave/valor nuevo, editarlo o eliminarlo. No hay límites predefinidos.

---

## 6. Desguace y recuperación de componentes

Desde la ficha de un equipo irreparable, presioná **Registrar desguace / recuperación**.

1. Cargá cada componente extraído (categoría, marca, modelo, cantidad y peso unitario).
2. Elegí el **estado final del chasis restante**: `Desguazado` o `Reciclado`.
3. Guardá con **Registrar desguace**.

Los componentes se dan de alta en inventario como `Recuperado`, reciben su propio código y quedan vinculados al equipo origen. En la ficha del equipo origen se listan todos ellos.

---

## 7. Borrado seguro y destrucción de datos

Está disponible dentro de la ficha de una **Unidad de Almacenamiento**, mediante el botón **Borrado seguro / Destrucción**.

Completá:

- Entidad de origen (si aplica).
- Tipo, capacidad, interfaz y estado SMART de la unidad.
- **Número de serie verificado** (obligatorio).
- **Modalidad**: `Destrucción física` (prensa, taladro, etc.) o `Borrado por software`.
- Nombre del software o herramienta física.
- Método / técnica utilizada.
- Fecha y hora.
- **Estándar compatible**: `NIST SP 800-88`, `IEEE 2883`, `DoD 5220.22-M` o `Físico`.
- Adjunto del comprobante (opcional).

Al guardar se genera una **constancia imprimible** desde **Ver certificado**.

---

## 8. Materiales recuperados

Menú **Materiales recuperados**.

### Crear tipos de materiales

Además de los materiales base (cobre, aluminio, hierro, plástico, placas electrónicas y cables sin pelar), podés crear nuevos tipos como plata, oro, bronce o vidrio, indicando su **factor de CO2e evitado por kg**.

### Altas y salidas

- **Alta de pesaje**: suma kilogramos al stock. Indicá material, kg, fecha, referencia y observación.
- **Salida por entrega / venta**: descuenta kilogramos y permite indicar el reciclador destino.

La tabla **Stock por material** muestra entradas, salidas, stock actual y factor. El **detalle de movimientos** conserva todo el historial de pesajes y entregas.

---

## 9. Donaciones

Menú **Donaciones**.

1. Presioná **+ Nueva donación**.
2. Elegí la **entidad receptora** (debe estar activa y ser del tipo *Receptor de donaciones*) y la fecha.
3. Marcá los equipos disponibles, que son los que están en estado `Para donar` o `Recuperado`.
4. Guardá con **Registrar donación**.

Los equipos pasan automáticamente a estado `Donado` y se genera el acta. Desde el detalle de la donación podés **Ver / imprimir acta**, que incluye el listado de equipos, pesos y espacios para firmas.

---

## 10. Impacto ambiental

Menú **Impacto ambiental**. Contabiliza el CO2e evitado con dos enfoques:

1. **Reutilización y donación**: equipos donados y recuperados, según factor por categoría.
2. **Reciclaje y valorización**: kilogramos de materiales recuperados multiplicados por su factor.

Usá los campos **Desde** y **Hasta** para filtrar por rango de fechas y presioná **Aplicar filtro**.

Se muestran equivalencias comprensibles (árboles por año y kilómetros evitados en auto) y un desglose por categoría y por material. El botón **Vista imprimible para gerencia** abre un informe limpio listo para imprimir.

---

## 11. Manual de uso

Este documento está disponible en todo momento desde el menú lateral, opción **Manual de uso**.

---

## 12. Preguntas frecuentes

**¿Qué hago si no arranca el sistema?**  
Verificá que Python 3.10 o superior esté instalado y volvé a ejecutar `iniciar.bat`. El script crea el entorno virtual, instala dependencias y genera la base automáticamente.

**¿Cómo arranco sin datos de ejemplo?**  
Ejecutá `python scripts/init_db.py --no-demo`. Si la base ya existe, primero borrá `data/raee.db` o usá `python scripts/init_db.py --reset` (esta última opción pide confirmación y elimina todos los datos).

**¿Se puede usar desde el celular o una tablet?**  
Sí. La interfaz se adapta a cualquier resolución: en pantallas chicas el menú se abre con el botón ☰.

**¿Dónde se guardan los comprobantes adjuntos?**  
En la carpeta `data/adjuntos/`, dentro de la carpeta del proyecto. Realizá copias de seguridad de la carpeta `data/` completa.
