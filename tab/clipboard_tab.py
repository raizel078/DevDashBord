from PySide6.QtWidgets import QWidget , QVBoxLayout , QApplication , QListWidget, QPushButton



class ClipBoard(QWidget):
    def __init__(self):
        super().__init__()
        #layout to show in UI
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #now taking the clipboard monitor.
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self._on_clipboard_changed)

        #now Qlist to add the copied item
        self.list = QListWidget()
        self.layout.addWidget(self.list)

        # explicit copy action for selected history item
        self.copy_button = QPushButton('📋 Copy Selected')
        self.copy_button.clicked.connect(self.copy_selected_item)
        self.layout.addWidget(self.copy_button)

        #now copy from clipboard.
        self.list.itemDoubleClicked.connect(self.copy_item)

        # load current clipboard text when tab opens
        self._on_clipboard_changed()

    def copy_item(self, item):
        text = item.text()
        if not text:
            return
        if self.clipboard.text() == text:
            return
        self.clipboard.setText(text)

    def copy_selected_item(self):
        item = self.list.currentItem()
        if item is None:
            return
        self.copy_item(item)

    def _on_clipboard_changed(self):
        text = self.clipboard.text(mode=self.clipboard.Mode.Clipboard)
        self.handle_clipboard(text)
    
    def handle_clipboard(self, text):
        if not text:
            return
        for i in range(self.list.count()):
            if self.list.item(i).text() == text:
                return
        self.list.insertItem(0, text)
        self.list.setStyleSheet("""
            QListWidget::item {
                border: 1px solid gray;
                padding: 4px;
                margin: 2px;
            }
        """)

    def closeEvent(self, event):
        self.clipboard.dataChanged.disconnect(self._on_clipboard_changed)
        super().closeEvent(event)




