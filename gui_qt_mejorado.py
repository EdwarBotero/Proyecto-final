"""
Sistema de Parqueadero Mejorado - Módulo de Interfaz Gráfica
===========================================================

Este módulo implementa la interfaz gráfica de usuario (GUI) del sistema de parqueadero
utilizando PyQt5. Proporciona una interfaz moderna e intuitiva con múltiples pestañas
para gestionar ingresos, salidas, vehículos activos e historial.

"""

# Importación de módulos de PyQt5 para la interfaz gráfica
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QFileDialog, QDateEdit, QTimeEdit, QGroupBox,
                            QFormLayout, QCheckBox, QStatusBar)
from PyQt5.QtCore import Qt, QDate, QTime, QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator, QFont

# Importación del módulo de base de datos
import database_mejorado as db

# Importación de módulos estándar
import sys
import os
from datetime import datetime

# Definimos la ruta para los iconos
ICON_PATH = "icons"

class ParkingApp(QMainWindow):
    """
    Clase principal de la aplicación de parqueadero.
    
    Esta clase implementa la ventana principal de la aplicación y gestiona
    todas las interacciones con el usuario a través de la interfaz gráfica.
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal y configura la interfaz.
        """
        # Llamamos al constructor de la clase padre (QMainWindow)
        super().__init__()
        
        # Configurar la interfaz principal
        self.setup_ui()
        
        # Iniciar temporizador para actualización automática de datos
        # Esto permite que la información se actualice periódicamente sin intervención del usuario
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(60000)  # Actualizar cada minuto (60000 ms)
        
        # Crear directorio para iconos si no existe
        # Esto asegura que la aplicación pueda guardar y acceder a los iconos necesarios
        if not os.path.exists(ICON_PATH):
            os.makedirs(ICON_PATH)
    
    def setup_ui(self):
        """
        Configura todos los elementos de la interfaz de usuario.
        
        Esta función crea la estructura principal de la ventana, incluyendo:
        - Título y dimensiones de la ventana
        - Barra de estado
        - Sistema de pestañas
        - Contenido de cada pestaña
        """
        # Configuración básica de la ventana
        self.setWindowTitle("Sistema de Parqueadero")
        self.setGeometry(100, 100, 1000, 700)  # Posición (x, y) y tamaño (ancho, alto)
        
        # Crear barra de estado en la parte inferior de la ventana
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Sistema de Parqueadero")
        
        # Widget central y layout principal
        # En PyQt, cada ventana necesita un widget central que contenga todos los elementos
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Crear el sistema de pestañas
        # QTabWidget permite organizar la interfaz en pestañas para mejor usabilidad
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Crear las pestañas individuales
        self.crear_tab_ingreso()    # Pestaña para registrar ingresos
        self.crear_tab_salida()     # Pestaña para registrar salidas
        self.crear_tab_activos()    # Pestaña para ver vehículos actualmente en el parqueadero
        self.crear_tab_historial()  # Pestaña para consultar el historial
        
        # Cargar datos iniciales
        self.actualizar_datos()
    
    def actualizar_datos(self):
        """
        Actualiza todos los datos dinámicos de la interfaz.
        
        Esta función se llama periódicamente para mantener la información
        actualizada en todas las pestañas.
        """
        # Actualizamos la lista de vehículos activos
        self.cargar_vehiculos_activos()
        
        # Actualizamos el historial
        self.cargar_historial()
    
    def crear_tab_ingreso(self):
        """
        Crea la pestaña de registro de ingreso de vehículos.
        
        Esta pestaña permite al usuario registrar la entrada de un vehículo
        al parqueadero, especificando placa, tipo y fecha/hora.
        """
        # Creamos un widget para la pestaña y lo añadimos al sistema de pestañas
        tab = QWidget()
        self.tabs.addTab(tab, "Ingreso")
        layout = QVBoxLayout(tab)
        
        # Título de la pestaña
        titulo = QLabel("Registro de Ingreso de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)  # Centrar el texto
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # Tamaño de fuente
        titulo_font.setBold(True)     # Negrita
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Formulario en un GroupBox para mejor organización visual
        form_group = QGroupBox("Datos del Vehículo")
        form_layout = QFormLayout()
        
        # Campo para la placa
        self.placa_ingreso = QLineEdit()
        self.placa_ingreso.setPlaceholderText("Ej: ABC123")  # Texto de ayuda
        
        # Validador para formato de placa (3 letras seguidas de 2 o 3 números)
        rx = QRegExp("[A-Za-z]{3}[0-9]{2,3}")
        validator = QRegExpValidator(rx)
        self.placa_ingreso.setValidator(validator)
        
        # Conectamos el evento de cambio de texto para validación en tiempo real
        self.placa_ingreso.textChanged.connect(self.validar_placa_ingreso)
        form_layout.addRow("Placa:", self.placa_ingreso)
        
        # Selector de tipo de vehículo
        self.tipo_vehiculo = QComboBox()
        self.tipo_vehiculo.addItems(["Carro", "Moto"])
        form_layout.addRow("Tipo:", self.tipo_vehiculo)
        
        # Campos para fecha y hora
        fecha_hora_layout = QHBoxLayout()
        
        # Selector de fecha
        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setCalendarPopup(True)  # Permite mostrar un calendario al hacer clic
        self.fecha_ingreso.setDate(QDate.currentDate())  # Fecha actual por defecto
        fecha_hora_layout.addWidget(QLabel("Fecha:"))
        fecha_hora_layout.addWidget(self.fecha_ingreso)
        
        # Selector de hora
        self.hora_ingreso = QTimeEdit()
        self.hora_ingreso.setTime(QTime.currentTime())  # Hora actual por defecto
        fecha_hora_layout.addWidget(QLabel("Hora:"))
        fecha_hora_layout.addWidget(self.hora_ingreso)
        
        form_layout.addRow("Fecha y Hora:", fecha_hora_layout)
        
        # Checkbox para usar fecha y hora actual
        self.usar_hora_actual = QCheckBox("Usar fecha y hora actual")
        self.usar_hora_actual.setChecked(True)  # Activado por defecto
        self.usar_hora_actual.stateChanged.connect(self.toggle_fecha_hora_ingreso)
        form_layout.addRow("", self.usar_hora_actual)
        
        # Aplicamos el layout al grupo
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botón de registrar ingreso
        self.btn_registrar_ingreso = QPushButton("Registrar Ingreso")
        self.btn_registrar_ingreso.setMinimumHeight(40)  # Altura mínima para mejor visibilidad
        self.btn_registrar_ingreso.clicked.connect(self.registrar_ingreso_ui)
        layout.addWidget(self.btn_registrar_ingreso)
        
        # Deshabilitar campos de fecha y hora si se usa la actual
        self.toggle_fecha_hora_ingreso()
        
        # Añadimos un espacio flexible al final para mejor distribución de elementos
        layout.addStretch()
    
    def toggle_fecha_hora_ingreso(self):
        """
        Habilita o deshabilita los campos de fecha y hora según el checkbox.
        
        Si el checkbox "Usar fecha y hora actual" está marcado, los campos
        de fecha y hora se deshabilitan y se establecen a la fecha/hora actual.
        """
        # Obtenemos el estado del checkbox
        usar_actual = self.usar_hora_actual.isChecked()
        
        # Habilitamos o deshabilitamos los campos según el estado
        self.fecha_ingreso.setEnabled(not usar_actual)
        self.hora_ingreso.setEnabled(not usar_actual)
        
        # Si se usa la fecha/hora actual, actualizamos los campos
        if usar_actual:
            self.fecha_ingreso.setDate(QDate.currentDate())
            self.hora_ingreso.setTime(QTime.currentTime())
    
    def validar_placa_ingreso(self):
        """
        Valida el formato de la placa en tiempo real.
        
        Esta función cambia el color de fondo del campo de placa según
        si el formato es válido (verde) o inválido (rojo).
        """
        # Obtenemos el texto de la placa, eliminamos espacios y convertimos a mayúsculas
        placa = self.placa_ingreso.text().strip().upper()
        
        if placa:
            # Validamos el formato usando la función del módulo de base de datos
            if db.validar_placa(placa):
                self.placa_ingreso.setStyleSheet("background-color: #c8e6c9;")  # Verde claro
            else:
                self.placa_ingreso.setStyleSheet("background-color: #ffcdd2;")  # Rojo claro
        else:
            # Si el campo está vacío, restauramos el estilo por defecto
            self.placa_ingreso.setStyleSheet("")
    
    def crear_tab_salida(self):
        """
        Crea la pestaña de registro de salida de vehículos.
        
        Esta pestaña permite al usuario registrar la salida de un vehículo
        del parqueadero, especificando la placa y opcionalmente la fecha/hora.
        """
        # Creamos un widget para la pestaña y lo añadimos al sistema de pestañas
        tab = QWidget()
        self.tabs.addTab(tab, "Salida")
        layout = QVBoxLayout(tab)
        
        # Título de la pestaña
        titulo = QLabel("Registro de Salida de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)  # Centrar el texto
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # Tamaño de fuente
        titulo_font.setBold(True)     # Negrita
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Formulario en un GroupBox para mejor organización visual
        form_group = QGroupBox("Datos de Salida")
        form_layout = QFormLayout()
        
        # Campo para la placa
        self.placa_salida = QLineEdit()
        self.placa_salida.setPlaceholderText("Ej: ABC123")  # Texto de ayuda
        
        # Conectamos el evento de cambio de texto para validación en tiempo real
        self.placa_salida.textChanged.connect(self.validar_placa_salida)
        form_layout.addRow("Placa:", self.placa_salida)
        
        # Campos para fecha y hora
        fecha_hora_layout = QHBoxLayout()
        
        # Selector de fecha
        self.fecha_salida = QDateEdit()
        self.fecha_salida.setCalendarPopup(True)  # Permite mostrar un calendario al hacer clic
        self.fecha_salida.setDate(QDate.currentDate())  # Fecha actual por defecto
        fecha_hora_layout.addWidget(QLabel("Fecha:"))
        fecha_hora_layout.addWidget(self.fecha_salida)
        
        # Selector de hora
        self.hora_salida = QTimeEdit()
        self.hora_salida.setTime(QTime.currentTime())  # Hora actual por defecto
        fecha_hora_layout.addWidget(QLabel("Hora:"))
        fecha_hora_layout.addWidget(self.hora_salida)
        
        form_layout.addRow("Fecha y Hora:", fecha_hora_layout)
        
        # Checkbox para usar fecha y hora actual
        self.usar_hora_actual_salida = QCheckBox("Usar fecha y hora actual")
        self.usar_hora_actual_salida.setChecked(True)  # Activado por defecto
        self.usar_hora_actual_salida.stateChanged.connect(self.toggle_fecha_hora_salida)
        form_layout.addRow("", self.usar_hora_actual_salida)
        
        # Aplicamos el layout al grupo
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botón de registrar salida
        self.btn_registrar_salida = QPushButton("Registrar Salida")
        self.btn_registrar_salida.setMinimumHeight(40)  # Altura mínima para mejor visibilidad
        self.btn_registrar_salida.clicked.connect(self.registrar_salida_ui)
        layout.addWidget(self.btn_registrar_salida)
        
        # Deshabilitar campos de fecha y hora si se usa la actual
        self.toggle_fecha_hora_salida()
        
        # Añadimos un espacio flexible al final para mejor distribución de elementos
        layout.addStretch()
    
    def toggle_fecha_hora_salida(self):
        """
        Habilita o deshabilita los campos de fecha y hora de salida según el checkbox.
        
        Si el checkbox "Usar fecha y hora actual" está marcado, los campos
        de fecha y hora se deshabilitan y se establecen a la fecha/hora actual.
        """
        # Obtenemos el estado del checkbox
        usar_actual = self.usar_hora_actual_salida.isChecked()
        
        # Habilitamos o deshabilitamos los campos según el estado
        self.fecha_salida.setEnabled(not usar_actual)
        self.hora_salida.setEnabled(not usar_actual)
        
        # Si se usa la fecha/hora actual, actualizamos los campos
        if usar_actual:
            self.fecha_salida.setDate(QDate.currentDate())
            self.hora_salida.setTime(QTime.currentTime())
    
    def validar_placa_salida(self):
        """
        Valida si la placa existe en vehículos activos.
        
        Esta función cambia el color de fondo del campo de placa según
        si la placa existe en el parqueadero (verde) o no (rojo).
        """
        # Obtenemos el texto de la placa, eliminamos espacios y convertimos a mayúsculas
        placa = self.placa_salida.text().strip().upper()
        
        if placa:
            # Verificar si la placa está en vehículos activos
            vehiculos = db.obtener_vehiculos_activos()
            placas_activas = [v[0] for v in vehiculos]  # Extraemos solo las placas
            
            if placa in placas_activas:
                self.placa_salida.setStyleSheet("background-color: #c8e6c9;")  # Verde claro
            else:
                self.placa_salida.setStyleSheet("background-color: #ffcdd2;")  # Rojo claro
        else:
            # Si el campo está vacío, restauramos el estilo por defecto
            self.placa_salida.setStyleSheet("")
    
    def crear_tab_activos(self):
        """
        Crea la pestaña de vehículos activos.
        
        Esta pestaña muestra una tabla con todos los vehículos que actualmente
        están en el parqueadero, permitiendo registrar su salida directamente.
        """
        # Creamos un widget para la pestaña y lo añadimos al sistema de pestañas
        tab = QWidget()
        self.tabs.addTab(tab, "Vehículos Activos")
        layout = QVBoxLayout(tab)
        
        # Título de la pestaña
        titulo = QLabel("Vehículos Actualmente en el Parqueadero")
        titulo.setAlignment(Qt.AlignCenter)  # Centrar el texto
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # Tamaño de fuente
        titulo_font.setBold(True)     # Negrita
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Tabla de vehículos activos
        self.tabla_activos = QTableWidget()
        self.tabla_activos.setColumnCount(5)  # 5 columnas
        self.tabla_activos.setHorizontalHeaderLabels([
            "Placa", "Tipo", "Fecha Entrada", "Hora Entrada", "Acciones"
        ])
        
        # Configuración de la tabla
        self.tabla_activos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Ajustar ancho de columnas
        self.tabla_activos.setEditTriggers(QTableWidget.NoEditTriggers)  # No permitir edición directa
        self.tabla_activos.setSelectionBehavior(QTableWidget.SelectRows)  # Seleccionar filas completas
        layout.addWidget(self.tabla_activos)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        # Botón para actualizar la lista de vehículos activos
        self.btn_actualizar_activos = QPushButton("Actualizar")
        self.btn_actualizar_activos.clicked.connect(self.cargar_vehiculos_activos)
        btn_layout.addWidget(self.btn_actualizar_activos)
        
        layout.addLayout(btn_layout)
    
    def cargar_vehiculos_activos(self):
        """
        Carga la lista de vehículos actualmente en el parqueadero.
        
        Esta función actualiza la tabla de vehículos activos con los datos
        más recientes de la base de datos.
        """
        # Limpiamos la tabla actual
        self.tabla_activos.setRowCount(0)
        
        # Obtenemos la lista de vehículos activos
        vehiculos = db.obtener_vehiculos_activos()
        
        # Añadimos cada vehículo a la tabla
        for fila in vehiculos:
            # Añadimos una nueva fila a la tabla
            row_position = self.tabla_activos.rowCount()
            self.tabla_activos.insertRow(row_position)
            
            # Extraemos los datos del vehículo
            placa, tipo, fecha_entrada, hora_entrada, minuto_entrada = fila
            
            # Añadimos los datos a las celdas correspondientes
            self.tabla_activos.setItem(row_position, 0, QTableWidgetItem(placa))
            self.tabla_activos.setItem(row_position, 1, QTableWidgetItem(tipo))
            self.tabla_activos.setItem(row_position, 2, QTableWidgetItem(fecha_entrada))
            self.tabla_activos.setItem(row_position, 3, QTableWidgetItem(f"{hora_entrada}:{minuto_entrada:02d}"))
            
            # Botón de registrar salida para cada vehículo
            btn_salida = QPushButton("Registrar Salida")
            # Usamos lambda con un parámetro adicional para capturar la placa específica
            btn_salida.clicked.connect(lambda checked, p=placa: self.registrar_salida_rapida(p))
            self.tabla_activos.setCellWidget(row_position, 4, btn_salida)
        
        # Actualizar contador en la pestaña
        self.tabs.setTabText(2, f"Vehículos Activos ({self.tabla_activos.rowCount()})")
    
    def registrar_salida_rapida(self, placa):
        """
        Registra la salida de un vehículo directamente desde la tabla de activos.
        
        Esta función permite registrar la salida con un solo clic desde la
        pestaña de vehículos activos, usando la fecha y hora actual.
        
        Args:
            placa (str): Placa del vehículo a registrar salida
        """
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
    
    def crear_tab_historial(self):
        """
        Crea la pestaña de historial de vehículos.
        
        Esta pestaña muestra una tabla con el historial de todos los vehículos
        que han usado el parqueadero, con opciones de filtrado y exportación.
        """
        # Creamos un widget para la pestaña y lo añadimos al sistema de pestañas
        tab = QWidget()
        self.tabs.addTab(tab, "Historial")
        layout = QVBoxLayout(tab)
        
        # Título de la pestaña
        titulo = QLabel("Historial de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)  # Centrar el texto
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # Tamaño de fuente
        titulo_font.setBold(True)     # Negrita
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Filtros en un GroupBox para mejor organización visual
        filtros_group = QGroupBox("Filtros")
        filtros_layout = QVBoxLayout()
        
        # Filtro por placa
        filtro_placa_layout = QHBoxLayout()
        filtro_placa_layout.addWidget(QLabel("Placa:"))
        self.filtro_placa = QLineEdit()
        self.filtro_placa.setPlaceholderText("Filtrar por placa")
        filtro_placa_layout.addWidget(self.filtro_placa)
        filtros_layout.addLayout(filtro_placa_layout)
        
        # Filtro por tipo
        filtro_tipo_layout = QHBoxLayout()
        filtro_tipo_layout.addWidget(QLabel("Tipo:"))
        self.filtro_tipo = QComboBox()
        self.filtro_tipo.addItems(["Todos", "Carro", "Moto"])
        filtro_tipo_layout.addWidget(self.filtro_tipo)
        filtros_layout.addLayout(filtro_tipo_layout)
        
        # Filtro por fecha
        filtro_fecha_layout = QHBoxLayout()
        
        # Fecha de inicio
        filtro_fecha_layout.addWidget(QLabel("Desde:"))
        self.filtro_fecha_inicio = QDateEdit()
        self.filtro_fecha_inicio.setCalendarPopup(True)
        # Por defecto, mostramos los últimos 30 días
        self.filtro_fecha_inicio.setDate(QDate.currentDate().addDays(-30))
        filtro_fecha_layout.addWidget(self.filtro_fecha_inicio)
        
        # Fecha de fin
        filtro_fecha_layout.addWidget(QLabel("Hasta:"))
        self.filtro_fecha_fin = QDateEdit()
        self.filtro_fecha_fin.setCalendarPopup(True)
        self.filtro_fecha_fin.setDate(QDate.currentDate())
        filtro_fecha_layout.addWidget(self.filtro_fecha_fin)
        
        filtros_layout.addLayout(filtro_fecha_layout)
        
        # Botones de filtro y exportación
        filtro_botones_layout = QHBoxLayout()
        
        # Botón para aplicar filtros
        self.btn_aplicar_filtros = QPushButton("Aplicar Filtros")
        self.btn_aplicar_filtros.clicked.connect(self.cargar_historial)
        filtro_botones_layout.addWidget(self.btn_aplicar_filtros)
        
        # Botón para exportar a CSV
        self.btn_exportar_csv = QPushButton("Exportar CSV")
        self.btn_exportar_csv.clicked.connect(lambda: self.exportar_historial("csv"))
        filtro_botones_layout.addWidget(self.btn_exportar_csv)
        
        # Botón para exportar a Excel
        self.btn_exportar_excel = QPushButton("Exportar Excel")
        self.btn_exportar_excel.clicked.connect(lambda: self.exportar_historial("excel"))
        filtro_botones_layout.addWidget(self.btn_exportar_excel)
        
        filtros_layout.addLayout(filtro_botones_layout)
        
        # Aplicamos el layout al grupo de filtros
        filtros_group.setLayout(filtros_layout)
        layout.addWidget(filtros_group)
        
        # Tabla de historial
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(8)  # 8 columnas
        self.tabla_historial.setHorizontalHeaderLabels([
            "Placa", "Tipo", "Fecha Entrada", "Hora Entrada", 
            "Fecha Salida", "Hora Salida", "Duración (h)", "Valor"
        ])
        
        # Configuración de la tabla
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Ajustar ancho de columnas
        self.tabla_historial.setEditTriggers(QTableWidget.NoEditTriggers)  # No permitir edición directa
        self.tabla_historial.setSelectionBehavior(QTableWidget.SelectRows)  # Seleccionar filas completas
        layout.addWidget(self.tabla_historial)
    
    def cargar_historial(self):
        """
        Carga el historial de vehículos con los filtros aplicados.
        
        Esta función actualiza la tabla de historial con los datos filtrados
        según los criterios especificados por el usuario.
        """
        # Limpiamos la tabla actual
        self.tabla_historial.setRowCount(0)
        
        # Obtener valores de filtros
        # Verificamos que los widgets existan antes de acceder a ellos
        filtro_placa = self.filtro_placa.text().strip() if hasattr(self, 'filtro_placa') else None
        
        filtro_tipo = None
        if hasattr(self, 'filtro_tipo') and self.filtro_tipo.currentText() != "Todos":
            filtro_tipo = self.filtro_tipo.currentText()
        
        fecha_inicio = None
        if hasattr(self, 'filtro_fecha_inicio'):
            fecha_inicio = self.filtro_fecha_inicio.date().toString("yyyy-MM-dd")
        
        fecha_fin = None
        if hasattr(self, 'filtro_fecha_fin'):
            fecha_fin = self.filtro_fecha_fin.date().toString("yyyy-MM-dd")
        
        # Obtener historial filtrado
        historial = db.obtener_historial(filtro_placa, filtro_tipo, fecha_inicio, fecha_fin)
        
        # Añadimos cada registro a la tabla
        for fila in historial:
            # Añadimos una nueva fila a la tabla
            row_position = self.tabla_historial.rowCount()
            self.tabla_historial.insertRow(row_position)
            
            # Extraemos los datos del registro
            placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, \
            fecha_salida, hora_salida, minuto_salida, duracion, valor = fila
            
            # Añadimos los datos a las celdas correspondientes
            self.tabla_historial.setItem(row_position, 0, QTableWidgetItem(placa))
            self.tabla_historial.setItem(row_position, 1, QTableWidgetItem(tipo))
            self.tabla_historial.setItem(row_position, 2, QTableWidgetItem(fecha_entrada))
            self.tabla_historial.setItem(row_position, 3, QTableWidgetItem(f"{hora_entrada}:{minuto_entrada:02d}"))
            self.tabla_historial.setItem(row_position, 4, QTableWidgetItem(fecha_salida if fecha_salida else "N/A"))
            self.tabla_historial.setItem(row_position, 5, QTableWidgetItem(f"{hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A"))
            self.tabla_historial.setItem(row_position, 6, QTableWidgetItem(f"{duracion:.2f}"))
            
            # Formato para el valor (alineado a la derecha)
            valor_item = QTableWidgetItem(f"${valor:,.0f}")
            valor_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla_historial.setItem(row_position, 7, valor_item)
        
        # Actualizar contador en la pestaña
        self.tabs.setTabText(3, f"Historial ({self.tabla_historial.rowCount()})")
    
    def exportar_historial(self, formato):
        """
        Exporta el historial en el formato especificado.
        
        Esta función permite exportar el historial filtrado a un archivo
        CSV o Excel, según la elección del usuario.
        
        Args:
            formato (str): Formato de exportación ('csv' o 'excel')
        """
        # Obtener valores de filtros
        filtro_placa = self.filtro_placa.text().strip()
        
        filtro_tipo = None
        if self.filtro_tipo.currentText() != "Todos":
            filtro_tipo = self.filtro_tipo.currentText()
        
        fecha_inicio = self.filtro_fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.filtro_fecha_fin.date().toString("yyyy-MM-dd")
        
        # Exportar según el formato seleccionado
        if formato == "csv":
            # Mostrar diálogo para seleccionar ubicación del archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar CSV", "historial_parqueadero.csv", "CSV Files (*.csv)"
            )
            
            if file_path:
                # Llamar a la función de exportación
                success, message = db.exportar_historial_csv(
                    file_path, filtro_placa, filtro_tipo, fecha_inicio, fecha_fin
                )
                
                # Mostrar resultado
                if success:
                    QMessageBox.information(self, "Éxito", message)
                else:
                    QMessageBox.critical(self, "Error", message)
        
        elif formato == "excel":
            # Mostrar diálogo para seleccionar ubicación del archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Excel", "historial_parqueadero.xlsx", "Excel Files (*.xlsx)"
            )
            
            if file_path:
                # Llamar a la función de exportación
                success, message = db.exportar_historial_excel(
                    file_path, filtro_placa, filtro_tipo, fecha_inicio, fecha_fin
                )
                
                # Mostrar resultado
                if success:
                    QMessageBox.information(self, "Éxito", message)
                else:
                    QMessageBox.critical(self, "Error", message)
    
    def registrar_ingreso_ui(self):
        """
        Registra el ingreso de un vehículo desde la interfaz.
        
        Esta función recopila los datos ingresados por el usuario en la
        pestaña de ingreso y llama a la función correspondiente en el
        módulo de base de datos.
        """
        # Obtenemos y validamos la placa
        placa = self.placa_ingreso.text().strip().upper()
        tipo = self.tipo_vehiculo.currentText()
        
        # Validar placa
        if not db.validar_placa(placa):
            QMessageBox.critical(self, "Error", "Formato de placa inválido. Verifique.")
            return
        
        # Obtener fecha y hora
        if self.usar_hora_actual.isChecked():
            # Usar fecha y hora actual
            fecha, hora, minuto = db.obtener_fecha_hora_actual()
        else:
            # Usar fecha y hora seleccionadas por el usuario
            fecha = self.fecha_ingreso.date().toString("yyyy-MM-dd")
            hora = self.hora_ingreso.time().hour()
            minuto = self.hora_ingreso.time().minute()
        
        # Registrar ingreso
        success, message = db.registrar_ingreso(placa, fecha, hora, minuto, tipo, "sistema")
        
        # Mostrar resultado
        if success:
            QMessageBox.information(
                self, 
                "Ingreso Registrado", 
                f"Ingreso registrado correctamente:\n\n"
                f"Placa: {placa}\n"
                f"Tipo: {tipo}\n"
                f"Fecha y Hora: {fecha} {hora}:{minuto:02d}"
            )
            # Limpiar campo de placa
            self.placa_ingreso.clear()
            # Actualizar tabla de vehículos activos
            self.cargar_vehiculos_activos()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def registrar_salida_ui(self):
        """
        Registra la salida de un vehículo desde la interfaz.
        
        Esta función recopila los datos ingresados por el usuario en la
        pestaña de salida y llama a la función correspondiente en el
        módulo de base de datos.
        """
        # Obtenemos y validamos la placa
        placa = self.placa_salida.text().strip().upper()
        
        if not placa:
            QMessageBox.critical(self, "Error", "Debe ingresar una placa.")
            return
        
        # Obtener fecha y hora
        if self.usar_hora_actual_salida.isChecked():
            # Usar fecha y hora actual
            fecha, hora, minuto = db.obtener_fecha_hora_actual()
        else:
            # Usar fecha y hora seleccionadas por el usuario
            fecha = self.fecha_salida.date().toString("yyyy-MM-dd")
            hora = self.hora_salida.time().hour()
            minuto = self.hora_salida.time().minute()
        
        # Confirmar acción
        reply = QMessageBox.question(
            self, 
            "Confirmar Salida", 
            f"¿Desea registrar la salida del vehículo con placa {placa}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No  # Opción por defecto: No
        )
        
        # Si el usuario confirma, procedemos con el registro
        if reply == QMessageBox.Yes:
            # Registrar salida
            success, result = db.registrar_salida(placa, fecha, hora, minuto, "sistema")
            
            # Mostrar resultado
            if success:
                QMessageBox.information(
                    self, 
                    "Salida Registrada", 
                    f"Salida registrada correctamente:\n\n"
                    f"Placa: {placa}\n"
                    f"Duración: {result['duracion']} horas\n"
                    f"Valor a pagar: ${result['valor']:,.0f}"
                )
                # Limpiar campo de placa
                self.placa_salida.clear()
                # Actualizar tablas
                self.cargar_vehiculos_activos()
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", result)


