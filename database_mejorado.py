import sqlite3
import csv
from pathlib import Path
from datetime import datetime, date, time

# Ruta donde tenemos almacenada la BD
DB_PATH = Path("data/parking.db")

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
    
    # Creamos la tabla de historial con soporte para fecha y hora completas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT,
            tipo TEXT,
            fecha_entrada TEXT,
            hora_entrada INTEGER,
            minuto_entrada INTEGER,
            fecha_salida TEXT,
            hora_salida INTEGER,
            minuto_salida INTEGER,
            duracion_horas REAL,
            valor_pagado REAL,
            usuario_registro TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Creamos tabla de usuarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            usuario TEXT UNIQUE,
            password TEXT,
            rol TEXT CHECK (rol IN ('admin', 'operador')),
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Creamos tabla de tarifas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tarifas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_vehiculo TEXT,
            dia_semana TEXT,
            hora_inicio INTEGER,
            hora_fin INTEGER,
            tarifa_hora REAL,
            tarifa_fraccion REAL,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Insertamos usuario admin por defecto si no existe
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO usuarios (nombre, usuario, password, rol) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", "admin123", "admin")
        )
    
    # Insertamos tarifas por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM tarifas")
    if cursor.fetchone()[0] == 0:
        # Tarifa para carros (todos los días)
        conn.execute(
            "INSERT INTO tarifas (tipo_vehiculo, dia_semana, hora_inicio, hora_fin, tarifa_hora, tarifa_fraccion) VALUES (?, ?, ?, ?, ?, ?)",
            ("Carro", "todos", 0, 23, 3000, 750)
        )
        # Tarifa para motos (todos los días)
        conn.execute(
            "INSERT INTO tarifas (tipo_vehiculo, dia_semana, hora_inicio, hora_fin, tarifa_hora, tarifa_fraccion) VALUES (?, ?, ?, ?, ?, ?)",
            ("Moto", "todos", 0, 23, 1500, 400)
        )
    
    conn.commit()
    return conn

def obtener_fecha_hora_actual():
    """Retorna la fecha y hora actual en formato adecuado para la BD."""
    ahora = datetime.now()
    fecha_actual = ahora.strftime("%Y-%m-%d")
    hora_actual = ahora.hour
    minuto_actual = ahora.minute
    return fecha_actual, hora_actual, minuto_actual

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

