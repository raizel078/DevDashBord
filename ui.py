from PySide6.QtWidgets import  QMainWindow  , QTabWidget  , QWidget

#code for the ui window.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 700)
        self.setWindowTitle('Nova DevBoard')

        #creation of the tab.
        self.tab = QTabWidget()
        self.setCentralWidget(self.tab)
        self.tab.addTab(QWidget(), 'CodeCLock')
        self.tab.addTab(QWidget(), 'Clipboard')
        self.tab.addTab(QWidget(), 'TODO')
        self.tab.setStyleSheet(f"""
            QTabBar::tab {{ width: {400 // 3}px; }}
            QTabBar::tab:selected {{ border: 2px solid white; }}
        """)
