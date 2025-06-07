
# Librerías Principales del Sistema de Parqueadero Mejorado

## Resumen de Librerías

A continuación se presentan las librerías más importantes utilizadas en el proyecto, agrupadas por categoría:

### Interfaz Gráfica (GUI)
- **PyQt5**: Framework completo para desarrollo de interfaces gráficas
  - `QtWidgets`: Componentes de interfaz (ventanas, botones, campos, etc.)
  - `QtCore`: Funcionalidades centrales (fechas, temporizadores, expresiones regulares)
  - `QtGui`: Elementos visuales (validadores, fuentes)

### Base de Datos
- **sqlite3**: Motor de base de datos SQL ligero y embebido

### Manejo de Archivos y Datos
- **csv**: Manejo de archivos CSV
- **openpyxl**: Creación y manipulación de archivos Excel
- **pathlib**: Manejo de rutas de archivos de forma segura

### Fecha y Hora
- **datetime**: Manipulación de fechas y horas

### Utilidades del Sistema
- **sys**: Interacción con el sistema operativo
- **os**: Operaciones del sistema operativo (manejo de directorios)

## Ejemplos Prácticos

A continuación se muestran ejemplos prácticos de cómo estas librerías mejoran y complementan la funcionalidad del proyecto:

### 1. PyQt5 - Interfaz Gráfica Moderna y Responsiva

PyQt5 proporciona una interfaz gráfica moderna, con componentes interactivos y validación en tiempo real.

#### Ejemplo: Validación en Tiempo Real de Placas

```python
# Creación del campo de texto con validación en tiempo real
self.placa_ingreso = QLineEdit()
self.placa_ingreso.setPlaceholderText("Ej: ABC123")

# Validador para formato de placa (3 letras seguidas de 2 o 3 números)
rx = QRegExp("[A-Za-z]{3}[0-9]{2,3}")
validator = QRegExpValidator(rx)
self.placa_ingreso.setValidator(validator)

# Conectamos el evento de cambio de texto para validación visual
self.placa_ingreso.textChanged.connect(self.validar_placa_ingreso)

# Función de validación que cambia el color de fondo según validez
def validar_placa_ingreso(self):
    placa = self.placa_ingreso.text().strip().upper()
    if placa:
        if db.validar_placa(placa):
            self.placa_ingreso.setStyleSheet("background-color: #c8e6c9;")  # Verde claro
        else:
            self.placa_ingreso.setStyleSheet("background-color: #ffcdd2;")  # Rojo claro
    else:
        self.placa_ingreso.setStyleSheet("")
```

**Beneficios:**
- Feedback visual inmediato al usuario
- Prevención de errores antes de enviar datos
- Mejor experiencia de usuario
- Reducción de errores en la entrada de datos

### 2. SQLite3 - Base de Datos Embebida sin Configuración

SQLite3 permite almacenar datos de forma persistente sin necesidad de un servidor de base de datos separado.

#### Ejemplo: Creación Automática de Tablas y Consultas Parametrizadas

```python
def conectar():
    """Establece conexión con la base de datos y crea las tablas si no existen."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # Creamos la tabla de vehículos activos con soporte para fecha y hora completas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            placa TEXT PRIMARY KEY,
            fecha_entrada TEXT,
            hora_entrada INTEGER,
            minuto_entrada INTEGER,
            tipo TEXT CHECK (tipo IN ('Carro', 'Moto')),
            usuario TEXT
        )
    ''')
    
    # Otras tablas...
    
    return conn

def obtener_vehiculos_activos():
    """Obtiene la lista de vehículos actualmente en el parqueadero."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT placa, tipo, fecha_entrada, hora_entrada, minuto_entrada
            FROM vehiculos
            ORDER BY fecha_entrada, hora_entrada, minuto_entrada
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener vehículos activos: {e}")
        return []
```

**Beneficios:**
- Base de datos sin configuración adicional
- Creación automática de tablas si no existen
- Consultas parametrizadas para prevenir inyección SQL
- Transacciones para garantizar integridad de datos

### 3. Datetime - Manejo Preciso de Fechas y Horas

