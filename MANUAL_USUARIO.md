# Manual de usuario — Electrogreem - Inventario

Electrogreem S.R.L. · Gestión integral de RAEE · Tucumán, Argentina

Este manual explica la operatoria diaria del sistema. La aplicación se ejecuta en la red local (LAN), se abre desde un navegador y no requiere conexión a internet.

---

## 1. Acceso

En la computadora servidor con Windows, hacé doble clic en el acceso directo **Electrogreem - Inventario** del escritorio. El lanzador inicia el servidor local en segundo plano (sin mostrar una ventana de consola que pueda cerrarse por error) y abre automáticamente el sistema en el navegador en `http://localhost:8000`.

Si necesitás acceder desde otra computadora o dispositivo conectado a la misma red local (LAN), abrí el navegador e ingresá a la dirección IP local del equipo servidor en el puerto `8000` (por ejemplo, `http://192.168.1.50:8000`). En Linux, podés iniciar el servicio desde terminal con `./iniciar.sh` y abrir `http://localhost:8000` o la IP local correspondiente.

El sistema no solicita usuario ni contraseña: está pensado para uso interno en la red local. Al apagar el equipo servidor desde Windows al final de la jornada, el sistema se cierra de forma ordenada; si necesitás detener el proceso de Python manualmente, podés hacerlo desde el Administrador de tareas.

---

## Cómo cargar mi primera información

Si es tu primera vez en el sistema, seguí estos cuatro pasos en orden. No necesitás conocimientos técnicos: completá los formularios con los datos que tengas a mano y guardá al final de cada paso.

### Paso 1: Crear o seleccionar la entidad (origen/contraparte)

Antes de registrar equipos o lotes, definí la entidad: quién entrega los RAEE o a dónde van destinados. Entrá al menú **Entidades** y presioná **+ Nueva entidad** (si ya existe, buscala en la lista y seleccionala). Cargá el **nombre o razón social** de forma uniforme —siempre el mismo texto, sin variantes ni abreviaturas distintas entre cargas—, el **tipo/rol** (`Generador`, `Receptor de donaciones`, `Operador / Reciclador` u `Otro`) y los datos disponibles (nombre corto, CUIT, provincia/localidad y contacto). Guardá con **Guardar entidad**. Si falta algún dato opcional, dejalo en blanco y completalo más adelante editando la entidad.

### Paso 2: Cargar el primer ingreso o lote de RAEE

En el menú **Ingresos**, presioná **+ Nuevo ingreso**. Elegí la entidad del paso anterior como **Generador**, la **fecha y hora de retiro** y, si lo tenés, el número de **Remito / Manifiesto**. Agregá una fila por cada tipo de equipo o material con **+ Agregar fila de ítem** y completá:

- **Categoría/tipo** (y subtipo si corresponde).
- **Cantidad** de unidades y **peso unitario en kg** (por ejemplo, `0.15` equivale a 150 gramos).
- **Estado inicial**: el sistema lo asigna automáticamente como `En recepción`.
- **Observaciones**: cargá en el campo **Resumen** del ingreso la marca, el modelo, el número de serie, el estado físico o el remito; en unidades de almacenamiento podés usar además los campos específicos (número de serie, capacidad, estado SMART).

Presioná **Registrar ingreso**: el sistema genera el código del ingreso (`ING-AAAA-00001`) y un código `RAEE-AAAA-000001` por cada unidad creada.

### Paso 3: Registrar movimientos, clasificación o cambios de estado

En el menú **Inventario**, buscá el equipo por código, marca o modelo y abrí su ficha. Desde ahí podés usar **Cambiar estado** (por ejemplo, pasar de `En recepción` a `En revisión`, `Recuperado` o `Para donar`) y agregar especificaciones técnicas. Si el equipo es irreparable, registrá el **desguace / recuperación**; si está listo para entregar, incluilo en una **donación**. Si te equivocaste en una carga, editá y guardá la corrección en la vista correspondiente; cuando un registro ya no deba usarse, dalo de baja o desactivalo (por ejemplo, **Activar / Desactivar** en entidades) para conservar su historial en lugar de perderlo.

### Paso 4: Revisar los tableros y cerrar la jornada

Volvé al **Panel principal** para ver los ítems registrados, el stock activo, el peso total, las donaciones y el CO2e, y mirá **Impacto ambiental** para ver el resumen de recuperación y reciclaje (son cifras estimativas, explicadas en ese módulo). Al terminar de cargar, apagá Windows de forma ordenada desde el menú Inicio: el servidor local se cierra junto con el equipo y no hace falta hacer nada más.

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

1. **Reutilización y donación**: equipos en estado `Recuperado` o `Donado`, según factor por categoría.
2. **Reciclaje y valorización**: kilogramos de materiales recuperados multiplicados por su factor.

