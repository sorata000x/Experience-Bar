from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QSpinBox, QSlider, QTabWidget, QTabBar, \
    QStylePainter, QStyleOptionTab, QStyle, QProxyStyle


class OptionWindow(QWidget):
    def __init__(self, app, windows, parent=None):
        super().__init__(parent)
        # Variable Init
        self.app = app
        self.windows = windows
        self.exp_bar_window = windows['exp_bar_window']
        self.action_window = windows['action_window']
        self.area_select_window = windows['area_select_window']
        self.skill_window = windows['skill_window']
        # Window config
        self.setWindowTitle('Option')
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(400, 300)
        # Select click area button
        #self.define_click_area_button = QPushButton(self)
        #self.define_click_area_button.setObjectName('OptionButton')
        #self.define_click_area_button.setText('Select Area')
        #self.define_click_area_button.setGeometry(50, 30, 100, 30)
        #self.define_click_area_button.clicked.connect(self.select_area)
        # Quit button
        #self.quit_button = QPushButton(self)
        #self.quit_button.setObjectName('OptionButton')
        #self.quit_button.setText('Quit')
        #self.quit_button.setGeometry(65, 80, 70, 30)
        #self.quit_button.clicked.connect(self.close)

        # Tab
        self.tab = QTabWidget(self)
        self.tab.resize(400, 250)
        self.tab.setTabBar(HorizontalTabBar())
        self.tab.setTabPosition(QTabWidget.TabPosition.West)

        self.exp_bar_tab = QWidget()
        # Set Level
        # --- label
        self.level_label = QLabel('Level: ', self.exp_bar_tab)
        self.level_label.setGeometry(30, 130, 70, 30)
        # --- edit
        self.level_edit = QLineEdit(self.exp_bar_tab)
        self.level_edit.setValidator(QIntValidator(1, 999))
        self.level_edit.setText(str(self.exp_bar_window.exp_bar.level))
        self.level_edit.setGeometry(80, 130, 30, 30)
        self.level_edit.setEnabled(False)
        # --- note
        self.level_note = QLabel(
            f'({self.exp_bar_window.MIN_LEVEL}-{self.exp_bar_window.MAX_LEVEL})', self.exp_bar_tab)
        self.level_note.setGeometry(120, 130, 70, 30)
        # Set Experience
        # --- label
        self.experience_label = QLabel('Experience: ', self.exp_bar_tab)
        self.experience_label.setGeometry(30, 170, 70, 30)
        # --- slider
        self.experience_slider = QSlider(Qt.Orientation.Horizontal, self.exp_bar_tab)
        self.experience_slider.setValue(self.exp_bar_window.exp_bar.value)
        self.experience_slider.setMaximum(self.exp_bar_window.exp_bar.exp_bar.maximum())
        self.experience_slider.move(110, 170)

        self.action_tab = QWidget()
        # --- Increase Experience By
        self.increase_by_label = QLabel(self.action_tab)
        self.increase_by_label.setText('Increase by: ')
        self.increase_by_label.move(30, 210)
        self.increase_by_edit = QLineEdit(self.action_tab)
        self.increase_by_edit.setText(str(self.exp_bar_window.exp_bar.increase_amount))
        self.increase_by_edit.setGeometry(100, 210, 50, 30)

        self.tab.addTab(self.exp_bar_tab, 'EXP BAR')
        self.tab.addTab(self.action_tab, 'ACTION')

        # OK Button
        self.ok_button = QPushButton('OK', self)
        self.ok_button.move(30, 250)
        self.ok_button.clicked.connect(self.apply_setting)
        # Cancel

    def select_area(self):
        self.area_select_window.show()
        self.app.setOverrideCursor(Qt.CursorShape.CrossCursor)

    def closeEvent(self, event):
        self.exp_bar_window.close()
        self.action_window.close()
        self.skill_window.close()

    def apply_setting(self):
        self.exp_bar_window.exp_bar.setLevel(int(self.level_edit.text()))
        self.exp_bar_window.exp_bar.setValue(self.experience_slider.value())
        self.exp_bar_window.exp_bar.setIncreaseAmount(int(self.increase_by_edit.text()))

class HorizontalTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
            QTabBar::tab { height: 100px; width: 100px; background-color: grey; }
            QTabBar::tab:selected { background-color: white; }''')
    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.ControlElement.CE_TabBarTabShape, option)
            painter.drawText(self.tabRect(index),
                             Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextDontClip,
                             self.tabText(index))

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        if size.width() < size.height():
            size.transpose()
        return size