La librería datetime permite un manejo preciso de fechas y horas, esencial para calcular duraciones y tarifas.

#### Ejemplo: Cálculo de Duración entre Entrada y Salida

```python
def calcular_duracion(fecha_entrada, hora_entrada, minuto_entrada, fecha_salida, hora_salida, minuto_salida):
    """Calcula la duración en horas (con decimales para fracciones) entre entrada y salida."""
    entrada = datetime.combine(
        datetime.strptime(fecha_entrada, "%Y-%m-%d").date(),
        time(hour=hora_entrada, minute=minuto_entrada)
    )
    
    salida = datetime.combine(
        datetime.strptime(fecha_salida, "%Y-%m-%d").date(),
        time(hour=hora_salida, minute=minuto_salida)
    )
    
    # Si la salida es anterior a la entrada, asumimos que pasó al menos un día
    if salida < entrada:
        salida = salida.replace(day=salida.day + 1)
    
    # Calculamos la diferencia en horas (con decimales)
    diferencia = salida - entrada
    horas = diferencia.total_seconds() / 3600
    
    return round(horas, 2)
```

**Beneficios:**
- Cálculo preciso de duraciones incluso entre días diferentes
- Soporte para fracciones de hora (minutos)
- Manejo automático de fechas y horas
- Conversión entre diferentes formatos de fecha/hora

### 4. Openpyxl - Exportación a Excel con Formato Profesional

Openpyxl permite exportar datos a Excel con formato profesional, mejorando la presentación de informes.

#### Ejemplo: Exportación de Historial a Excel con Estilos

```python
def exportar_historial_excel(ruta="historial_parqueadero.xlsx", filtro_placa=None, filtro_tipo=None, fecha_inicio=None, fecha_fin=None):
    """Exporta el historial a un archivo Excel con opciones de filtrado."""
    try:
        # Importamos openpyxl solo cuando se necesita
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
        
        historial = obtener_historial(filtro_placa, filtro_tipo, fecha_inicio, fecha_fin)
        if not historial:
            return False, "No hay datos para exportar"
        
        # Creamos un nuevo libro y hoja
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Historial Parqueadero"
        
        # Añadimos encabezados con estilo
        headers = ["Placa", "Tipo", "Fecha Entrada", "Hora Entrada", 
                  "Fecha Salida", "Hora Salida", "Duración (horas)", "Valor"]
        
        # Estilo para encabezados
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        centered = Alignment(horizontal="center")
        
        # Aplicamos encabezados con estilo
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = centered
        
        # Añadimos datos
        for row_num, fila in enumerate(historial, 2):
            placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, \
            fecha_salida, hora_salida, minuto_salida, duracion, valor = fila
            
            # Llenamos las celdas con los datos
            ws.cell(row=row_num, column=1, value=placa)
            ws.cell(row=row_num, column=2, value=tipo)
            ws.cell(row=row_num, column=3, value=fecha_entrada)
            ws.cell(row=row_num, column=4, value=f"{hora_entrada}:{minuto_entrada:02d}")
            ws.cell(row=row_num, column=5, value=fecha_salida if fecha_salida else "N/A")
            ws.cell(row=row_num, column=6, value=f"{hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A")
            ws.cell(row=row_num, column=7, value=duracion)
            
            # Formato para el valor monetario
            cell = ws.cell(row=row_num, column=8, value=valor)
            cell.number_format = "$#,##0"
            cell.alignment = Alignment(horizontal="right")
        
        # Ajustamos anchos de columna
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width
        
        # Guardamos el archivo
        wb.save(ruta)
        return True, f"Historial exportado a '{ruta}'"
    
    except Exception as e:
        print(f"Error al exportar Excel: {e}")
        return False, f"Error al exportar: {e}"
```

**Beneficios:**
- Exportación de datos con formato profesional
- Estilos personalizados para encabezados y datos
- Formato automático para valores monetarios
- Ajuste automático de anchos de columna
- Mejor presentación para análisis y reportes

### 5. QTimer - Actualización Automática de Datos

QTimer permite actualizar automáticamente los datos sin intervención del usuario.

#### Ejemplo: Actualización Periódica de Vehículos Activos

