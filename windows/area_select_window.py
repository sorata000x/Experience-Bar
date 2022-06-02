from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from pynput import mouse

class AreaSelectWindow(QWidget):
    def __init__(self, connect_to, app, parent=None):
        super().__init__(parent)
        # Variable init
        self.app = app
        self.start_x, self.start_y = 0, 0
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        # Select area
        self.selected_area = QWidget(self)
        self.selected_area.setObjectName('SelectedArea')
        # Detect click on screen
        signaller = self.Signaller()
        signaller.clicked_on_area.connect(connect_to)

        def on_click(x, y, button, pressed):
            if not pressed:  # on release
                target_start_x = self.selected_area.x()
                target_start_y = self.selected_area.y()
                target_end_x = target_start_x + self.selected_area.width()
                target_end_y = target_start_y + self.selected_area.height()
                if target_start_x <= x <= target_end_x and target_start_y <= y <= target_end_y:
                    signaller.on_click_area()

        listener = mouse.Listener(on_click=on_click)
        listener.start()

    def mousePressEvent(self, event):
        self.start_x, self.start_y = event.pos().x(), event.pos().y()

    def mouseMoveEvent(self, event):
        width, height = abs(event.pos().x() - self.start_x), abs(event.pos().y() - self.start_y)
        if event.pos().x() >= self.start_x and event.pos().y() >= self.start_y:
            self.selected_area.setGeometry(self.start_x, self.start_y, width, height)
        elif event.pos().x() >= self.start_x and event.pos().y() <= self.start_y:
            self.selected_area.setGeometry(self.start_x, event.pos().y(), width, height)
        elif event.pos().x() <= self.start_x and event.pos().y() >= self.start_y:
            self.selected_area.setGeometry(event.pos().x(), self.start_y, width, height)
        elif event.pos().x() <= self.start_x and event.pos().y() <= self.start_y:
            self.selected_area.setGeometry(event.pos().x(), event.pos().y(), width, height)

    def mouseReleaseEvent(self, event):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def close(self):
        self.app.restoreOverrideCursor()
        super().close()

    def show(self):
        self.selected_area.setGeometry(0, 0, 0, 0)
        super().show()

    class Signaller(QObject):
        clicked_on_area = pyqtSignal()

        def __init__(self):
            super().__init__()

        def on_click_area(self):
            self.clicked_on_area.emit()

