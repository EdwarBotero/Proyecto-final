import sys
from PyQt5.QtWidgets import QApplication
from gui_qt_mejorado import ParkingApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingApp()
    window.show()
    sys.exit(app.exec_())
