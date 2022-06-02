StyleSheet = '''
#ExpBar {
    text-align: center;
    background-color: rgba(0, 0, 0, 100);
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
#ExpBar::chunk {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #e8fa48,
                                stop: 0.5 #cfe600,
                                stop: 0.6 #cfe600,
                                stop: 1 #e8fa48       
                                );
    margin: 6px;
    border-radius: 5px;
}

#ExpLabel {
    text-align: center;
    background-color: rgba(0, 0, 0, 100);
    border-radius: 0px;
}

#LevelLabel {
    text-align: center;
    background-color: rgba(0, 0, 0, 100);
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}

#Overlay {
    text-align: center;
    background-color: rgba(0, 0, 0, 60);
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}

#Overlay2 {
    text-align: center;
    background-color: #e8fa48;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}




#PlusButton {
    background-color: #a3d13f;
    border-radius: 6px;

    border-bottom: 4px solid #8aad3d;

    font-size: 20px;
    font-weight: bold;
}
#PlusButton:pressed {
    background-color: #94b840;
    border: 0px;
}

#MinusButton {
    background-color: #d1d1d1;
    border-radius: 6px;
    border-bottom: 4px solid #adadad;
    font-size: 20px;
    font-weight: bold;
}
#MinusButton:pressed {
    background-color: #b8b8b8;
    border: 0px;
}

#ActionWindow {
    background-color: rgba(0, 0, 0, 100);
    border-radius: 5px;
}

#ActionWindowToggle {
    background-color: rgba(0, 0, 0, 100);
    border-top-left-radius: 5px;
    border-bottom-left-radius: 8px;
}

QWidget#SelectedArea {
    background-color: rgba(0, 0, 0, 200);
}

QPushButton#OptionButton {
    background-color: rgb(255, 255, 255);
    border-radius: 8px;
    border: 1px solid black;
}

QPushButton#OptionButton:hover {
    border-radius: 8px;
    border: 2px solid blue;
}
'''