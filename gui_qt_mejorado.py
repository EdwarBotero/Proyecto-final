from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QFileDialog, QDateEdit, QTimeEdit, QGroupBox,
                            QFormLayout, QCheckBox, QStatusBar)
from PyQt5.QtCore import Qt, QDate, QTime, QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator, QFont
import database_mejorado as db
import sys
import os
from datetime import datetime

# Definimos la ruta para los iconos
ICON_PATH = "icons"

class ParkingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar la interfaz principal
        self.setup_ui()
        
        # Iniciar temporizador para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(60000)  # Actualizar cada minuto
        
        # Crear directorio para iconos si no existe
        if not os.path.exists(ICON_PATH):
            os.makedirs(ICON_PATH)
    
    def setup_ui(self):
        self.setWindowTitle("Sistema de Parqueadero")
        self.setGeometry(100, 100, 1000, 700)
        
        # Crear barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Sistema de Parqueadero")
        
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Crear el sistema de pestañas
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Crear las pestañas
        self.crear_tab_ingreso()
        self.crear_tab_salida()
        self.crear_tab_activos()
        self.crear_tab_historial()
        
        # Cargar datos iniciales
        self.actualizar_datos()
    
    def actualizar_datos(self):
        """Actualiza todos los datos dinámicos de la interfaz."""
        self.cargar_vehiculos_activos()
        self.cargar_historial()
    
    def crear_tab_ingreso(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Ingreso")
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Registro de Ingreso de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Formulario en un GroupBox
        form_group = QGroupBox("Datos del Vehículo")
        form_layout = QFormLayout()
        
        # Placa
        self.placa_ingreso = QLineEdit()
        self.placa_ingreso.setPlaceholderText("Ej: ABC123")
        # Validador para formato de placa
        rx = QRegExp("[A-Za-z]{3}[0-9]{2,3}")
        validator = QRegExpValidator(rx)
        self.placa_ingreso.setValidator(validator)
        self.placa_ingreso.textChanged.connect(self.validar_placa_ingreso)
        form_layout.addRow("Placa:", self.placa_ingreso)
        
        # Tipo de vehículo
        self.tipo_vehiculo = QComboBox()
        self.tipo_vehiculo.addItems(["Carro", "Moto"])
        form_layout.addRow("Tipo:", self.tipo_vehiculo)
        
        # Fecha y hora
        fecha_hora_layout = QHBoxLayout()
        
        # Fecha
        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setCalendarPopup(True)
        self.fecha_ingreso.setDate(QDate.currentDate())
        fecha_hora_layout.addWidget(QLabel("Fecha:"))
        fecha_hora_layout.addWidget(self.fecha_ingreso)
        
        # Hora
        self.hora_ingreso = QTimeEdit()
        self.hora_ingreso.setTime(QTime.currentTime())
        fecha_hora_layout.addWidget(QLabel("Hora:"))
        fecha_hora_layout.addWidget(self.hora_ingreso)
        
        form_layout.addRow("Fecha y Hora:", fecha_hora_layout)
        
        # Checkbox para usar fecha y hora actual
        self.usar_hora_actual = QCheckBox("Usar fecha y hora actual")
        self.usar_hora_actual.setChecked(True)
        self.usar_hora_actual.stateChanged.connect(self.toggle_fecha_hora_ingreso)
        form_layout.addRow("", self.usar_hora_actual)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botón de registrar
        self.btn_registrar_ingreso = QPushButton("Registrar Ingreso")
        self.btn_registrar_ingreso.setMinimumHeight(40)
        self.btn_registrar_ingreso.clicked.connect(self.registrar_ingreso_ui)
        layout.addWidget(self.btn_registrar_ingreso)
        
        # Deshabilitar campos de fecha y hora si se usa la actual
        self.toggle_fecha_hora_ingreso()
        
        layout.addStretch()
    
    def toggle_fecha_hora_ingreso(self):
        """Habilita o deshabilita los campos de fecha y hora según el checkbox."""
        usar_actual = self.usar_hora_actual.isChecked()
        self.fecha_ingreso.setEnabled(not usar_actual)
        self.hora_ingreso.setEnabled(not usar_actual)
        
        if usar_actual:
            self.fecha_ingreso.setDate(QDate.currentDate())
            self.hora_ingreso.setTime(QTime.currentTime())
    
    def validar_placa_ingreso(self):
        """Valida el formato de la placa en tiempo real."""
        placa = self.placa_ingreso.text().strip().upper()
        if placa:
            if db.validar_placa(placa):
                self.placa_ingreso.setStyleSheet("background-color: #c8e6c9;")  # Verde claro
            else:
                self.placa_ingreso.setStyleSheet("background-color: #ffcdd2;")  # Rojo claro
        else:
            self.placa_ingreso.setStyleSheet("")
    
    def crear_tab_salida(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Salida")
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Registro de Salida de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Formulario en un GroupBox
        form_group = QGroupBox("Datos de Salida")
        form_layout = QFormLayout()
        
        # Placa
        self.placa_salida = QLineEdit()
        self.placa_salida.setPlaceholderText("Ej: ABC123")
        self.placa_salida.textChanged.connect(self.validar_placa_salida)
        form_layout.addRow("Placa:", self.placa_salida)
        
        # Fecha y hora
        fecha_hora_layout = QHBoxLayout()
        
        # Fecha
        self.fecha_salida = QDateEdit()
        self.fecha_salida.setCalendarPopup(True)
        self.fecha_salida.setDate(QDate.currentDate())
        fecha_hora_layout.addWidget(QLabel("Fecha:"))
        fecha_hora_layout.addWidget(self.fecha_salida)
        
        # Hora
        self.hora_salida = QTimeEdit()
        self.hora_salida.setTime(QTime.currentTime())
        fecha_hora_layout.addWidget(QLabel("Hora:"))
        fecha_hora_layout.addWidget(self.hora_salida)
        
        form_layout.addRow("Fecha y Hora:", fecha_hora_layout)
        
        # Checkbox para usar fecha y hora actual
        self.usar_hora_actual_salida = QCheckBox("Usar fecha y hora actual")
        self.usar_hora_actual_salida.setChecked(True)
        self.usar_hora_actual_salida.stateChanged.connect(self.toggle_fecha_hora_salida)
        form_layout.addRow("", self.usar_hora_actual_salida)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botón de registrar
        self.btn_registrar_salida = QPushButton("Registrar Salida")
        self.btn_registrar_salida.setMinimumHeight(40)
        self.btn_registrar_salida.clicked.connect(self.registrar_salida_ui)
        layout.addWidget(self.btn_registrar_salida)
        
        # Deshabilitar campos de fecha y hora si se usa la actual
        self.toggle_fecha_hora_salida()
        
        layout.addStretch()
    
    def toggle_fecha_hora_salida(self):
        """Habilita o deshabilita los campos de fecha y hora según el checkbox."""
        usar_actual = self.usar_hora_actual_salida.isChecked()
        self.fecha_salida.setEnabled(not usar_actual)
        self.hora_salida.setEnabled(not usar_actual)
        
        if usar_actual:
            self.fecha_salida.setDate(QDate.currentDate())
            self.hora_salida.setTime(QTime.currentTime())
    
    def validar_placa_salida(self):
        """Valida si la placa existe en vehículos activos."""
        placa = self.placa_salida.text().strip().upper()
        if placa:
            # Verificar si la placa está en vehículos activos
            vehiculos = db.obtener_vehiculos_activos()
            placas_activas = [v[0] for v in vehiculos]
            
            if placa in placas_activas:
                self.placa_salida.setStyleSheet("background-color: #c8e6c9;")  # Verde claro
            else:
                self.placa_salida.setStyleSheet("background-color: #ffcdd2;")  # Rojo claro
        else:
            self.placa_salida.setStyleSheet("")
    
    def crear_tab_activos(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Vehículos Activos")
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Vehículos Actualmente en el Parqueadero")
        titulo.setAlignment(Qt.AlignCenter)
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Tabla de vehículos activos
        self.tabla_activos = QTableWidget()
        self.tabla_activos.setColumnCount(5)
        self.tabla_activos.setHorizontalHeaderLabels(["Placa", "Tipo", "Fecha Entrada", "Hora Entrada", "Acciones"])
        self.tabla_activos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_activos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_activos.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla_activos)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_actualizar_activos = QPushButton("Actualizar")
        self.btn_actualizar_activos.clicked.connect(self.cargar_vehiculos_activos)
        btn_layout.addWidget(self.btn_actualizar_activos)
        
        layout.addLayout(btn_layout)
    
    def cargar_vehiculos_activos(self):
        """Carga la lista de vehículos actualmente en el parqueadero."""
        self.tabla_activos.setRowCount(0)
        vehiculos = db.obtener_vehiculos_activos()
        
        for fila in vehiculos:
            row_position = self.tabla_activos.rowCount()
            self.tabla_activos.insertRow(row_position)
            
            placa, tipo, fecha_entrada, hora_entrada, minuto_entrada = fila
            
            self.tabla_activos.setItem(row_position, 0, QTableWidgetItem(placa))
            self.tabla_activos.setItem(row_position, 1, QTableWidgetItem(tipo))
            self.tabla_activos.setItem(row_position, 2, QTableWidgetItem(fecha_entrada))
            self.tabla_activos.setItem(row_position, 3, QTableWidgetItem(f"{hora_entrada}:{minuto_entrada:02d}"))
            
            # Botón de registrar salida
            btn_salida = QPushButton("Registrar Salida")
            btn_salida.clicked.connect(lambda checked, p=placa: self.registrar_salida_rapida(p))
            self.tabla_activos.setCellWidget(row_position, 4, btn_salida)
        
        # Actualizar contador en la pestaña
        self.tabs.setTabText(2, f"Vehículos Activos ({self.tabla_activos.rowCount()})")
    
    def registrar_salida_rapida(self, placa):
        """Registra la salida de un vehículo directamente desde la tabla de activos."""
        reply = QMessageBox.question(
            self, 
            "Confirmar Salida", 
            f"¿Desea registrar la salida del vehículo con placa {placa}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Usar fecha y hora actual
            fecha_actual, hora_actual, minuto_actual = db.obtener_fecha_hora_actual()
            
            success, result = db.registrar_salida(
                placa, 
                fecha_actual, 
                hora_actual, 
                minuto_actual, 
                "sistema"
            )
            
            if success:
                QMessageBox.information(
                    self, 
                    "Salida Registrada", 
                    f"Salida registrada correctamente:\n\n"
                    f"Placa: {placa}\n"
                    f"Duración: {result['duracion']} horas\n"
                    f"Valor a pagar: ${result['valor']:,.0f}"
                )
                self.cargar_vehiculos_activos()
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", result)
    
    def crear_tab_historial(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Historial")
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Historial de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Filtros en un GroupBox
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
        
        filtro_fecha_layout.addWidget(QLabel("Desde:"))
        self.filtro_fecha_inicio = QDateEdit()
        self.filtro_fecha_inicio.setCalendarPopup(True)
        self.filtro_fecha_inicio.setDate(QDate.currentDate().addDays(-30))
        filtro_fecha_layout.addWidget(self.filtro_fecha_inicio)
        
        filtro_fecha_layout.addWidget(QLabel("Hasta:"))
        self.filtro_fecha_fin = QDateEdit()
        self.filtro_fecha_fin.setCalendarPopup(True)
        self.filtro_fecha_fin.setDate(QDate.currentDate())
        filtro_fecha_layout.addWidget(self.filtro_fecha_fin)
        
        filtros_layout.addLayout(filtro_fecha_layout)
        
        # Botones de filtro
        filtro_botones_layout = QHBoxLayout()
        
        self.btn_aplicar_filtros = QPushButton("Aplicar Filtros")
        self.btn_aplicar_filtros.clicked.connect(self.cargar_historial)
        filtro_botones_layout.addWidget(self.btn_aplicar_filtros)
        
        self.btn_exportar_csv = QPushButton("Exportar CSV")
        self.btn_exportar_csv.clicked.connect(lambda: self.exportar_historial("csv"))
        filtro_botones_layout.addWidget(self.btn_exportar_csv)
        
        self.btn_exportar_excel = QPushButton("Exportar Excel")
        self.btn_exportar_excel.clicked.connect(lambda: self.exportar_historial("excel"))
        filtro_botones_layout.addWidget(self.btn_exportar_excel)
        
        filtros_layout.addLayout(filtro_botones_layout)
        
        filtros_group.setLayout(filtros_layout)
        layout.addWidget(filtros_group)
        
        # Tabla de historial
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(8)
        self.tabla_historial.setHorizontalHeaderLabels([
            "Placa", "Tipo", "Fecha Entrada", "Hora Entrada", 
            "Fecha Salida", "Hora Salida", "Duración (h)", "Valor"
        ])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_historial.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_historial.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla_historial)
    
    def cargar_historial(self):
        """Carga el historial de vehículos con los filtros aplicados."""
        self.tabla_historial.setRowCount(0)
        
        # Obtener valores de filtros
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
        
        for fila in historial:
            row_position = self.tabla_historial.rowCount()
            self.tabla_historial.insertRow(row_position)
            
            placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, \
            fecha_salida, hora_salida, minuto_salida, duracion, valor = fila
            
            self.tabla_historial.setItem(row_position, 0, QTableWidgetItem(placa))
            self.tabla_historial.setItem(row_position, 1, QTableWidgetItem(tipo))
            self.tabla_historial.setItem(row_position, 2, QTableWidgetItem(fecha_entrada))
            self.tabla_historial.setItem(row_position, 3, QTableWidgetItem(f"{hora_entrada}:{minuto_entrada:02d}"))
            self.tabla_historial.setItem(row_position, 4, QTableWidgetItem(fecha_salida if fecha_salida else "N/A"))
            self.tabla_historial.setItem(row_position, 5, QTableWidgetItem(f"{hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A"))
            self.tabla_historial.setItem(row_position, 6, QTableWidgetItem(f"{duracion:.2f}"))
            
            # Formato para el valor
            valor_item = QTableWidgetItem(f"${valor:,.0f}")
            valor_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla_historial.setItem(row_position, 7, valor_item)
        
        # Actualizar contador en la pestaña
        self.tabs.setTabText(3, f"Historial ({self.tabla_historial.rowCount()})")
    
    def exportar_historial(self, formato):
        """Exporta el historial en el formato especificado."""
        # Obtener valores de filtros
        filtro_placa = self.filtro_placa.text().strip()
        
        filtro_tipo = None
        if self.filtro_tipo.currentText() != "Todos":
            filtro_tipo = self.filtro_tipo.currentText()
        
        fecha_inicio = self.filtro_fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.filtro_fecha_fin.date().toString("yyyy-MM-dd")
        
        if formato == "csv":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar CSV", "historial_parqueadero.csv", "CSV Files (*.csv)"
            )
            
            if file_path:
                success, message = db.exportar_historial_csv(
                    file_path, filtro_placa, filtro_tipo, fecha_inicio, fecha_fin
                )
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                else:
                    QMessageBox.critical(self, "Error", message)
        
        elif formato == "excel":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Excel", "historial_parqueadero.xlsx", "Excel Files (*.xlsx)"
            )
            
            if file_path:
                success, message = db.exportar_historial_excel(
                    file_path, filtro_placa, filtro_tipo, fecha_inicio, fecha_fin
                )
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                else:
                    QMessageBox.critical(self, "Error", message)
    
    def registrar_ingreso_ui(self):
        """Registra el ingreso de un vehículo desde la interfaz."""
        placa = self.placa_ingreso.text().strip().upper()
        tipo = self.tipo_vehiculo.currentText()
        
        # Validar placa
        if not db.validar_placa(placa):
            QMessageBox.critical(self, "Error", "Formato de placa inválido. Verifique.")
            return
        
        # Obtener fecha y hora
        if self.usar_hora_actual.isChecked():
            fecha, hora, minuto = db.obtener_fecha_hora_actual()
        else:
            fecha = self.fecha_ingreso.date().toString("yyyy-MM-dd")
            hora = self.hora_ingreso.time().hour()
            minuto = self.hora_ingreso.time().minute()
        
        # Registrar ingreso
        success, message = db.registrar_ingreso(placa, fecha, hora, minuto, tipo, "sistema")
        
        if success:
            QMessageBox.information(
                self, 
                "Ingreso Registrado", 
                f"Ingreso registrado correctamente:\n\n"
                f"Placa: {placa}\n"
                f"Tipo: {tipo}\n"
                f"Fecha y Hora: {fecha} {hora}:{minuto:02d}"
            )
            self.placa_ingreso.clear()
            self.cargar_vehiculos_activos()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def registrar_salida_ui(self):
        """Registra la salida de un vehículo desde la interfaz."""
        placa = self.placa_salida.text().strip().upper()
        
        if not placa:
            QMessageBox.critical(self, "Error", "Debe ingresar una placa.")
            return
        
        # Obtener fecha y hora
        if self.usar_hora_actual_salida.isChecked():
            fecha, hora, minuto = db.obtener_fecha_hora_actual()
        else:
            fecha = self.fecha_salida.date().toString("yyyy-MM-dd")
            hora = self.hora_salida.time().hour()
            minuto = self.hora_salida.time().minute()
        
        # Confirmar acción
        reply = QMessageBox.question(
            self, 
            "Confirmar Salida", 
            f"¿Desea registrar la salida del vehículo con placa {placa}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Registrar salida
            success, result = db.registrar_salida(placa, fecha, hora, minuto, "sistema")
            
            if success:
                QMessageBox.information(
                    self, 
                    "Salida Registrada", 
                    f"Salida registrada correctamente:\n\n"
                    f"Placa: {placa}\n"
                    f"Duración: {result['duracion']} horas\n"
                    f"Valor a pagar: ${result['valor']:,.0f}"
                )
                self.placa_salida.clear()
                self.cargar_vehiculos_activos()
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", result)
