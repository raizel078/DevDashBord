from PySide6.QtWidgets import QWidget , QLabel , QVBoxLayout
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
        #adding the time bar to the widget
        self.layout.addWidget(self.time_bar)
        #setting the layout i:e sending layout after changes to main layout
        self.setLayout(self.layout)
        #setting the displayed timer at the top center.
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        #adding border to the displayed time and date.
        self.time_bar.setStyleSheet('border: 2px solid')


    def update_time(self):
        self.time_bar.setText(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


