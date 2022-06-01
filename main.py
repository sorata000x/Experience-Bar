"""
Might Helpful
    Stackoverflow: Creating a pyqt5 text with a gradient color [closed] | https://stackoverflow.com/questions/68152680/creating-a-pyqt5-text-with-a-gradient-color

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
from PyQt6.QtCore import QTimer, QSize, Qt, QPoint, QPropertyAnimation, QEasingCurve, QRectF, QObject, pyqtSignal
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
    QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPalette, QColor, QPainter, QPixmap, QIcon, QTransform, QFont, QLinearGradient, QPen, \
    QTextOption
from widgets import *
from pynput import mouse

import stylesheet
from time import sleep


class ExpBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ----- Level label -----
        self.level_label = QWidget(self)
        self.level_label.setObjectName('LevelLabel')
        self.level_label.setGeometry(0, 0, 70, 30)
        self.text_label = QLabel(self)
        self.text_label.setText('Lv.101')
        self.text_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #f5c722;")
        self.text_label.setGeometry(10, 3, 60, 24)
        # ------- EXP bar -------
        self.exp_bar = QProgressBar(self)
        self.exp_bar.setMinimum(0)
        self.exp_bar.setMaximum(1000)
        self.exp_bar.setObjectName("ExpBar")
        self.exp_bar.setValue(0)
        self.exp_bar.setFormat('')
        self.exp_bar.setGeometry(70, 0, 1250, 30)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
        self.exp_bar.setPalette(palette)
        self.anim = QPropertyAnimation(self.exp_bar, b"value")
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.setDuration(600)
        # ------- Segments --------
        self.segments = Segments(self)
        self.segments.setGeometry(172, 0, 1300, 30)

    def increase(self):
        self.anim.setEndValue(self.exp_bar.value() + 100)
        self.anim.start()
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')

    def decrease(self):
        self.anim.setEndValue(self.exp_bar.value() - 100)
        self.anim.start()
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')


class Segments(QWidget):
    def __init__(self, parent=None):
        super(Segments, self).__init__(parent)
        self.addSegment()

    def addSegment(self):
        for i in range(9):
            segment = QWidget(self)
            segment.setGeometry(i*200, 0, 10, 30)
            black_seg = QWidget(segment)
            black_seg.setStyleSheet("background-color: rgba(150, 150, 150, 100); border-radius: 1px;")
            black_seg.setGeometry(3, 6, 2, 18)


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
        self.exp_bar.setGeometry(10, 0, 1300, 50)

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
        # Window config
        self.setWindowTitle('Option')
        # Sub windows
        # --- Experience bar window
        self.exp_bar_window = ExpBarWindow()
        self.exp_bar_window.show()
        # --- Action window
        self.action_window = ActionWindow()
        self.action_window.show()
        self.action_window.plus_button.clicked.connect(self.exp_bar_window.exp_bar.increase)
        self.action_window.minus_button.clicked.connect(self.exp_bar_window.exp_bar.decrease)
        # --- Area selection window
        self.area_select_window = AreaSelectWindow()
        # Buttons
        # --- Select click area button
        self.define_click_area_button = QPushButton(self)
        self.define_click_area_button.setText('Select Area')
        self.define_click_area_button.setGeometry(10, 10, 100, 30)
        self.define_click_area_button.clicked.connect(self.select_area)
        # --- Quit button
        self.quit_button = QPushButton(self)
        self.quit_button.setText('Quit')
        self.quit_button.setGeometry(10, 50, 70, 30)
        self.quit_button.clicked.connect(self.close)

    # Windows

    def select_area(self):
        self.area_select_window.show()
        app.setOverrideCursor(Qt.CursorShape.CrossCursor)

    # Events

    def closeEvent(self, event):
        self.exp_bar_window.close()
        self.action_window.close()

    def mousePressEvent(self, event):
        print(event.pos().x())


class Signaller(QObject):
    clicked_on_area = pyqtSignal()
    def __init__(self):
        super(Signaller, self).__init__()

    def on_click_area(self):
        self.clicked_on_area.emit()


app = QApplication(sys.argv)
app.setStyleSheet(stylesheet.StyleSheet)
screen_size = app.primaryScreen().size()
# Main window
w = MainWindow()
w.setGeometry(int(screen_size.width()/2 - 100), int(screen_size.height()/2 - 100), 200, 200)
w.exp_bar_window.setGeometry(64, 750, 1365, 44)
w.show()

signaller = Signaller()
signaller.clicked_on_area.connect(w.exp_bar_window.exp_bar.increase)

# detect click on selected area
def on_click(x, y, button, pressed):
    if not pressed:     # on release
        target_start_x = w.area_select_window.selected_area.x()
        target_start_y = w.area_select_window.selected_area.y()
        target_end_x = target_start_x + w.area_select_window.selected_area.width()
        target_end_y = target_start_y + w.area_select_window.selected_area.height()
        if target_start_x <= x <= target_end_x and target_start_y <= y <= target_end_y:
            signaller.on_click_area()


listener = mouse.Listener(on_click=on_click)
listener.start()
# -------

app.exec()


