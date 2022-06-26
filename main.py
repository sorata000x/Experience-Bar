"""
Doing
    -

To Do
    - design option, setting interface
    - make progress bar more smooth
    - design level and corresponding experience to level up
    - consider make an option/setting window instead of put in main window class
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from stylesheet import StyleSheet
from windows.exp_bar_window import ExpBarWindow
from windows.action_window import ActionWindow
from windows.area_select_window import AreaSelectWindow
from windows.skill_window import SkillWindow
from windows.option_window import OptionWindow

debug = True

def start_windows(app, setting):
    screen_size = app.primaryScreen().size()
    # External Windows
    # --- Experience bar window
    exp_bar_window = ExpBarWindow(setting)
    # self.exp_bar_window.setGeometry(64, 750, 1365, 44)
    exp_bar_window.show()
    # --- Action window
    action_window = ActionWindow()
    action_window.show()
    action_window.plus_button.clicked.connect(lambda: exp_bar_window.exp_bar.increase())
    action_window.minus_button.clicked.connect(lambda: exp_bar_window.exp_bar.decrease())
    # --- Area selection window
    area_select_window = AreaSelectWindow(lambda: exp_bar_window.exp_bar.increase(), app)
    area_select_window.setGeometry(0, 0, screen_size.width(), screen_size.height())
    # --- Skill Window
    skill_window = SkillWindow()
    skill_window.show()
    # --- Option Window
    windows = {
        'exp_bar_window': exp_bar_window,
        'action_window': action_window,
        'area_select_window': area_select_window,
        'skill_window': skill_window,
    }
    option_window = OptionWindow(app, windows)
    option_window.setGeometry(int(screen_size.width() / 2 - 100), int(screen_size.height() / 2 - 100), 250, 300)
    option_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)

    # config = get_data('info.json')
    setting = QSettings('Game Logic', 'exp_bar')

    if debug:
        print(setting.fileName())

    start_windows(app, setting)

    app.exec()
