from ctypes import alignment
import os
import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import tweaker
from tweaker import POSITION

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        global selectedPosition
        selectedPosition = POSITION.BOTTOM
        self.setupUi(self)
        self.setFixedSize(350,220)
        status = QLabel('<a href="https://github.com/vivars7/W11TaskbarTweak">https://github.com/vivars7/W11TaskbarTweak</a> ', self)
        status.setAlignment(Qt.AlignRight)
        status.setOpenExternalLinks(True)
        self.statusBar().addWidget(status, 1)
        self.radioButton_2.setChecked(True)
        self.radioButton_1.clicked.connect(self.changePosition)
        self.radioButton_2.clicked.connect(self.changePosition)
        self.radioButton_3.clicked.connect(self.changePosition)
        self.radioButton_4.clicked.connect(self.changePosition)
        self.pushButton.clicked.connect(self.runTweak)

    def changePosition(self):
        global selectedPosition
        if self.radioButton_1.isChecked():
            self.label.setPixmap(QPixmap(":/images/top.jpg"))
            selectedPosition = POSITION.TOP
        elif self.radioButton_2.isChecked():
            self.label.setPixmap(QPixmap(":/images/bottom.jpg"))
            selectedPosition = POSITION.BOTTOM
        elif self.radioButton_3.isChecked():
            self.label.setPixmap(QPixmap(":/images/left.jpg"))
            selectedPosition = POSITION.LEFT
        elif self.radioButton_4.isChecked():
            self.label.setPixmap(QPixmap(":/images/right.jpg"))
            selectedPosition = POSITION.RIGHT

    def runTweak(self):
        if tweaker.isWindows() == False:
            QMessageBox.warning(self, "Warning", "This tweak only supports for Windows11.")
            return
        if tweaker.detectWindows11() == False:
            QMessageBox.warning(self, "Warning", "TThis tweak only supports for Windows11.")
            return

        if selectedPosition == POSITION.LEFT or selectedPosition == POSITION.RIGHT:
            left_right_side_warn = QMessageBox.question(self, 'Warning', 'You can put the taskbar on the left or right\nbut it doesn\'t display correctly.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if left_right_side_warn == QMessageBox.No:
                return

        restart_explorer_warn = QMessageBox.question(self, 'Warning', 'You needs to restart "Windoes Explorer".\nAre you agree?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if restart_explorer_warn == QMessageBox.No:
            return
        
        tweaker.run(selectedPosition)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()