def obtener_tarifa(tipo_vehiculo, fecha, hora):
    """Obtiene la tarifa aplicable según tipo de vehículo, día y hora."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtenemos el día de la semana (0=lunes, 6=domingo)
        dia_semana = datetime.strptime(fecha, "%Y-%m-%d").weekday()
        dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        
        # Buscamos tarifa específica para este día y hora
        cursor.execute("""
            SELECT tarifa_hora, tarifa_fraccion FROM tarifas 
            WHERE tipo_vehiculo = ? AND 
                  (dia_semana = ? OR dia_semana = 'todos') AND
                  hora_inicio <= ? AND hora_fin >= ? AND
                  activo = 1
            ORDER BY CASE WHEN dia_semana = ? THEN 0 ELSE 1 END
            LIMIT 1
        """, (tipo_vehiculo, dias[dia_semana], hora, hora, dias[dia_semana]))
        
        resultado = cursor.fetchone()
        if resultado:
            return resultado
        
        # Si no hay tarifa específica, usamos la tarifa por defecto
        return (3000, 750) if tipo_vehiculo == "Carro" else (1500, 400)
    
    except sqlite3.Error as e:
        print(f"Error al obtener tarifa: {e}")
        return (3000, 750) if tipo_vehiculo == "Carro" else (1500, 400)

def calcular_valor(tipo_vehiculo, duracion_horas, fecha_entrada, hora_entrada):
    """Calcula el valor a pagar según tipo de vehículo y duración."""
    try:
        # Obtenemos la tarifa aplicable
        tarifa_hora, tarifa_fraccion = obtener_tarifa(tipo_vehiculo, fecha_entrada, hora_entrada)
        
        # Calculamos horas completas y fracción
        horas_completas = int(duracion_horas)
        fraccion = duracion_horas - horas_completas
        
        # Si hay fracción, aplicamos tarifa por fracción (cada 15 minutos)
        if fraccion > 0:
            if fraccion <= 0.25:
                valor_fraccion = tarifa_fraccion
            elif fraccion <= 0.5:
                valor_fraccion = tarifa_fraccion * 2
            elif fraccion <= 0.75:
                valor_fraccion = tarifa_fraccion * 3
            else:
                valor_fraccion = tarifa_hora  # Si es más de 45 minutos, cobra hora completa
        else:
            valor_fraccion = 0
        
        # Calculamos valor total
        valor_total = (horas_completas * tarifa_hora) + valor_fraccion
        
        return round(valor_total, 0)
    
    except Exception as e:
        print(f"Error en cálculo de valor: {e}")
        # Valores por defecto en caso de error
        tarifas = {"Carro": 3000, "Moto": 1500}
        return tarifas.get(tipo_vehiculo, 2000) * duracion_horas

def validar_placa(placa):
    """Valida el formato de la placa según normativa colombiana."""
    if not placa or len(placa) < 5 or len(placa) > 7:
        return False
    
    # Formato básico: 3 letras seguidas de 3 números (carros) o 2 letras, 2 números y 1 letra (motos)
    return True

def registrar_ingreso(placa, fecha=None, hora=None, minuto=None, tipo="Carro", usuario="sistema"):
    """Registra el ingreso de un vehículo al parqueadero."""
    if not validar_placa(placa):
        return False, "Formato de placa inválido"
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verificar si la placa ya está registrada
        cursor.execute("SELECT placa FROM vehiculos WHERE placa=?", (placa,))
        if cursor.fetchone():
            return False, "La placa ya está registrada en el parqueadero"
        
        # Si no se proporcionan fecha y hora, usamos la actual
        if fecha is None or hora is None or minuto is None:
            fecha, hora, minuto = obtener_fecha_hora_actual()
        
        # Validamos el tipo de vehículo
        tipo = tipo.capitalize()
        if tipo not in ["Carro", "Moto"]:
            return False, "Tipo de vehículo inválido"
        
        # Insertar el vehículo en la tabla de vehículos activos
        conn.execute(
            "INSERT INTO vehiculos (placa, fecha_entrada, hora_entrada, minuto_entrada, tipo, usuario) VALUES (?, ?, ?, ?, ?, ?)",
            (placa, fecha, hora, minuto, tipo, usuario)
        )
        conn.commit()
        return True, "Ingreso registrado correctamente"
    
    except sqlite3.Error as e:
        print(f"Error en registrar ingreso: {e}")
        return False, f"Error en la base de datos: {e}"

def registrar_salida(placa, fecha_salida=None, hora_salida=None, minuto_salida=None, usuario="sistema"):
    """Registra la salida de un vehículo del parqueadero."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verificar si el vehículo está en el parqueadero
        cursor.execute(
            "SELECT fecha_entrada, hora_entrada, minuto_entrada, tipo FROM vehiculos WHERE placa=?",
            (placa,)
        )
        fila = cursor.fetchone()
        if not fila:
            return False, "Vehículo no encontrado en el parqueadero"
        
        fecha_entrada, hora_entrada, minuto_entrada, tipo = fila
        
        # Si no se proporcionan fecha y hora de salida, usamos la actual
        if fecha_salida is None or hora_salida is None or minuto_salida is None:
            fecha_salida, hora_salida, minuto_salida = obtener_fecha_hora_actual()
        
        # Calculamos la duración y el valor a pagar
        duracion = calcular_duracion(
            fecha_entrada, hora_entrada, minuto_entrada,
            fecha_salida, hora_salida, minuto_salida
        )
        
        valor = calcular_valor(tipo, duracion, fecha_entrada, hora_entrada)
        
        # Registramos en el historial
        cursor.execute(
            """
            INSERT INTO historial 
            (placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, 
             fecha_salida, hora_salida, minuto_salida, duracion_horas, valor_pagado, usuario_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (placa, tipo, fecha_entrada, hora_entrada, minuto_entrada,
             fecha_salida, hora_salida, minuto_salida, duracion, valor, usuario)
        )
        
        # Eliminamos el vehículo de la tabla de vehículos activos
        cursor.execute("DELETE FROM vehiculos WHERE placa=?", (placa,))
        conn.commit()
        
        return True, {
            "duracion": duracion,
            "valor": valor,
            "tipo": tipo,
            "entrada": f"{fecha_entrada} {hora_entrada}:{minuto_entrada:02d}",
            "salida": f"{fecha_salida} {hora_salida}:{minuto_salida:02d}"
        }
    
    except sqlite3.Error as e:
        print(f"Error en registrar salida: {e}")
        return False, f"Error en la base de datos: {e}"

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

def obtener_historial(filtro_placa=None, filtro_tipo=None, fecha_inicio=None, fecha_fin=None):
    """Obtiene el historial de vehículos con opciones de filtrado."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Construimos la consulta base
        query = """
            SELECT placa, tipo, fecha_entrada, hora_entrada, minuto_entrada,
                   fecha_salida, hora_salida, minuto_salida, duracion_horas, valor_pagado
            FROM historial
            WHERE 1=1
        """
        params = []
        
        # Añadimos filtros si se proporcionan
        if filtro_placa:
            query += " AND placa LIKE ?"
            params.append(f"%{filtro_placa}%")
        
        if filtro_tipo:
            query += " AND tipo = ?"
            params.append(filtro_tipo)
        
        if fecha_inicio:
            query += " AND fecha_entrada >= ?"
            params.append(fecha_inicio)
        
        if fecha_fin:
            query += " AND fecha_entrada <= ?"
            params.append(fecha_fin)
        
        # Ordenamos por fecha de registro descendente
        query += " ORDER BY fecha_registro DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    
    except sqlite3.Error as e:
        print(f"Error en obtener historial: {e}")
        return []

def exportar_historial_csv(ruta="historial_parqueadero.csv", filtro_placa=None, filtro_tipo=None, fecha_inicio=None, fecha_fin=None):
    """Exporta el historial a un archivo CSV con opciones de filtrado."""
    try:
        historial = obtener_historial(filtro_placa, filtro_tipo, fecha_inicio, fecha_fin)
        if not historial:
            return False, "No hay datos para exportar"
        
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                "Placa", "Tipo", "Fecha Entrada", "Hora Entrada", 
                "Fecha Salida", "Hora Salida", "Duración (horas)", "Valor"
            ])
            
            for fila in historial:
                placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, \
                fecha_salida, hora_salida, minuto_salida, duracion, valor = fila
                
                # Formateamos las horas para mejor legibilidad
                entrada_str = f"{fecha_entrada} {hora_entrada}:{minuto_entrada:02d}"
                salida_str = f"{fecha_salida} {hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A"
                
                writer.writerow([
                    placa, tipo, fecha_entrada, f"{hora_entrada}:{minuto_entrada:02d}",
                    fecha_salida, f"{hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A",
                    duracion, valor
                ])
        
        return True, f"Historial exportado a '{ruta}'"
    
    except Exception as e:
        print(f"Error al exportar CSV: {e}")
        return False, f"Error al exportar: {e}"

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
        
        # Añadimos encabezados
        headers = [
            "Placa", "Tipo", "Fecha Entrada", "Hora Entrada", 
            "Fecha Salida", "Hora Salida", "Duración (horas)", "Valor"
        ]
        
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
            
            # Formateamos las horas para mejor legibilidad
            entrada_str = f"{hora_entrada}:{minuto_entrada:02d}"
            salida_str = f"{hora_salida}:{minuto_salida:02d}" if fecha_salida else "N/A"
            
            # Insertamos datos en la hoja
            ws.cell(row=row_num, column=1, value=placa)
            ws.cell(row=row_num, column=2, value=tipo)
            ws.cell(row=row_num, column=3, value=fecha_entrada)
            ws.cell(row=row_num, column=4, value=entrada_str)
            ws.cell(row=row_num, column=5, value=fecha_salida if fecha_salida else "N/A")
            ws.cell(row=row_num, column=6, value=salida_str)
            ws.cell(row=row_num, column=7, value=duracion)
            ws.cell(row=row_num, column=8, value=valor)
            
            # Formato para valor
            ws.cell(row=row_num, column=8).number_format = "$#,##0"
        
        # Ajustamos ancho de columnas
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

