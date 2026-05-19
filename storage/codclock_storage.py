import time
from PySide6.QtCore import QThread , Signal
import psutil
#code for the checking, logic goes below

def check_date(table, date):
    for i in range(table.rowCount()):
        if table.item(i,0).text() ==str(date):
            return True
    return None

def is_pycharm_running():
    for process in psutil.process_iter():
        if 'pycharm' in process.name().lower():
            return True
    return False


class PyCharm(QThread):
    pycharm_signal = Signal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            if is_pycharm_running():
                self.pycharm_signal.emit(f'open')
            else:
                self.pycharm_signal.emit('closed')
            time.sleep(2)

        


