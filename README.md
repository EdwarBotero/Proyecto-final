# Guía de Usuario - Sistema de Parqueadero Mejorado

## Requisitos del sistema

Para ejecutar el sistema mejorado, necesitarás tener instalado:

1. Python 3.6 o superior
2. PyQt5 (`pip install PyQt5`)
3. Matplotlib (`pip install matplotlib`) - Para gráficos y estadísticas
4. Openpyxl (`pip install openpyxl`) - Para exportación a Excel

## Estructura de archivos

El sistema consta de los siguientes archivos principales:

- `main_mejorado.py`: Punto de entrada de la aplicación
- `gui_qt_mejorado.py`: Interfaz gráfica mejorada
- `database_mejorado.py`: Lógica de negocio y persistencia de datos

## Instalación

1. Asegúrate de tener instaladas todas las dependencias:
   ```
   pip install PyQt5 matplotlib openpyxl
   ```

2. Crea las carpetas necesarias:
   ```
   mkdir -p data
   mkdir -p icons
   ```

3. Ejecuta la aplicación:
   ```
   python main_mejorado.py
   ```

## Inicio de sesión

Al iniciar la aplicación, se mostrará una pantalla de inicio de sesión:

- Usuario por defecto: `admin`
- Contraseña por defecto: `admin123`

## Funcionalidades principales

### Registro de ingreso

1. Selecciona la pestaña "Ingreso"
2. Ingresa la placa del vehículo (formato validado automáticamente)
3. Selecciona el tipo de vehículo (Carro o Moto)
4. Opcionalmente, ajusta la fecha y hora (por defecto usa la actual)
5. Haz clic en "Registrar Ingreso"

### Registro de salida

1. Selecciona la pestaña "Salida"
2. Ingresa la placa del vehículo (se valida automáticamente si existe)
3. Opcionalmente, ajusta la fecha y hora de salida
4. Haz clic en "Registrar Salida"
5. Confirma la acción en el diálogo

### Vehículos activos

1. Selecciona la pestaña "Vehículos Activos"
2. Visualiza todos los vehículos actualmente en el parqueadero
3. Puedes registrar la salida directamente desde esta vista

### Historial

1. Selecciona la pestaña "Historial"
2. Aplica filtros por placa, tipo de vehículo o rango de fechas
3. Haz clic en "Aplicar Filtros" para actualizar la vista
4. Exporta los datos filtrados a CSV o Excel

### Estadísticas

1. Selecciona la pestaña "Estadísticas"
2. Selecciona el rango de fechas para el análisis
3. Visualiza resumen de ingresos, tipos de vehículos y horas pico
4. Observa los gráficos generados automáticamente


## Mejoras implementadas

1. **Interfaz mejorada**:
   - Validación visual en tiempo real
   - Diseño más intuitivo y moderno
   - Nueva pestaña de vehículos activos
   - Sistema de filtros avanzados

2. **Funcionalidades avanzadas**:
   - Soporte para fechas completas y minutos
   - Cálculo de tarifas por fracciones de hora
   - Sistema de usuarios y permisos
   - Estadísticas con gráficos
   - Exportación a Excel

3. **Mayor robustez**:
   - Validaciones mejoradas
   - Respaldo de datos
   - Mejor manejo de errores

### Tutoriales para ententer las implementaciones
    Tutoriales de PyQt5
    Documentación oficial de PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/
    Tutorial de PyQt5 en RealPython: https://realpython.com/python-pyqt-gui-calculator/
    Curso de PyQt5 en YouTube por Codigofacilito: Ofrece tutoriales en español sobre PyQt5

    Tutoriales de SQLite con Python
    Tutorial de SQLite en Python: https://www.sqlitetutorial.net/sqlite-python/
    Documentación oficial de sqlite3 en Python: https://docs.python.org/3/library/sqlite3.html

    Tutoriales de Matplotlib para gráficos
    Documentación oficial de Matplotlib: https://matplotlib.org/stable/tutorials/index.html
    Tutorial de Matplotlib en DataCamp: https://www.datacamp.com/community/tutorials/matplotlib-tutorial-python

    GitHub: Busca proyectos similares con "parking management system pyqt"
    "Building a Parking Management System with PyQt5 and SQLite" en Udemy
    "Python Desktop Applications with PyQt" en Pluralsight
    "Sistema de Gestión con Python y SQLite" en Platzi (en español )
    

