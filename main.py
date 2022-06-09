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
    - make progress bar text easier to see
    - design option, configuration interface
    - make progress bar more smooth
    - design level and corresponding experience to level up
    - store user info (experience amount, configuration)
"""

import sys
from PyQt6.QtWidgets import QApplication
from windows.main_window import MainWindow
from stylesheet import StyleSheet

import json

def get_data(filename):
    """
    Get data from json file
    :return: json data (dictionary)
    """
    # Opening JSON file
    with open(filename, 'r') as openfile:
        # Reading from json file
        try:
            return json.load(openfile)
        except json.decoder.JSONDecodeError:
            return dict()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)

    config = get_data('info.json')

    w = MainWindow(app, config)

    w.show()
    app.exec()
