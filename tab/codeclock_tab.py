from PySide6.QtWidgets import QWidget , QLabel , QVBoxLayout , QTableWidget , QHeaderView
import datetime
from PySide6.QtCore import QTimer , Qt

#now main ui code goes here,
class CodeClock(QWidget):
    def __init__(self):
        super().__init__()
        #for the real-time show.
        self.time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # for setting the timer to see the real time.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        #making the layout for tab screen for only code clock tab
        self.layout = QVBoxLayout()
        #creating a level to view the time and date
        self.time_bar = QLabel(str(self.time))
        #this will place the live timer in the center of the window.
        self.time_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #now below is styling to make the border only for the timer.
        self.time_bar.setStyleSheet('border: 4px solid white')
        #adding the time bar to the widget
        self.layout.addWidget(self.time_bar)
        #setting the layout i:e sending layout after changes to main layout
        self.setLayout(self.layout)
        #now the layout for the table for our date, session and duration
        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(['Date','session', 'Duration'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)



    def update_time(self):
        self.time_bar.setText(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


