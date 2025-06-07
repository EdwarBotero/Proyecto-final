#Sistema de Parqueadero Mejorado - Punto de entrada principal

#Este archivo sirve como punto de entrada principal para la aplicación del Sistema de Parqueadero.
#Inicializa la aplicación PyQt5 y muestra la ventana principal.


# Importación de módulos necesarios
import sys  # Módulo para interactuar con el sistema operativo
from PyQt5.QtWidgets import QApplication  # Clase principal para aplicaciones PyQt5
from gui_qt_mejorado import ParkingApp  # Importamos nuestra clase principal de la interfaz gráfica

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    # Creamos una instancia de QApplication con los argumentos del sistema
    # QApplication gestiona el flujo de control y configuración principal de la aplicación GUI
    app = QApplication(sys.argv)
    
    # Creamos una instancia de nuestra ventana principal personalizada
    window = ParkingApp()
    
    # Mostramos la ventana principal
    window.show()
    
    # Iniciamos el bucle de eventos de la aplicación
    # app.exec_() inicia el bucle principal de eventos de Qt, que espera hasta que se cierre la aplicación
    # sys.exit() asegura que la aplicación se cierre correctamente con el código de salida adecuado
    sys.exit(app.exec_())


