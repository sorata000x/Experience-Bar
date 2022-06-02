from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import Qt
from windows.exp_bar_window import ExpBarWindow
from windows.action_window import ActionWindow
from windows.area_select_window import AreaSelectWindow

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        # Variable init
        self.app = app
        # Window config
        self.setWindowTitle('Option')
        screen_size = app.primaryScreen().size()
        self.setGeometry(int(screen_size.width()/2 - 100), int(screen_size.height()/2 - 100), 200, 200)
        # Sub windows
        # --- Experience bar window
        self.exp_bar_window = ExpBarWindow()
        self.exp_bar_window.setGeometry(64, 750, 1365, 44)
        self.exp_bar_window.show()
        # --- Action window
        self.action_window = ActionWindow()
        self.action_window.show()
        self.action_window.plus_button.clicked.connect(self.exp_bar_window.exp_bar.increase)
        self.action_window.minus_button.clicked.connect(self.exp_bar_window.exp_bar.decrease)
        # --- Area selection window
        self.area_select_window = AreaSelectWindow(self.exp_bar_window.exp_bar.increase, app)
        self.area_select_window.setGeometry(0, 0, screen_size.width(), screen_size.height())
        # Buttons
        # --- Select click area button
        self.define_click_area_button = QPushButton(self)
        self.define_click_area_button.setObjectName('OptionButton')
        self.define_click_area_button.setText('Select Area')
        self.define_click_area_button.resize(100, 30)
        self.define_click_area_button.setGeometry(50, 30, 100, 30)
        print(self.define_click_area_button.geometry())
        self.define_click_area_button.clicked.connect(self.select_area)
        # --- Quit button
        self.quit_button = QPushButton(self)
        self.quit_button.setObjectName('OptionButton')
        self.quit_button.setText('Quit')
        self.quit_button.setGeometry(65, 80, 70, 30)
        self.quit_button.clicked.connect(self.close)

    # Windows

    def select_area(self):
        self.area_select_window.show()
        self.app.setOverrideCursor(Qt.CursorShape.CrossCursor)

    # Events

    def closeEvent(self, event):
        self.exp_bar_window.close()
        self.action_window.close()

    def mousePressEvent(self, event):
        print(event.pos().x())