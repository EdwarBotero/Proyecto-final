import tkinter as tk #Nuestra biblioteca principal para la interfaz grafica
from gui import ParkingApp # Importamos nuestra clase ParkingApp del módulo gui.py

# Con esto nos aseguramos de que el codigo solo sea ejecutado cuando el archivo sea ejecutado directamente
if __name__ == "__main__": 
    root = tk.Tk() # Creamos la ventana principal de la aplicacion
    app = ParkingApp(root) # Crea una instancia de nuestra aplicacion (Esto nos ayuda a iniciar toda la interfaz que definimos en la clase ParkingApp)
    root.mainloop() # Con esto iniciamos el bucle principal de la aplicacion (Esto nos permite mantener la la aplicacion ejecutandose hasta que sea cerrada y nos ayuda a manejar todas las interaciones del usuario)
