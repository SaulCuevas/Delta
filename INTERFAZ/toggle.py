# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 16:49:58 2023

link:
    https://touch-sp.hatenablog.com/entry/2022/04/16/081340

@author: Spect
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QGridLayout, QFrame, QSizePolicy

class ToggleButton(QFrame):

    clicked = pyqtSignal(bool)

    def __init__(self, width = 30, height = 50):
        super().__init__()
        self.width = width
        self.height = height
        if self.width < self.height * 2 - 20:
            self.width = self.height * 2 - 20
        self.setFixedSize(self.width, self.height)
        self.toggle_on = False
        self.initUI()

    def initUI(self):
        
        self.button_1 = QPushButton()
        self.button_1.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.button_2 = QPushButton()
        self.button_3 = QPushButton()

        self.button_2.setFixedSize(self.height - 30, self.height - 30)
        self.button_3.setFixedSize(self.height - 30, self.height - 30)

        self.button_1.setStyleSheet(
            "border-radius : %d; border : 2px solid black; background-color: rgb(255, 255, 255)"%((self.height - 20)//2))

        self.button_2.setStyleSheet(
            "border-radius : %d; background-color: rgb(0, 0, 0)"%((self.height - 30)//2))
        
        self.button_3.setStyleSheet(
            "border-radius : %d; background-color: rgb(255, 255, 255)"%((self.height - 30)//2))
        self.button_3.setVisible(False)
        
        self.button_1.clicked.connect(self.pushToggle)
        self.button_2.clicked.connect(self.pushToggle)
        self.button_3.clicked.connect(self.pushToggle)

        layout = QGridLayout()
        layout.addWidget(self.button_1, 0, 0, 1, 2)
        layout.addWidget(self.button_2, 0, 0, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_3, 0, 1, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def pushToggle(self):

        self.toggle_on = not self.toggle_on

        if (self.toggle_on == True):
                self.button_1.setStyleSheet("border-radius : %s; border : 2px solid black; background-color: rgb(60, 156, 253)"%((self.height - 20)//2))
                self.button_2.setVisible(False)
                self.button_3.setVisible(True)
        else:
                self.button_1.setStyleSheet("border-radius : %s; border : 2px solid black; background-color: rgb(255, 255, 255)"%((self.height - 20)//2))
                self.button_2.setVisible(True)
                self.button_3.setVisible(False)
        
        self.clicked.emit(self.toggle_on)