# Sistema de Parqueadero Mejorado
## Documentación Técnica y Funcional

**Autor:** Edwar Botero Grajales  
**Fecha:** 7 de junio de 2025  
**Versión:** 3.0

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Idea del Proyecto](#idea-del-proyecto)
3. [Metodología de Desarrollo](#metodología-de-desarrollo)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Descripción de Módulos](#descripción-de-módulos)
6. [Flujo del Sistema](#flujo-del-sistema)
7. [Funcionalidades Principales](#funcionalidades-principales)
8. [Mejoras Implementadas](#mejoras-implementadas)
9. [Conclusiones y Recomendaciones](#conclusiones-y-recomendaciones)
10. [Referencias](#referencias)

## Introducción

Este documento presenta una explicación detallada del Sistema de Parqueadero Mejorado, una aplicación de escritorio desarrollada en Python con PyQt5 para la gestión eficiente de un parqueadero. El sistema permite registrar entradas y salidas de vehículos, calcular tarifas, gestionar el historial y exportar datos para análisis.

La documentación abarca desde la idea conceptual del proyecto hasta los detalles técnicos de implementación, incluyendo la metodología seguida, la arquitectura del sistema, la descripción de cada módulo y el flujo de operación. También se detallan las funcionalidades principales y las mejoras implementadas respecto a versiones anteriores.

## Idea del Proyecto

El Sistema de Parqueadero Mejorado surge como respuesta a la necesidad de optimizar la gestión de parqueaderos, proporcionando una solución integral que automatiza los procesos de registro, cálculo de tarifas y generación de informes. La idea central es crear una aplicación que sea:

1. **Intuitiva y fácil de usar:** Interfaz gráfica amigable que permita a los operadores realizar tareas comunes con pocos clics.
2. **Precisa en el cálculo de tarifas:** Sistema de cálculo que considere horas completas y fracciones, con tarifas diferenciadas por tipo de vehículo.
3. **Robusta en el manejo de datos:** Almacenamiento persistente de información con validaciones para evitar errores.
4. **Flexible para análisis:** Capacidad de filtrar y exportar datos para análisis posteriores.

El proyecto está orientado a pequeños y medianos establecimientos de parqueadero que necesitan una solución informática accesible pero completa para mejorar su operación diaria, reducir errores y optimizar la atención al cliente.

## Metodología de Desarrollo

Para el desarrollo del Sistema de Parqueadero Mejorado se ha seguido una metodología ágil adaptada, con elementos de Scrum y desarrollo iterativo incremental. Esta metodología ha permitido construir el sistema de manera progresiva, incorporando mejoras y nuevas funcionalidades en cada iteración.

### Fases del Desarrollo

1. **Análisis de Requisitos:**
   - Identificación de necesidades del usuario
   - Definición de funcionalidades clave
   - Establecimiento de restricciones y alcance

2. **Diseño:**
   - Diseño de la arquitectura del sistema
   - Diseño de la base de datos
   - Diseño de la interfaz de usuario
   - Definición de flujos de trabajo

3. **Implementación:**
   - Desarrollo modular (separación de lógica de negocio e interfaz)
   - Implementación incremental de funcionalidades
   - Pruebas unitarias durante el desarrollo

4. **Pruebas:**
   - Pruebas de integración
   - Pruebas de usabilidad
   - Validación de cálculos y operaciones

5. **Mejora Continua:**
   - Refactorización de código
   - Optimización de procesos
   - Incorporación de nuevas funcionalidades

### Principios Aplicados

- **Separación de Responsabilidades:** Clara división entre la lógica de negocio (database_mejorado.py) y la interfaz de usuario (gui_qt_mejorado.py).
- **Diseño Modular:** Componentes independientes que interactúan a través de interfaces bien definidas.
- **Validación Temprana:** Implementación de validaciones en tiempo real para mejorar la experiencia del usuario.
- **Persistencia de Datos:** Uso de SQLite para almacenamiento local, asegurando que los datos se mantengan entre sesiones.
- **Experiencia de Usuario:** Enfoque en crear una interfaz intuitiva y eficiente para el operador del parqueadero.

## Arquitectura del Sistema

El Sistema de Parqueadero Mejorado sigue una arquitectura de tres capas, que separa claramente la presentación, la lógica de negocio y el acceso a datos:

### 1. Capa de Presentación (GUI)

Implementada en el módulo `gui_qt_mejorado.py`, esta capa es responsable de:
- Mostrar la interfaz gráfica al usuario
- Capturar las interacciones del usuario
- Validar entradas en tiempo real
- Presentar resultados y mensajes

La interfaz se ha diseñado con PyQt5, utilizando un sistema de pestañas para organizar las diferentes funcionalidades y formularios intuitivos para la entrada de datos.

### 2. Capa de Lógica de Negocio

Implementada principalmente en el módulo `database_mejorado.py`, esta capa contiene:
- Reglas de negocio para el cálculo de tarifas
- Validación de datos
- Procesamiento de operaciones (ingresos, salidas, consultas)
- Lógica para exportación de datos

Aunque el nombre del archivo sugiere funcionalidad de base de datos, este módulo en realidad contiene toda la lógica de negocio del sistema, no solo el acceso a datos.

### 3. Capa de Datos

También implementada en `database_mejorado.py`, esta capa gestiona:
- Conexión con la base de datos SQLite
- Creación y mantenimiento de tablas
- Operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
- Consultas y filtrado de datos

### Punto de Entrada

El módulo `main_mejorado.py` sirve como punto de entrada a la aplicación, inicializando la interfaz gráfica y comenzando el bucle de eventos de la aplicación.

### Diagrama de Arquitectura

```
+------------------+
| main_mejorado.py |
+--------+---------+
         |
         v
+------------------+
| gui_qt_mejorado.py |
|  (Presentación)  |
+--------+---------+
         |
         v
+------------------+
|database_mejorado.py|
| (Lógica y Datos) |
+--------+---------+
         |
         v
+------------------+
|  SQLite Database |
+------------------+
```

## Descripción de Módulos

### 1. main_mejorado.py

Este módulo es el punto de entrada de la aplicación. Su función principal es inicializar la aplicación PyQt5 y mostrar la ventana principal.

**Funcionalidades:**
- Importar los módulos necesarios
- Crear una instancia de QApplication
- Inicializar la ventana principal (ParkingApp)
- Iniciar el bucle de eventos de la aplicación

**Código clave:**
```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingApp()
    window.show()
    sys.exit(app.exec_())
```

### 2. gui_qt_mejorado.py

Este módulo implementa la interfaz gráfica de usuario utilizando PyQt5. Proporciona una interfaz intuitiva con pestañas para las diferentes funcionalidades del sistema.

**Clases principales:**
- `ParkingApp`: Clase principal que hereda de QMainWindow y contiene toda la lógica de la interfaz.

**Métodos clave:**
- `setup_ui()`: Configura la estructura principal de la ventana.
- `crear_tab_ingreso()`: Crea la pestaña para registrar ingresos de vehículos.
- `crear_tab_salida()`: Crea la pestaña para registrar salidas de vehículos.
- `crear_tab_activos()`: Crea la pestaña para visualizar vehículos actualmente en el parqueadero.
- `crear_tab_historial()`: Crea la pestaña para consultar el historial de vehículos.
- `registrar_ingreso_ui()`: Maneja el registro de ingreso desde la interfaz.
- `registrar_salida_ui()`: Maneja el registro de salida desde la interfaz.
- `cargar_vehiculos_activos()`: Actualiza la tabla de vehículos activos.
- `cargar_historial()`: Actualiza la tabla de historial con filtros aplicados.
- `exportar_historial()`: Exporta el historial a CSV o Excel.

**Características destacadas:**
- Validación en tiempo real de entradas
- Feedback visual para el usuario
- Sistema de pestañas para organizar funcionalidades
- Tablas interactivas con acciones integradas
- Filtros avanzados para consultas
- Exportación de datos a diferentes formatos

### 3. database_mejorado.py

Este módulo implementa la lógica de negocio y el acceso a datos del sistema. Gestiona todas las operaciones relacionadas con la base de datos SQLite y los cálculos de tarifas.

**Funciones principales:**
- `conectar()`: Establece conexión con la base de datos y crea las tablas si no existen.
- `obtener_fecha_hora_actual()`: Retorna la fecha y hora actual en formato adecuado.
- `calcular_duracion()`: Calcula la duración en horas entre entrada y salida.
- `obtener_tarifa()`: Obtiene la tarifa aplicable según tipo de vehículo, día y hora.
- `calcular_valor()`: Calcula el valor a pagar según tipo de vehículo y duración.
- `validar_placa()`: Valida el formato de la placa.
- `registrar_ingreso()`: Registra el ingreso de un vehículo al parqueadero.
- `registrar_salida()`: Registra la salida de un vehículo y calcula el valor a pagar.
- `obtener_vehiculos_activos()`: Obtiene la lista de vehículos actualmente en el parqueadero.
- `obtener_historial()`: Obtiene el historial de vehículos con opciones de filtrado.
- `exportar_historial_csv()`: Exporta el historial a un archivo CSV.
- `exportar_historial_excel()`: Exporta el historial a un archivo Excel.
- `migrar_datos_antiguos()`: Migra datos del formato antiguo al nuevo esquema.

**Características destacadas:**
- Sistema flexible de tarifas (por tipo de vehículo, día y hora)
- Cálculo preciso de duración y valor a pagar
- Soporte para fracciones de hora
- Validaciones robustas
- Exportación formateada a diferentes formatos
- Migración de datos para compatibilidad con versiones anteriores

## Flujo del Sistema

El Sistema de Parqueadero Mejorado sigue un flujo de operación claro y estructurado para las principales funcionalidades:

### Registro de Ingreso

1. El operador selecciona la pestaña "Ingreso"
2. Ingresa la placa del vehículo (con validación en tiempo real)
3. Selecciona el tipo de vehículo (Carro o Moto)
4. Opcionalmente, ajusta la fecha y hora (por defecto usa la actual)
5. Hace clic en "Registrar Ingreso"
6. El sistema valida los datos y registra el ingreso en la base de datos
7. Se muestra un mensaje de confirmación con los detalles del ingreso
8. La tabla de vehículos activos se actualiza automáticamente

### Registro de Salida

1. El operador puede registrar la salida de tres formas:
   - Desde la pestaña "Salida"
   - Desde la pestaña "Vehículos Activos" usando el botón de acción
   - Buscando el vehículo por placa
2. El sistema verifica que el vehículo esté en el parqueadero
3. Se calcula la duración de la estancia y el valor a pagar
4. Se solicita confirmación al operador
5. El sistema registra la salida en el historial y elimina el vehículo de activos
6. Se muestra un mensaje con los detalles de la operación y el valor a pagar

### Consulta de Vehículos Activos

1. El operador selecciona la pestaña "Vehículos Activos"
2. El sistema muestra una tabla con todos los vehículos actualmente en el parqueadero
3. Para cada vehículo se muestra: placa, tipo, fecha y hora de entrada
4. El operador puede registrar la salida directamente desde esta vista
5. La tabla se actualiza automáticamente o mediante el botón "Actualizar"

### Consulta de Historial

1. El operador selecciona la pestaña "Historial"
2. Puede aplicar filtros por:
   - Placa (parcial o completa)
   - Tipo de vehículo (Carro, Moto o Todos)
   - Rango de fechas (desde/hasta)
3. Hace clic en "Aplicar Filtros" para actualizar la vista
4. El sistema muestra los registros que cumplen con los criterios
5. El operador puede exportar los datos filtrados a CSV o Excel

### Exportación de Datos

1. Desde la pestaña "Historial", el operador aplica los filtros deseados
2. Selecciona el formato de exportación (CSV o Excel)
3. El sistema solicita la ubicación donde guardar el archivo
4. Se genera el archivo con los datos filtrados y formato adecuado
5. Se muestra un mensaje de confirmación con la ruta del archivo

## Funcionalidades Principales

### 1. Gestión de Ingresos

El sistema permite registrar el ingreso de vehículos al parqueadero con las siguientes características:

- **Validación de placa:** Verifica que la placa tenga un formato válido y no esté ya registrada.
- **Selección de tipo:** Permite especificar si es un carro o una moto.
- **Fecha y hora flexibles:** Permite usar la fecha/hora actual o especificar una diferente.
- **Feedback visual:** Proporciona retroalimentación inmediata sobre la validez de los datos.
- **Confirmación:** Muestra un mensaje con los detalles del ingreso registrado.

### 2. Gestión de Salidas

Para el registro de salidas, el sistema ofrece:

- **Múltiples puntos de acceso:** Permite registrar salidas desde diferentes partes de la interfaz.
- **Verificación de existencia:** Comprueba que el vehículo esté realmente en el parqueadero.
- **Cálculo automático:** Determina la duración de la estancia y el valor a pagar.
- **Confirmación de acción:** Solicita confirmación antes de procesar la salida.
- **Resumen detallado:** Muestra información completa sobre la operación realizada.

### 3. Visualización de Vehículos Activos

La pestaña de vehículos activos proporciona:

- **Vista en tiempo real:** Muestra todos los vehículos actualmente en el parqueadero.
- **Información completa:** Incluye placa, tipo, fecha y hora de entrada.
- **Acciones rápidas:** Permite registrar la salida directamente desde la tabla.
- **Actualización automática:** La vista se actualiza periódicamente y bajo demanda.
- **Contador en pestaña:** Muestra el número de vehículos activos en el título de la pestaña.

### 4. Consulta de Historial

El sistema ofrece capacidades avanzadas de consulta:

- **Filtros múltiples:** Permite filtrar por placa, tipo de vehículo y rango de fechas.
- **Vista detallada:** Muestra información completa de cada registro.
- **Ordenamiento:** Presenta los registros más recientes primero.
- **Formato adecuado:** Aplica formato a valores monetarios y duraciones.
- **Contador de resultados:** Muestra el número de registros encontrados.

### 5. Exportación de Datos

Para análisis y reportes, el sistema permite:

- **Múltiples formatos:** Exportación a CSV y Excel.
- **Filtrado previo:** Exporta solo los datos que cumplen con los filtros aplicados.
- **Formato mejorado:** En Excel, aplica estilos y formatos para mejor presentación.
- **Selección de destino:** Permite elegir la ubicación donde guardar el archivo.
- **Confirmación:** Informa sobre el éxito o fracaso de la operación.

### 6. Cálculo de Tarifas

El sistema implementa un sofisticado mecanismo de cálculo:

- **Tarifas diferenciadas:** Precios diferentes para carros y motos.
- **Soporte para fracciones:** Cobra por intervalos de 15 minutos.
- **Tarifas configurables:** Permite definir tarifas según día y hora.
- **Cálculo preciso:** Considera fechas diferentes para estancias largas.
- **Valores por defecto:** Usa tarifas predefinidas si no hay configuración específica.

## Mejoras Implementadas

El Sistema de Parqueadero Mejorado incorpora numerosas mejoras respecto a versiones anteriores:

### 1. Interfaz Mejorada

- **Validación visual en tiempo real:** Feedback inmediato sobre la validez de los datos.
- **Diseño más intuitivo:** Organización clara de funcionalidades en pestañas.
- **Nueva pestaña de vehículos activos:** Vista dedicada para gestionar vehículos en el parqueadero.
- **Sistema de filtros avanzados:** Capacidades mejoradas de búsqueda y filtrado.
- **Mensajes informativos:** Diálogos claros con información relevante.
- **Botones de acción contextual:** Acciones específicas según el contexto.

### 2. Funcionalidades Avanzadas

- **Soporte para fechas completas:** Manejo adecuado de fechas para estancias largas.
- **Precisión al minuto:** Registro de horas y minutos para cálculos más precisos.
- **Cálculo de tarifas por fracciones:** Cobro por intervalos de 15 minutos.
- **Exportación a Excel con formato:** Archivos Excel con estilos y formatos mejorados.
- **Actualización automática:** Refresco periódico de datos sin intervención del usuario.
- **Acciones rápidas:** Registro de salida directamente desde la tabla de activos.

### 3. Mayor Robustez

- **Validaciones mejoradas:** Verificaciones más completas para evitar errores.
- **Manejo de errores:** Captura y gestión adecuada de excepciones.
- **Confirmación de acciones críticas:** Solicitud de confirmación para operaciones importantes.
- **Respaldo de datos:** Estructura de base de datos mejorada para mayor integridad.
- **Migración de datos:** Soporte para actualizar desde versiones anteriores.
- **Código modular:** Mejor organización del código para facilitar mantenimiento.

## Conclusiones y Recomendaciones

### Conclusiones

El Sistema de Parqueadero Mejorado representa una solución completa y robusta para la gestión de parqueaderos, ofreciendo:

1. **Interfaz intuitiva:** La organización en pestañas y los formularios claros facilitan el uso por parte de los operadores, reduciendo la curva de aprendizaje.

2. **Cálculos precisos:** El sistema de cálculo de tarifas por fracciones de hora asegura cobros justos y transparentes para los clientes.

3. **Gestión eficiente:** La visualización en tiempo real de vehículos activos y las acciones rápidas optimizan la operación diaria del parqueadero.

4. **Capacidades analíticas:** Las funciones de filtrado y exportación permiten analizar datos históricos para toma de decisiones.

5. **Arquitectura sólida:** La separación clara entre interfaz y lógica de negocio facilita el mantenimiento y la extensión del sistema.

### Recomendaciones

Para futuras versiones y mejoras del sistema, se recomienda:

1. **Implementar autenticación de usuarios:** Añadir sistema de login para diferentes operadores con niveles de acceso.

2. **Desarrollar reportes predefinidos:** Crear informes comunes (diarios, semanales, mensuales) con estadísticas relevantes.

3. **Añadir gestión de espacios:** Implementar un mapa visual del parqueadero para asignar ubicaciones específicas.

4. **Integrar impresión de tickets:** Permitir la impresión de comprobantes para clientes.

5. **Desarrollar una versión web:** Crear una versión accesible desde navegadores para mayor flexibilidad.

6. **Implementar respaldo automático:** Añadir funcionalidad para copias de seguridad programadas de la base de datos.

7. **Añadir soporte para abonados:** Implementar sistema de clientes frecuentes con tarifas especiales.

8. **Mejorar la visualización de datos:** Incorporar gráficos y estadísticas en tiempo real.

## Referencias

1. Documentación oficial de PyQt5: [https://www.riverbankcomputing.com/static/Docs/PyQt5/](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

2. Tutorial de PyQt5 en RealPython: [https://realpython.com/python-pyqt-gui-calculator/](https://realpython.com/python-pyqt-gui-calculator/)

3. Documentación oficial de sqlite3 en Python: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)

4. Tutorial de SQLite en Python: [https://www.sqlitetutorial.net/sqlite-python/](https://www.sqlitetutorial.net/sqlite-python/)

5. Curso de PyQt5 en YouTube por Codigofacilito: [https://www.youtube.com/playlist?list=PLpOqH6AE0tNiQ-ofrDlbAUSc1r67r_AWv](https://www.youtube.com/playlist?list=PLpOqH6AE0tNiQ-ofrDlbAUSc1r67r_AWv)


