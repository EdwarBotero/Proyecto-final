import sqlite3 # Para este trabajo vamos a implementar BD sqlite ya que es facil de usar para lo que necesitamos
import csv # Con este vamos a generar el archivo CSV del historal de vehiculos que pasaron por el parqueadero
from pathlib import Path # Lo vamos a usar para manejo de archivos multiplataforma ya que la BD nos estaba generando novedad al conectarse
from datetime import datetime # Lo usaremos para trabajar con las horas de entrada y de salida de vehicuos

DB_PATH = Path("data/parking.db") # Ruta donde tenemos almacenada la BD

def conectar():
    DB_PATH.parent.mkdir(exist_ok=True) # Esta parte la tuvimos que implementar ya que trataba de conectarse a la BD  pero aun no teniaos la ruta (esto se encarga de crearla si no exixte)
    conn = sqlite3.connect(DB_PATH) # hacemos la conexion con la BD
    
    #Realizamos la creacion de las tablas que vamos a usar para almacenar los vehiculos y el historial de los mismos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            placa TEXT PRIMARY KEY,
            hora_entrada INTEGER,
            tipo TEXT CHECK (tipo IN ('Carro', 'Moto'))
        )
    ''')
    
    # Creamos la tabla de historial donde vamos a almacenar los vehiculos que ya salieron del parqueadero
    conn.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT,
            tipo TEXT,
            hora_entrada INTEGER,
            hora_salida INTEGER,
            duracion INTEGER,
            valor_pagado REAL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    return conn

# Definimos la funcion para calcular el valor a pagar por el vehiculo dependiendo de su tipo y la duracion que estuvo en el parqueadero
# En este caso definimos que el carro tiene un costo de 3000 por hora y la moto 1500 por hora, si no es ninguno de los dos se le asigna un costo de 2000 por hora
def calcular_valor(tipo, duracion):
    tarifas = {"Carro": 3000, "Moto": 1500}
    return tarifas.get(tipo, 2000) * duracion

# Definimos la funcion para registrar el ingreso de un vehiculo al parqueadero, en este caso se le asigna una hora de entrada y se valida que la placa no haya sido registrada antes
def registrar_ingreso(placa, hora, tipo):
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verificar si la placa ya está registrada (Con esto no vamos a permitir placas duplicadas que no registren una salida)
        cursor.execute("SELECT placa FROM vehiculos WHERE placa=?", (placa,))
        if cursor.fetchone():
            return False
        
        # Con esto nos aseguramos de que las opciones de tipo de vehiculo sean solo Carro o Moto
        tipo = tipo.capitalize()
        if tipo not in ["Carro", "Moto"]:
            return False
        
        # Insertar el vehículo en la tabla de vehículos activos
        conn.execute(
            "INSERT INTO vehiculos (placa, hora_entrada, tipo) VALUES (?, ?, ?)",
            (placa, hora, tipo)
        )
        conn.commit()
        return True
    
    # En caso de no poder hacer el ingreso devolvemos mensaje de error
    except sqlite3.Error as e:
        print(f"Error en registrar ingreso: {e}")
        return False

# Definimos la funcion para registrar la salida de un vehiculo del parqueadero, en este caso se le asigna una hora de salida y se valida que la placa haya sido registrada antes
# En este caso se le asigna un costo dependiendo de la duracion que estuvo en el parqueadero y se elimina de la tabla de vehiculos activos
def registrar_salida(placa, hora_salida):
    try:
        conn = conectar() # Conectamos a la BD para verificar los datos almacenados
        cursor = conn.cursor()
        
        # Por medio de la Placa vamos averificar si el vehiculo ya esta registrado en la tabla de vehiculos activos
        cursor.execute(
            "SELECT hora_entrada, tipo FROM vehiculos WHERE placa=?",
            (placa,)
        )
        fila = cursor.fetchone() # Con esto vamos a obtener la hora de entrada y el tipo de vehiculo que tenemos registrado
        if not fila:# Si no existe la placa en la tabla de vehiculos activos, devolvemos False
            return False 
        
        hora_entrada, tipo = fila # Obtenemos la hora de entrada y el tipo de vehiculo que tenemos registrado
        # Calculamos la duraion de un vehiculo en el parqueadero, si la hora de salida es menor a la de entrada significa que el vehiculo estuvo durante la noche y se le suma 24 horas
        # Si no es asi simplemente se le resta la hora de entrada a la de salida
        if hora_salida < hora_entrada:
            duracion = (24 - hora_entrada) + hora_salida
        else:
            duracion = hora_salida - hora_entrada
        
        valor = calcular_valor(tipo, duracion) # Con esto calculamos el valor a pagar por el vehiculo dependiendo de su tipo y la duracion que estuvo en el parqueadero
        
        # Ingresamos el vehículo en el historial
        cursor.execute(
            """
            INSERT INTO historial 
            (placa, tipo, hora_entrada, hora_salida, duracion, valor_pagado)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (placa, tipo, hora_entrada, hora_salida, duracion, valor)
        )
        
        # Eliminamos el vehículo de la tabla de vehículos activos porque ya se registro su salida
        # Esto lo hacemos para que no se repita la placa en la tabla de vehiculos activos y no se pueda registrar una salida sin haber registrado una entrada
        cursor.execute("DELETE FROM vehiculos WHERE placa=?", (placa,))
        conn.commit()
        return True
    except sqlite3.Error as e: # En caso de no poder hacer el ingreso devolvemos mensaje de error
        print(f"Error en registrar salida: {e}")
        return False

# Definimos la funcion para obtener el historial de vehiculos que han pasado por el parqueadero, en este caso se ordena por fecha de registro
# En este caso se obtiene la placa, el tipo de vehiculo, la hora de entrada, la hora de salida, la duracion y el valor pagado
def obtener_historial():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT placa, tipo, hora_entrada, hora_salida, duracion, valor_pagado
            FROM historial
            ORDER BY fecha_registro DESC
        """)
        return cursor.fetchall() # Con esto vamos a optener los registros almacenados en la tabla de historial
    except sqlite3.Error as e: # En caso de no poder hacer el ingreso devolvemos mensaje de error
        print(f"Error en obtener historial: {e}")
        return []

# Definimos la funcion para exportar el historial a un archivo CSV, en este caso se crea un archivo CSV con los registros almacenados en la tabla de historial
def exportar_historial_csv(ruta="historial_parqueadero.csv"):
    try:
        historial = obtener_historial() # Obtenemos el historial de vehiculos que han pasado por el parqueadero
        if not historial:
            return False # Si no hay historial, devolvemos False
        
        # Con esto lo que hacemos es que creamos el archivo CSV o en caso de que ya exista lo sobreescribimos
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Placa", "Tipo", "Entrada", "Salida", "Horas", "Valor"]) # Con esto escribimos la cabecera del archivo CSV
            for fila in historial: # Con esto escribimos los registros almacenados en la tabla de historial
                writer.writerow(fila) 
        return True
    except Exception as e: # En caso de no poder hacer el ingreso devolvemos mensaje de error
        print(f"Error al exportar CSV: {e}")
        return False