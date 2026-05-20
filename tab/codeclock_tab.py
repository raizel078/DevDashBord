from PySide6.QtWidgets import QWidget , QLabel , QVBoxLayout , QTableWidget , QHeaderView , QTableWidgetItem
import datetime
from PySide6.QtCore import QTimer , Qt
from storage.codclock_storage import PyCharm ,save_session


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
        self.end_time = None
        self.base_duration_before_session = datetime.timedelta()

    def _find_date_row(self):
        for i in range(self.table.rowCount()):
            date_item = self.table.item(i, 0)
            if date_item is not None and date_item.text() == str(self.date):
                return i
        return None

    def _get_or_create_date_row(self):
        row = self._find_date_row()
        if row is None:
            row = self.table.rowCount()
            self.table.insertRow(row)
            date_item = QTableWidgetItem(str(self.date))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, date_item)
        return row

    def _parse_duration(self, duration_text):
        if not duration_text:
            return datetime.timedelta()
        hours, minutes, seconds = map(int, duration_text.split(':'))
        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def _format_duration(self, delta):
        total_seconds = int(delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def handle_pycharm(self, text):
        if text == 'open':
            if self.start_time is None:
                self.start_time = datetime.datetime.now()
                row = self._get_or_create_date_row()
                existing_duration_item = self.table.item(row, 2)
                if existing_duration_item is not None:
                    self.base_duration_before_session = self._parse_duration(existing_duration_item.text())
                else:
                    self.base_duration_before_session = datetime.timedelta()
                session_item = QTableWidgetItem(self.start_time.strftime('%H:%M:%S') + '..')
                session_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 1, session_item)

        elif text == 'closed':
            if self.start_time is not None:
                start = self.start_time
                self.start_time = None
                end_time_dt = datetime.datetime.now()
                end_time_str = end_time_dt.strftime("%H:%M:%S")
                session_display = f"{start.strftime('%H:%M:%S')} - {end_time_str}"
                session_item = QTableWidgetItem(session_display)
                session_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row = self._get_or_create_date_row()
                self.table.setItem(row, 1, session_item)
                
                # finalize and accumulate duration for the day
                delta = end_time_dt - start
                total_duration = self.base_duration_before_session + delta
                duration_item = QTableWidgetItem(self._format_duration(total_duration))
                duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 2, duration_item)
                self.base_duration_before_session = total_duration
                
                # Save session
                save_session(str(self.date), session_display, str(delta).split('.')[0])

    def Duration(self,start_time):
        delta = datetime.datetime.now()-self.start_time
        return str(delta).split('.')[0]

    def update_time(self):
        self.time_bar.setText(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        if self.start_time is not None:
            delta = datetime.datetime.now() - self.start_time
            row = self._find_date_row()
            if row is not None:
                live_total = self.base_duration_before_session + delta
                duration_item = QTableWidgetItem(self._format_duration(live_total))
                duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 2, duration_item)







