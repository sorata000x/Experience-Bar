from PyQt6.QtCore import QObject, pyqtSignal

class Signaller(QObject):
    clicked_on_area = pyqtSignal()

    def __init__(self):
        super(Signaller, self).__init__()

    def on_click_area(self):
        self.clicked_on_area.emit()