Usá los campos **Desde** y **Hasta** para filtrar por rango de fechas y presioná **Aplicar filtro**.

Se muestran equivalencias comprensibles (árboles por año y kilómetros evitados en auto) y un desglose por categoría y por material. El botón **Vista imprimible para gerencia** abre un informe limpio listo para imprimir.

> **Todas las cifras mostradas son estimativas.** Son valores orientativos calculados según los factores cargados en el sistema y los pesos y cantidades registrados; **no constituyen una medición exacta ni una certificación ambiental oficial**.

### Cómo leer e interpretar los números

- **Cantidades e ítems según estado**: cada equipo tiene su propio código `RAEE-AAAA-000001` y un estado (`En recepción`, `En revisión`, `Recuperado`, `Para donar`, `Donado`, `Reciclado` o `Desguazado`). El panel y el inventario muestran cuántos ítems hay en cada estado. En Impacto ambiental solo se cuentan los ítems `Recuperados` y `Donados`, que son los que se consideran reutilizados; el número de la columna **Cant.** es la cantidad de equipos de esa categoría incluidos en el cálculo.
- **Kilogramos y fracciones**: el peso se expresa siempre en kg con decimales (por ejemplo, `0.15` kg son 150 g). Conviene distinguir el **peso confirmado** —obtenido al pesar el equipo o el material en una balanza— del **peso estimado** —declarado a simple vista o tomado de un remito—. El sistema suma ambos tal como se cargaron: si un peso fue estimado, aclaralo en las observaciones para no confundirlo con un pesaje real. Los kilogramos de materiales recuperados son los que se usan para calcular el reciclaje.
- **Indicadores de CO₂e evitado**: son estimaciones que resultan de multiplicar cada ítem recuperado o donado por el factor de su categoría y cada kg de material recuperado por el factor de ese material. El **total evitado** es la suma de ambos enfoques; las equivalencias en árboles por año o kilómetros en auto son solo comparaciones ilustrativas, no mediciones reales de emisiones.

---

## 11. Preguntas frecuentes

**¿Qué hago si no arranca el sistema?**  
Verificá que Python 3.10 o superior esté instalado y volvé a ejecutar `iniciar.bat`. El script crea el entorno virtual, instala dependencias y genera la base automáticamente.

**¿Solo yo puedo utilizar el sistema?**  
No, cualquier dispositivo en la misma red local (LAN) puede acceder ingresando a `http://<IP-DEL-SERVIDOR>:8000`, y en el equipo servidor también con `http://localhost:8000`.

**¿Qué pasa si cargo determinada información y otro usuario quiere hacer lo mismo?**  
Todos trabajan sobre la misma base de datos central (`data/raee.db`) del servidor; cada cambio guardado se refleja para todos. Recomendamos coordinar las cargas simultáneas sobre un mismo lote para no duplicar entradas.

**Me equivoqué de datos: ¿puedo editar/agregar/actualizar/eliminar información?**  
Sí, desde las vistas del sistema se pueden agregar nuevos registros, editar o actualizar datos existentes y eliminar o dar de baja registros cuando corresponda.

**¿Qué sucede si en pleno uso del sistema se apaga la PC?**  
El servidor local se detiene y los navegadores pierden conexión hasta volver a encender la PC e iniciar el sistema. Los registros ya confirmados antes del corte quedan guardados en SQLite, mientras que una operación sin guardar al instante del apagón no queda asentada.

**¿Qué pasa si ingresa un RAEE que no está en la lista, con su respectiva marca, modelo, número de serie y demás datos que correspondan?**  
Seleccioná la categoría o tipo general más cercano disponible en el listado (o la opción genérica/otros si corresponde) y asentá la marca, el modelo, el número de serie, el estado físico y cualquier dato técnico relevante en los campos específicos del equipo o en las observaciones del registro, para no perder trazabilidad.

**¿Qué pasa si no cuento con alguna información a llenar de una entidad?**  
Cargá la entidad con los datos mínimos obligatorios disponibles (como el nombre o razón social y su tipo/rol) y dejá en blanco o como pendiente los datos opcionales que aún no tengas (por ejemplo teléfono, correo o dirección); más adelante podés editar la entidad para completarlos sin afectar los movimientos ya registrados.

**¿Se puede usar desde el celular o una tablet?**  
Sí. La interfaz se adapta a cualquier resolución: en pantallas chicas el menú se abre con el botón ☰.

**¿Dónde se guardan los comprobantes adjuntos?**  
En la carpeta `data/adjuntos/`, dentro de la carpeta del proyecto. Realizá copias de seguridad de la carpeta `data/` completa.
