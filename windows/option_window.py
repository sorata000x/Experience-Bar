from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QSpinBox


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
        # Buttons
        # --- Select click area button
        self.define_click_area_button = QPushButton(self)
        self.define_click_area_button.setObjectName('OptionButton')
        self.define_click_area_button.setText('Select Area')
        self.define_click_area_button.resize(100, 30)
        self.define_click_area_button.setGeometry(50, 30, 100, 30)
        self.define_click_area_button.clicked.connect(self.select_area)
        # --- Quit button
        self.quit_button = QPushButton(self)
        self.quit_button.setObjectName('OptionButton')
        self.quit_button.setText('Quit')
        self.quit_button.setGeometry(65, 80, 70, 30)
        self.quit_button.clicked.connect(self.close)
        # --- Set Level
        self.level_label = QLabel(self)
        self.level_label.setText('Level: ')
        self.level_label.setGeometry(30, 130, 70, 30)
        self.level_edit = QLineEdit(self)
        # self.level_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{3}")))
        self.level_edit.setValidator(QIntValidator(1, 999))
        self.level_edit.setText(str(self.exp_bar_window.exp_bar.level))
        self.level_edit.setGeometry(80, 130, 30, 30)
        self.level_edit.setEnabled(False)
        self.level_edit.returnPressed.connect(
            lambda: self.exp_bar_window.exp_bar.setLevel(int(self.level_edit.text())))

        # self.level_spin_box = QSpinBox(self)
        # self.level_spin_box.move(80, 130)
        # self.level_spin_box.setMaximum(999)
        # self.level_spin_box.setMinimum(1)
        # self.level_spin_box.setValue(self.exp_bar_window.exp_bar.level)
        # self.level_spin_box.valueChanged.connect(lambda: self.exp_bar_window.exp_bar.setLevel(self.level_spin_box.value()))
        # --- Set Value
        self.value_label = QLabel(self)
        self.value_label.setText('Value')
        self.value_label.setGeometry(30, 170, 70, 30)
        self.value_spin_box = QSpinBox(self)
        self.value_spin_box.setGeometry(80, 170, 70, 30)
        self.value_spin_box.setMaximum(self.exp_bar_window.exp_bar.exp_bar.maximum() - 1)
        self.value_spin_box.setMinimum(self.exp_bar_window.exp_bar.exp_bar.minimum())
        self.value_spin_box.setValue(self.exp_bar_window.exp_bar.value)
        self.value_spin_box.valueChanged.connect(
            lambda: self.exp_bar_window.exp_bar.setValue(self.value_spin_box.value()))
        self.value_percentage_spin_box = QSpinBox(self)
        self.value_percentage_spin_box.setGeometry(160, 170, 50, 30)
        self.value_percentage_label = QLabel(self)
        self.value_percentage_label.setText('%')
        self.value_percentage_label.move(210, 170)
        # --- Increase Value
        self.increase_amount_label = QLabel(self)
        self.increase_amount_label.setText('Increase')
        self.increase_amount_label.move(30, 210)
        self.increase_amount_box = QLineEdit(self)
        self.increase_amount_box.setText(str(self.exp_bar_window.exp_bar.increase_amount))
        self.increase_amount_box.setGeometry(100, 210, 50, 30)
        self.increase_amount_box.textChanged.connect(
            lambda: self.exp_bar_window.exp_bar.setIncreaseAmount(int(self.increase_amount_box.text())))

    def select_area(self):
        self.area_select_window.show()
        self.app.setOverrideCursor(Qt.CursorShape.CrossCursor)

    def closeEvent(self, event):
        self.exp_bar_window.close()
        self.action_window.close()
        self.skill_window.close()
