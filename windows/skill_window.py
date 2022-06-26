from PyQt6.QtCore import Qt, QSize, QLine
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QListWidget, QListWidgetItem, \
    QAbstractItemView, QButtonGroup, QScrollBar, QDialog, QInputDialog, QLabel, QLineEdit


class SkillWindow(QWidget):
    def __init__(self):
        super(SkillWindow, self).__init__()
        self.setGeometry(900, 250, 250, 350)
        self.scroll_area = QListWidget(self)
        self.scroll_area.setLayout(QVBoxLayout())
        self.scroll_area.resize(250, 300)
        self.scroll_area.setStyleSheet('''QListView::item:selected { background-color: white; }''')
        self.scroll_area.setSpacing(5)
        self.scroll_area.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)


        #self.skill1 = QPushButton(self.scroll_area)
        #self.skill1.setText('JavaScript   Lv.5')
        #self.skill1.setGeometry(10, 10, 230, 50)
        self.setWindowTitle('Skill')
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        #self.skills.append(self.skill1)

        self.skill_button_group = QButtonGroup()

        self.create_button = QPushButton(self)
        self.create_button.setGeometry(10, 300, 220, 50)
        self.create_button.setText('+ Create')
        input_box = self.InputDialog(self, self.addSkill)
        self.create_button.clicked.connect(lambda: input_box.show())

        '''
        self.addSkill('Skill2')
        self.addSkill('Skill3')
        self.addSkill('Skill4')
        self.addSkill('Skill5')
        self.addSkill('Skill6')
        self.addSkill('Skill7')
        '''
        #self.greyOut()

        self.dialog = self.InputDialog(self)


    def greyOut(self):
        cover = QWidget(self)
        cover.setGeometry(0, 0, 250, 350)
        cover.setStyleSheet('background-color: rgba(100, 100, 100, 50)')

    def addSkill(self, name):
        #user_input = QInputDialog(self)
        #user_input.exec()

        #self.dialog.getText('Skill name')

        #name = dialog.getText(self, 'input', 'Skill name: ')[0]

        newSkill = self.Skill(name, self)
        self.skill_button_group.addButton(newSkill.button)
        self.scroll_area.addItem(newSkill.item)
        self.scroll_area.setItemWidget(newSkill.item, newSkill.button)

    class Skill(QPushButton):
        def __init__(self, name, window=None):
            super().__init__()
            self.name = name
            self.level = 1
            # GUI
            self.item = QListWidgetItem()
            self.item.setSizeHint(QSize(220, 50))
            self.item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.button = QPushButton()
            self.button.setText(f'{self.name}   Lv. {self.level}')
            self.button.setStyleSheet('''
                        QPushButton {
                            border: 1px solid black; border-radius: 5px; 
                        }
                        QPushButton::pressed {
                            background-color: grey;
                        }
                        QPushButton::checked {
                            background-color: yellow;
                        }
                        ''')
            self.button.setCheckable(True)

    class InputDialog(QWidget):
        def __init__(self, parent=None, connect_to=None):
            super().__init__(parent)

            background = QWidget(self)
            background.setStyleSheet('background-color: rgba(0, 0, 0, 70)')
            background.setGeometry(0, 0, 250, 350)

            dialog = QWidget(self)
            dialog.setStyleSheet('background-color: white; border-radius: 10px;')
            dialog.setGeometry(15, 110, 220, 80)

            self.label = QLabel(dialog)
            self.label.setText('Skill name')
            self.label.move(15, 18)

            self.input_box = QLineEdit(dialog)
            self.input_box.setStyleSheet('border: 1px solid rgb(150, 150, 150); border-radius: 2px;')
            self.input_box.setGeometry(15, 38, 190, 24)
            self.input_box.returnPressed.connect(lambda: connect_to(self.input_box.text()))
            self.input_box.returnPressed.connect(self.close)
            self.input_box.returnPressed.connect(self.input_box.clear)

            #self.setGeometry(10, 10, 200, 200)
            self.label.setText('New Skill Name')

            self.hide()

        def getText(self, message):
            self.show()
