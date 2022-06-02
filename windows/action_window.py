from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
from PyQt6.QtCore import QPropertyAnimation, Qt, QPoint, QSize, QObject, pyqtSignal
from PyQt6.QtGui import QIcon

class ActionWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Variable init
        self.offset = self.pos()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(600)
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.setGeometry(1424, 250, 90, 150)
        # Panel
        self.panel = QWidget(self)
        self.panel.setObjectName('ActionWindow')
        self.panel.setGeometry(10, 0, 90, 150)

        # Toggle
        self.toggle = QWidget(self)
        self.toggle.setObjectName('ActionWindowToggle')
        self.toggle.setGeometry(0, 0, 12, 150)
        def mouseMoveEvent(event):
            self.anim.setEndValue(QPoint(1350, 250))
            self.anim.start()
            self.toggle.hide()
        def enterEvent(event):
            self.setGeometry(1350, 250, 90, 150)
            self.toggle.hide()
        self.toggle.mouseMoveEvent = mouseMoveEvent
        self.toggle.enterEvent = enterEvent
        def leaveEvent(event):
            self.setGeometry(1424, 250, 90, 150)
            self.toggle.show()
        self.leaveEvent = leaveEvent
        self.toggle.setMouseTracking(True)
        label = QLabel(self.toggle)
        label.setText('〈')
        label.setStyleSheet("font-size: 18pt; color: #fff")
        label.setGeometry(-6, 60, 30, 30)

        # Button
        self.plus_button = QPushButton(self.panel)
        self.plus_button.setObjectName('PlusButton')
        icon = QIcon('image/up_arrow_white.png')
        self.plus_button.setIcon(icon)
        self.plus_button.setIconSize(QSize(60, 60))
        self.plus_button.setGeometry(20, 20, 50, 50)

        self.minus_button = QPushButton(self.panel)
        self.minus_button.setObjectName('MinusButton')
        icon = QIcon('image/down_arrow.png')
        self.minus_button.setIcon(icon)
        self.minus_button.setIconSize(QSize(60, 60))
        self.minus_button.setGeometry(20, 80, 50, 50)

    def mousePressEvent(self, event):
        """ Purpose: dragging window, close (hide) button. """
        self.offset = event.pos()   # for dragging window

    def mouseMoveEvent(self, event):
        """ Purpose: dragging window """
        x = event.globalPosition().x()
        y = event.globalPosition().y()
        x_w = self.offset.x()
        y_w = self.offset.y()
        mx = int(x-x_w)
        my = int(y-y_w)
        self.move(mx, my)

    class Signaller(QObject):
        window_out = pyqtSignal()
        window_in = pyqtSignal()

        def __init__(self):
            super().__init__()

        def pop_window(self):
            self.window_out.emit()

        def shrink_window(self):
            self.window_in.emit()
