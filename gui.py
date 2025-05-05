import tkinter as tk #Nuestra biblioteca principal para la interfaz grafica
from tkinter import ttk, messagebox # Importamos la biblioteca de tkinter para crear la interfaz grafica y el modulo messagebox con widgets mejorados
from database import registrar_ingreso, registrar_salida, obtener_historial, exportar_historial_csv # Importamos las funciones de la base de datos que nos permiten registrar el ingreso y salida de vehiculos, obtener el historial y exportar el historial a un archivo CSV

# Definimos la clase ParkingApp que va a contener toda la logica de la aplicacion
class ParkingApp:
    # Definimos el constructor de la clase ParkingApp, que va a inicializar la ventana principal y los widgets de la aplicacion
    # En este caso se inicializa la ventana principal, el notebook que va a contener las diferentes pestañas de la aplicacion y las pestañas de ingreso, salida e historial
    def __init__(self, root):
        self.root = root # Inicializamos la ventana principal
        self.root.title("Sistema de Parqueadero")
        self.root.geometry("700x450") #El tamaño de la ventana principal
        
        ## Inicializamos el notebook que va a contener las diferentes pestañas de la aplicacion
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        ## Creamos las pestañas de ingreso, salida e historial
        self.crear_tab_ingreso()
        self.crear_tab_salida()
        self.crear_tab_historial()
    
    # Definimos la funcion para crear la pestaña de ingreso, en este caso se crean los widgets que van a contener los campos de ingreso y el boton de registrar ingreso
    # En este caso se crean los campos de placa, hora de ingreso y tipo de vehiculo, y el boton de registrar ingreso
    def crear_tab_ingreso(self):
        tab = ttk.Frame(self.notebook) # Creamos la pestaña de ingreso
        self.notebook.add(tab, text="Ingreso") # Agregamos la pestaña al notebook
        
        # Campo: Placa
        ttk.Label(tab, text="Placa:").grid(row=0, column=0, padx=10, pady=5, sticky="e") # Creamos el campo de placa
        self.placa_ingreso = ttk.Entry(tab, width=20) # Creamos el campo de entrada para la placa
        self.placa_ingreso.grid(row=0, column=1, padx=10, pady=5) # Agregamos el campo de entrada a la pestaña
        
        # Campo: Hora de ingreso
        ttk.Label(tab, text="Hora de ingreso (0-23):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.hora_ingreso = ttk.Entry(tab, width=5)
        self.hora_ingreso.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Campo: Tipo de vehículo
        ttk.Label(tab, text="Tipo:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.tipo_vehiculo = ttk.Combobox(tab, values=["Carro", "Moto"], state="readonly", width=10)
        self.tipo_vehiculo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Boton para registrar ingreso
        ttk.Button(tab, text="Registrar Ingreso", command=self.registrar_ingreso_ui).grid(
            row=3, column=0, columnspan=2, pady=15 
        ) 
    
    # Definimos la funcion para crear la pestaña de salida, en este caso se crean los widgets que van a contener los campos de salida y el boton de registrar salida
    # En este caso se crean los campos de placa y hora de salida, y el boton de registrar salida
    def crear_tab_salida(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Salida")
        
        # Campo: Placa
        ttk.Label(tab, text="Placa:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.placa_salida = ttk.Entry(tab, width=20)
        self.placa_salida.grid(row=0, column=1, padx=10, pady=5)
        
        # Campo: Hora de salida
        ttk.Label(tab, text="Hora de salida (0-23):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.hora_salida = ttk.Entry(tab, width=5)
        self.hora_salida.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Botón
        ttk.Button(tab, text="Registrar Salida", command=self.registrar_salida_ui).grid(
            row=2, column=0, columnspan=2, pady=15
        )
    
    # Definimos la funcion para crear la pestaña de historial, en este caso se crean los widgets que van a contener el historial de vehiculos y los botones de actualizar y exportar
    # En este caso se crea un Treeview con scrollbar para mostrar el historial de vehiculos y los botones de actualizar y exportar
    def crear_tab_historial(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Historial")
        
        # Frame para contener el Treeview con scrollbar
        frame_tree = ttk.Frame(tab)
        frame_tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(frame_tree, orient="vertical") 
        scroll_y.pack(side="right", fill="y")
        
        # Asignamos los nombres de las columnas y el Treeview
        self.tree = ttk.Treeview(
            frame_tree,
            columns=("placa", "tipo", "entrada", "salida", "horas", "valor"),
            show="headings",
            yscrollcommand=scroll_y.set,
            height=15
        )
        
        # configuramos las columnas del Treeview
        columnas = [ 
            ("Placa", 100),
            ("Tipo", 80),
            ("Entrada", 80),
            ("Salida", 80),
            ("Horas", 60),
            ("Valor", 100)
        ]
        
        # Configuramos las columnas y sus encabezados
        for col, width in columnas:
            self.tree.heading(col.lower(), text=col)  # Usar lowercase para coincidir con columns
            self.tree.column(col.lower(), width=width, anchor="center") 
        
        self.tree.pack(expand=True, fill="both")
        scroll_y.config(command=self.tree.yview) # Asignamos el scrollbar al Treeview
        
        # Frame para los Botones
        frame_botones = ttk.Frame(tab)
        frame_botones.pack(pady=10)
        
        # Botones para Actualizar y Exportar CSV
        ttk.Button(frame_botones, text="Actualizar", command=self.cargar_historial).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=5)
    
    # Definimos la funcion para validar la hora de ingreso y salida, en este caso se valida que la hora sea un numero entre 0 y 23
    def validar_hora(self, hora_str):
        try:
            hora = int(hora_str) # Lo usamos con el fin de convertir la hora a un entero
            if 0 <= hora <= 23: # Verificamos que la hora este entre 0 y 23
                return hora # Si la hora es valida, devolvemos la hora
            return None # Si la hora no es valida, devolvemos None
        except ValueError:
            return None # Si no se puede convertir a entero, devolvemos None
    
    # Definimos la funcion para registrar el ingreso de un vehiculo, en este caso se valida que los datos sean correctos y se llama a la funcion registrar_ingreso de la base de datos
    def registrar_ingreso_ui(self):
        placa = self.placa_ingreso.get().strip().upper() # Obtenemos la placa y la convertimos a mayusculas
        hora = self.validar_hora(self.hora_ingreso.get()) # Obtenemos la hora y la validamos
        tipo = self.tipo_vehiculo.get()
        
        # Validacion basica 
        if not placa or hora is None or not tipo: 
            messagebox.showerror("Error", "Datos inválidos. Verifique:")
            return
        
        # Lo usamos para registrar el ingreso
        if registrar_ingreso(placa, hora, tipo):
            messagebox.showinfo("Éxito", f"Ingreso registrado:\nPlaca: {placa}\nHora: {hora}:00\nTipo: {tipo}")
            # Lo usamos para limpiar los campos
            self.placa_ingreso.delete(0, tk.END)
            self.hora_ingreso.delete(0, tk.END)
            self.tipo_vehiculo.set("")
        else:
            messagebox.showerror("Error", "¡La placa ya está registrada o hay un error!") # Si la placa ya se encuentra registrada o tenemos error mostramos el mensaje
    
    # Definimos la funcion para registrar la salida de un vehiculo, en este caso se valida que los datos sean correctos y se llama a la funcion registrar_salida de la base de datos
    def registrar_salida_ui(self):
        # Lo usamos para optener y limpiar los datos
        placa = self.placa_salida.get().strip().upper()
        hora = self.validar_hora(self.hora_salida.get())
        
        # Validacion basica de salida del parqueadero
        if not placa or hora is None:
            messagebox.showerror("Error", "Datos inválidos. Verifique:")
            return
        
        # Hce el registro en la BD de la salida
        if registrar_salida(placa, hora):
            messagebox.showinfo("Éxito", f"Salida registrada:\nPlaca: {placa}")
            #Lo samos para limpiar los campos
            self.placa_salida.delete(0, tk.END)
            self.hora_salida.delete(0, tk.END)
            self.cargar_historial()
        else:
            messagebox.showerror("Error", "Placa no encontrada o error en BD.") #En caso de que la placa no exista o este mal devolvemos el mensaje de error
    
    # Definimos la funcion para cargar el historial de vehiculos, en este caso se llama a la funcion obtener_historial de la base de datos y se cargan los datos en el Treeview
    def cargar_historial(self):
        #Limpia el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lo usamos para obtener los datos y los insertamos en el treeview
        for fila in obtener_historial():
            self.tree.insert("", "end", values=(
                fila[0],  # Placa
                fila[1],  # Tipo
                f"{fila[2]}:00",  # Hora Entrada
                f"{fila[3]}:00" if fila[3] is not None else "N/A",  # Hora Salida
                fila[4],  # Tiempo en parqueadero
                f"${fila[5]:,.0f}"  # <-- Aquí mostramos el valor con $, pero la columna se llama "valor"
            ))
    
    # Definimos la funcion para exportar el historial a un archivo CSV, en este caso se llama a la funcion exportar_historial_csv de la base de datos y se muestra un mensaje de exito o error
    def exportar_csv(self):
        # Lo usamos para que una vez tengamos datos en historial podamos exportar
        if exportar_historial_csv():
            messagebox.showinfo("Éxito", "Historial exportado a 'historial_parqueadero.csv'")
        else:
            messagebox.showerror("Error", "No se pudo exportar el historial.")