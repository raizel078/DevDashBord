from PySide6.QtWidgets import QWidget , QLabel , QVBoxLayout , QTableWidget , QHeaderView , QTableWidgetItem
import datetime
from PySide6.QtCore import QTimer , Qt

from storage.codclock_storage import check_date ,PyCharm
#now main ui code goes here,
class CodeClock(QWidget):
    def __init__(self):
        super().__init__()
        #for the real-time show. on tab clock
        self.time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.date = datetime.date.today()
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


        #capture the signal.
        self.pycharm_thread = PyCharm()
        self.pycharm_thread.pycharm_signal.connect(self.handle_pycharm)
        self.pycharm_thread.start()
        #now timer to record the start and end time.
        self.start_time =None

    def handle_pycharm(self, text):
        if text =='open' and self.end_time is None:
            self.start_time = datetime.datetime.now()
            if not check_date(self.table, self.date):
                self.table.insertRow(0)

                date_item = QTableWidgetItem(str(self.date))
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, date_item)

                session_item = QTableWidgetItem(self.start_time.strftime('%H:%M:%S') + ' -..')
                session_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 1, session_item)

                #duration column will do here.

        elif text =='closed':
            pass



    def update_time(self):
        self.time_bar.setText(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))