```python
def __init__(self):
    super().__init__()
    
    # Configurar la interfaz principal
    self.setup_ui()
    
    # Iniciar temporizador para actualización automática
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.actualizar_datos)
    self.timer.start(60000)  # Actualizar cada minuto (60000 ms)

def actualizar_datos(self):
    """Actualiza todos los datos dinámicos de la interfaz."""
    self.cargar_vehiculos_activos()
    self.cargar_historial()
```

**Beneficios:**
- Actualización automática de datos sin intervención del usuario
- Información siempre actualizada
- Mejor experiencia de usuario
- Reducción de errores por datos desactualizados

### 6. Pathlib - Manejo Seguro de Rutas de Archivos

Pathlib proporciona una forma orientada a objetos y segura de manejar rutas de archivos.

#### Ejemplo: Creación de Directorios y Manejo de Rutas

```python
from pathlib import Path

# Ruta donde tenemos almacenada la BD
DB_PATH = Path("data/parking.db")

def conectar():
    """Establece conexión con la base de datos y crea las tablas si no existen."""
    # Creamos el directorio padre si no existe
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # Resto del código...
```

**Beneficios:**
- Manejo de rutas compatible con múltiples sistemas operativos
- Creación automática de directorios si no existen
- Operaciones de ruta más seguras y legibles
- Mejor mantenibilidad del código

### 7. QMessageBox - Diálogos Interactivos con el Usuario

QMessageBox permite mostrar mensajes y solicitar confirmación al usuario de forma elegante.

#### Ejemplo: Confirmación de Salida de Vehículo

```python
def registrar_salida_rapida(self, placa):
    """Registra la salida de un vehículo directamente desde la tabla de activos."""
    # Mostramos un diálogo de confirmación
    reply = QMessageBox.question(
        self, 
        "Confirmar Salida", 
        f"¿Desea registrar la salida del vehículo con placa {placa}?",
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No  # Opción por defecto: No
    )
    
    # Si el usuario confirma, procedemos con el registro
    if reply == QMessageBox.Yes:
        # Usar fecha y hora actual
        fecha_actual, hora_actual, minuto_actual = db.obtener_fecha_hora_actual()
        
        # Registramos la salida
        success, result = db.registrar_salida(
            placa, 
            fecha_actual, 
            hora_actual, 
            minuto_actual, 
            "sistema"  # Usuario que registra
        )
        
        # Mostramos el resultado
        if success:
            QMessageBox.information(
                self, 
                "Salida Registrada", 
                f"Salida registrada correctamente:\n\n"
                f"Placa: {placa}\n"
                f"Duración: {result['duracion']} horas\n"
                f"Valor a pagar: ${result['valor']:,.0f}"
            )
            # Actualizamos las tablas
            self.cargar_vehiculos_activos()
            self.cargar_historial()
        else:
            QMessageBox.critical(self, "Error", result)
```

**Beneficios:**
- Diálogos interactivos con el usuario
- Confirmación de acciones importantes
- Presentación clara de resultados y errores
- Mejor experiencia de usuario
- Prevención de acciones no deseadas

## Conclusión

Las librerías utilizadas en el Sistema de Parqueadero Mejorado proporcionan una base sólida para crear una aplicación robusta, con una interfaz moderna y funcionalidades avanzadas. Cada librería aporta características específicas que mejoran diferentes aspectos del sistema:

- **PyQt5**: Interfaz gráfica moderna, responsiva y con validación en tiempo real
- **SQLite3**: Almacenamiento persistente de datos sin necesidad de configuración adicional
- **Datetime**: Manejo preciso de fechas y horas para cálculos de duración y tarifas
- **Openpyxl**: Exportación de datos con formato profesional para análisis y reportes
- **QTimer**: Actualización automática de datos para mantener la información al día
- **Pathlib**: Manejo seguro de rutas de archivos compatible con múltiples sistemas operativos
- **QMessageBox**: Diálogos interactivos para mejorar la comunicación con el usuario

La combinación de estas librerías permite crear un sistema completo, fácil de usar y mantener, que cumple con todos los requisitos de un sistema de gestión de parqueadero moderno.
