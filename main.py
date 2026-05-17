import sys
from PySide6.QtWidgets import  QApplication
from ui import MainWindow


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow() # we will pass the window later
    window.show()
    sys.exit(app.exec())