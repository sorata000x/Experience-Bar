"""
Might Helpful
    Stackoverflow: Creating a pyqt5 text with a gradient color [closed] | https://stackoverflow.com/questions/68152680/creating-a-pyqt5-text-with-a-gradient-color

Package
    PyQt6
    Pynput
        note: need to grant accessibility and input monitoring in mac

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
from windows.main_window import MainWindow
from stylesheet import StyleSheet

debug = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)

    # config = get_data('info.json')
    setting = QSettings('Game Logic', 'exp_bar')

    if debug:
        print(setting.fileName())

    w = MainWindow(app, setting)

    w.show()
    app.exec()
