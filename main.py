"""
Package
    PyQt6
    Pynput
        note: need to grant accessibility and input monitoring in mac

Doing
    - change progress bar effect

To Do
    - organize code
    - design option, configuration interface
    - progress bar overlay
"""

import sys
from PyQt6.QtCore import QTimer, QSize, Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QStackedLayout,
    QGridLayout,
    QToolButton,
)
from PyQt6.QtGui import QPalette, QColor, QPainter, QPixmap, QIcon, QTransform
from widgets import *
from pynput import mouse

import stylesheet


class ExpBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # EXP label
        self.exp_label = ProgressBar(self, objectName="ExpLabel")
        self.exp_label.setGeometry(0, 0, 40, 24)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor(250, 250, 250))
        self.exp_label.setPalette(palette)
        self.text_label = QLabel(self)
        self.text_label.setText('EXP')
        self.text_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white;")
        self.text_label.setGeometry(7, 0, 40, 24)
        # EXP bar
        self.exp_bar = ProgressBar(self, minimum=0, maximum=1000, objectName="ExpBar")
        self.exp_bar.setValue(400)
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')
        self.exp_bar.setGeometry(40, 0, 1250, 24)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
        self.exp_bar.setPalette(palette)

    def increase(self):
        self.exp_bar.setValue(self.exp_bar.value() + 10)
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')

    def decrease(self):
        self.exp_bar.setValue(self.exp_bar.value() - 10)
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')


class ExpBarWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Variable init
        self.offset = self.pos()
        self.timer = QTimer()
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        # Close button
        icon = QPixmap('close_button.png')
        self.button = PicButton(icon, self)
        self.button.clicked.connect(self.close)
        self.button.setGeometry(1306, 14, 16, 16)
        self.button.close()
        # Exp bar
        self.exp_bar = ExpBar(self)
        self.exp_bar.setGeometry(10, 10, 1300, 24)

    def mousePressEvent(self, event):
        """ Purpose: dragging window, close (hide) button. """
        self.offset = event.pos()   # for dragging window
        if self.button.isVisible():
            self.button.close()

    def mouseMoveEvent(self, event):
        """ Purpose: dragging window """
        x = event.globalPosition().x()
        y = event.globalPosition().y()
        x_w = self.offset.x()
        y_w = self.offset.y()
        mx = int(x-x_w)
        my = int(y-y_w)
        self.move(mx, my)

    def leaveEvent(self, event):
        """ Purpose: hide close button after leave for 3 seconds """
        if self.button.isVisible():
            self.timer.timeout.connect(lambda: self.button.close())
            self.timer.start(3000)

    def mouseDoubleClickEvent(self, event):
        """ Purpose: show close button """
        if not self.button.isVisible():
            self.button.show()


class ActionWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Variable init
        self.offset = self.pos()
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        # Button
        self.container = QWidget(self)
        self.container.setObjectName('ActionWindow')
        self.container.setGeometry(0, 0, 90, 150)

        self.plus_button = QPushButton(self.container)
        self.plus_button.setObjectName('PlusButton')
        icon = QIcon('up_arrow_white.png')
        self.plus_button.setIcon(icon)
        self.plus_button.setIconSize(QSize(60, 60))
        self.plus_button.setGeometry(20, 20, 50, 50)

        self.minus_button = QPushButton(self.container)
        self.minus_button.setObjectName('MinusButton')
        icon = QIcon('down_arrow.png')
        self.minus_button.setIcon(icon)
        self.minus_button.setIconSize(QSize(60, 60))
        self.minus_button.setGeometry(20, 80, 50, 50)

        self.setGeometry(100, 100, 90, 150)

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


class AreaSelectWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Variable init
        self.start_x, self.start_y = 0, 0
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())
        # Select area
        self.selected_area = QWidget(self)
        self.selected_area.setObjectName('SelectedArea')

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
        app.restoreOverrideCursor()
        super().close()

    def show(self):
        self.selected_area.setGeometry(0, 0, 0, 0)
        super().show()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_bar_window = ExpBarWindow()
        self.exp_bar_window.show()
        self.action_window = ActionWindow()
        self.action_window.show()
        self.action_window.plus_button.clicked.connect(self.exp_bar_window.exp_bar.increase)
        self.action_window.minus_button.clicked.connect(self.exp_bar_window.exp_bar.decrease)

        self.area_select_window = AreaSelectWindow()

        self.define_click_area_button = QPushButton(self)
        self.define_click_area_button.setText('Select')
        self.define_click_area_button.setGeometry(10, 10, 70, 30)
        self.define_click_area_button.clicked.connect(self.select_area)

    def closeEvent(self, event):
        self.exp_bar_window.close()
        self.action_window.close()

    def mousePressEvent(self, event):
        print(event.pos().x())

    def select_area(self):
        self.area_select_window.show()
        app.setOverrideCursor(Qt.CursorShape.CrossCursor)


app = QApplication(sys.argv)
app.setStyleSheet(stylesheet.StyleSheet)
screen_size = app.primaryScreen().size()
w = MainWindow()


# not using
eb_width = 1250
eb_height = 50
eb_x = int(screen_size.width() / 2 - eb_width / 2)
eb_y = 700

w.exp_bar_window.setGeometry(64, 780, 1365, 44)

w.show()

# detect click on selected area
def on_click(x, y, button, pressed):
    if not pressed:     # on release
        target_start_x = w.area_select_window.selected_area.x()
        target_start_y = w.area_select_window.selected_area.y()
        target_end_x = target_start_x + w.area_select_window.selected_area.width()
        target_end_y = target_start_y + w.area_select_window.selected_area.height()
        if target_start_x <= x <= target_end_x and target_start_y <= y <= target_end_y:
            w.exp_bar_window.exp_bar.increase()


listener = mouse.Listener(on_click=on_click)
listener.start()
# -------

app.exec()