def realizar_backup():
    """Realiza una copia de seguridad de la base de datos."""
    try:
        import shutil
        from datetime import datetime
        
        if not DB_PATH.exists():
            return False, "No existe la base de datos para respaldar"
        
        # Creamos directorio de backups si no existe
        backup_dir = Path("data/backups")
        backup_dir.mkdir(exist_ok=True, parents=True)
        
        # Nombre del archivo de backup con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"parking_backup_{timestamp}.db"
        
        # Copiamos la base de datos
        shutil.copy2(DB_PATH, backup_file)
        
        return True, f"Backup creado en {backup_file}"
    
    except Exception as e:
        print(f"Error al realizar backup: {e}")
        return False, f"Error al realizar backup: {e}"

def verificar_usuario(usuario, password):
    """Verifica las credenciales de un usuario."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, nombre, rol FROM usuarios WHERE usuario = ? AND password = ? AND activo = 1",
            (usuario, password)
        )
        
        resultado = cursor.fetchone()
        if resultado:
            return True, {
                "id": resultado[0],
                "nombre": resultado[1],
                "rol": resultado[2],
                "usuario": usuario
            }
        
        return False, "Credenciales inválidas o usuario inactivo"
    
    except sqlite3.Error as e:
        print(f"Error al verificar usuario: {e}")
        return False, f"Error en la base de datos: {e}"

def obtener_estadisticas(fecha_inicio=None, fecha_fin=None):
    """Obtiene estadísticas de uso del parqueadero."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Si no se proporcionan fechas, usamos el último mes
        if not fecha_inicio:
            fecha_inicio = (datetime.now().replace(day=1) - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
        
        # Total de ingresos
        cursor.execute(
            "SELECT SUM(valor_pagado) FROM historial WHERE fecha_entrada BETWEEN ? AND ?",
            (fecha_inicio, fecha_fin)
        )
        total_ingresos = cursor.fetchone()[0] or 0
        
        # Vehículos por tipo
        cursor.execute(
            "SELECT tipo, COUNT(*) FROM historial WHERE fecha_entrada BETWEEN ? AND ? GROUP BY tipo",
            (fecha_inicio, fecha_fin)
        )
        vehiculos_por_tipo = cursor.fetchall()
        
        # Promedio de duración
        cursor.execute(
            "SELECT AVG(duracion_horas) FROM historial WHERE fecha_entrada BETWEEN ? AND ?",
            (fecha_inicio, fecha_fin)
        )
        promedio_duracion = cursor.fetchone()[0] or 0
        
        # Horas pico (más entradas)
        cursor.execute(
            """
            SELECT hora_entrada, COUNT(*) as cantidad 
            FROM historial 
            WHERE fecha_entrada BETWEEN ? AND ?
            GROUP BY hora_entrada 
            ORDER BY cantidad DESC 
            LIMIT 3
            """,
            (fecha_inicio, fecha_fin)
        )
        horas_pico = cursor.fetchall()
        
        return {
            "total_ingresos": total_ingresos,
            "vehiculos_por_tipo": vehiculos_por_tipo,
            "promedio_duracion": promedio_duracion,
            "horas_pico": horas_pico
        }
    
    except sqlite3.Error as e:
        print(f"Error al obtener estadísticas: {e}")
        return None

# Migración de datos antiguos (si es necesario)
def migrar_datos_antiguos():
    """Migra datos del formato antiguo al nuevo esquema."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verificamos si existe la tabla historial antigua (sin campos de fecha)
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='historial' AND 
            sql NOT LIKE '%fecha_entrada%'
        """)
        
        if cursor.fetchone():
            # La tabla existe en formato antiguo, necesitamos migrar
            print("Migrando datos antiguos...")
            
            # Obtenemos los datos antiguos
            cursor.execute("""
                SELECT placa, tipo, hora_entrada, hora_salida, duracion, valor_pagado
                FROM historial
            """)
            registros_antiguos = cursor.fetchall()
            
            # Renombramos la tabla antigua
            conn.execute("ALTER TABLE historial RENAME TO historial_old")
            
            # Creamos la nueva tabla con el esquema actualizado
            conn.execute('''
                CREATE TABLE historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT,
                    tipo TEXT,
                    fecha_entrada TEXT,
                    hora_entrada INTEGER,
                    minuto_entrada INTEGER,
                    fecha_salida TEXT,
                    hora_salida INTEGER,
                    minuto_salida INTEGER,
                    duracion_horas REAL,
                    valor_pagado REAL,
                    usuario_registro TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fecha actual para los registros migrados
            fecha_actual = date.today().strftime("%Y-%m-%d")
            
            # Insertamos los datos antiguos en la nueva tabla
            for placa, tipo, hora_entrada, hora_salida, duracion, valor_pagado in registros_antiguos:
                conn.execute(
                    """
                    INSERT INTO historial 
                    (placa, tipo, fecha_entrada, hora_entrada, minuto_entrada, 
                     fecha_salida, hora_salida, minuto_salida, duracion_horas, valor_pagado, usuario_registro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (placa, tipo, fecha_actual, hora_entrada, 0, 
                     fecha_actual, hora_salida, 0, duracion, valor_pagado, "migración")
                )
            
            conn.commit()
            print(f"Migración completada: {len(registros_antiguos)} registros")
            return True
        
        return False  # No era necesario migrar
    
    except sqlite3.Error as e:
        print(f"Error en migración: {e}")
        return False
