import time
import json

from PySide6.QtCore import QThread , Signal
import psutil
from pathlib import Path
#code for the checking, logic goes below
json_path = Path('/home/nowa/Desktop/new ML/sessions.json')


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
        last_state = None
        while True:
            current_running = is_pycharm_running()
            if current_running and last_state != 'open':
                self.pycharm_signal.emit('open')
                last_state = 'open'
            elif not current_running and last_state != 'closed':
                self.pycharm_signal.emit('closed')
                last_state = 'closed'
            time.sleep(2)

def save_session(date, session, duration):
    if not json_path.exists():
        with open(json_path, 'w') as f:
            json.dump([], f)
    with open(json_path, 'r') as f:
        data = json.load(f)
    data.append({
        'date': date,
        'session': session,
        'duration': duration
    })
    with open(json_path, 'w') as f:
        json.dump(data, f)






