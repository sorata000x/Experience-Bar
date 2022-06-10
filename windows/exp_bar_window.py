from PyQt6.QtWidgets import QWidget, QLabel, QProgressBar, QAbstractButton
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QPalette, QColor, QPainter

class ExpBarWindow(QWidget):
    def __init__(self, settings):
        super().__init__()
        # Variable init
        self.settings = settings
        self.offset = self.pos()
        self.timer = QTimer()
        # Window config
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # set background transparent
        self.resize(1365, 44)
        self.move(self.settings.value('exp_bar_window_pos_x', 64), self.settings.value('exp_bar_window_pos_y', 750))
        # Close button
        icon = QPixmap('close_button.png')
        self.button = self.PicButton(icon, self)
        self.button.clicked.connect(self.close)
        self.button.setGeometry(1306, 14, 16, 16)
        self.button.close()
        # Exp bar
        self.exp_bar = ExpBar(settings, parent=self)
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
        # Update settings
        self.settings.setValue('exp_bar_window_pos_x', mx)
        self.settings.setValue('exp_bar_window_pos_y', my)

    def leaveEvent(self, event):
        """ Purpose: hide close button after leave for 3 seconds """
        if self.button.isVisible():
            self.timer.timeout.connect(lambda: self.button.close())
            self.timer.start(3000)

    def mouseDoubleClickEvent(self, event):
        """ Purpose: show close button """
        if not self.button.isVisible():
            self.button.show()

    class PicButton(QAbstractButton):
        def __init__(self, pixmap, parent=None):
            super().__init__(parent)
            self.pixmap = pixmap

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.drawPixmap(event.rect(), self.pixmap)

        def sizeHint(self):
            return self.pixmap.size()

class ExpBar(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        # ---- Init variable ----
        self.settings = settings
        self.value = settings.value('value', 0)
        self.level = settings.value('level', 1)
        # ----- Level label -----
        self.level_label = QWidget(self)
        self.level_label.setObjectName('LevelLabel')
        self.level_label.setGeometry(0, 0, 70, 30)
        self.text_label = QLabel(self)
        # ------ EXP bar --------
        self.exp_bar = QProgressBar(self)
        self.exp_bar.setMinimum(0)
        self.exp_bar.setMaximum(1000)
        self.exp_bar.setObjectName("ExpBar")
        self.exp_bar.setFormat('')
        self.exp_bar.setGeometry(70, 0, 1200, 30)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
        self.exp_bar.setPalette(palette)
        self.anim = QPropertyAnimation(self.exp_bar, b"value")
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.setDuration(600)
        # ------- Segments --------
        self.segments = Segments(self)
        self.segments.setGeometry(172, 0, 1300, 30)
        # ------- Settings --------
        self.setValue(settings.value('value', 0))
        self.setLevel(settings.value('level', 1))

    def increase(self):
        if self.anim.state() == QPropertyAnimation.State.Stopped:   # wait for previous animation complete
            newValue = self.exp_bar.value() + 120 if self.exp_bar.value() + 120 < self.exp_bar.maximum() else self.exp_bar.maximum()
            # Set new value label
            percentage = newValue / self.exp_bar.maximum() * 100
            self.exp_bar.setFormat(f'{self.exp_bar.value() + 100} [{percentage:.2f}%]')
            # Progress increase animation
            self.anim.setEndValue(newValue)
            self.anim.start()
            if newValue == self.exp_bar.maximum():
                self.anim.finished.connect(self.levelUp)
            else:
                # Update setting
                self.settings.setValue('value', newValue)

    def levelUp(self):
        self.setValue(0)
        self.setLevel(self.level + 1)
        self.anim.disconnect()

    def decrease(self):
        if self.anim.state() == QPropertyAnimation.State.Stopped:   # wait for previous animation complete
            newValue = self.exp_bar.value() - 100
            # Set new value label
            percentage = newValue / self.exp_bar.maximum() * 100
            self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')
            # Progress increase animation
            self.anim.setEndValue(newValue)
            self.anim.start()
            # Update setting
            self.settings.setValue('value', newValue)

    def setValue(self, value):
        self.exp_bar.setValue(value)
        percentage = self.exp_bar.value() / self.exp_bar.maximum() * 100
        self.exp_bar.setFormat(f'{self.exp_bar.value()} [{percentage:.2f}%]')
        # Update setting
        self.settings.setValue('value', value)

    def setLevel(self, level):
        self.level = level
        self.text_label.setText(f'Lv. {level}')
        self.text_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #f5c722;")
        text_width = self.text_label.fontMetrics().boundingRect(self.text_label.text()).width()
        self.text_label.move(int(30 - text_width / 2), 3)
        # Update setting
        self.settings.setValue('level', level)

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

