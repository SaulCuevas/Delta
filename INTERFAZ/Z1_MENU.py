# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

Descripción:
    El siguiente código tiene como objetivo desarrollar la interfaz gráfica de
    usuario para el control por medio de la pantalla tactil del proyecto de TT.
    Esta es su versión 1, donde se implementa un diseño sencillo, muy básico 
    para poder realizar pruebas y cumplir con todas las ventanas deseadas en
    el diseño.

@author: Spect
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton)

class MENU(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        
        main_layout = QVBoxLayout()

        # Button 01: Inicio de programa
        self.btn_1 = QPushButton("Tutorial")
        # btn_1.clicked.connect(start_acquisition)
        
        style = "QPushButton { "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: blue; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(0, 224, 224); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 0, 224); "
        style += "border-style: inset } "
        
        self.btn_1.setStyleSheet(style)
        self.btn_1.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_1.sizeHint().width() + 60
        h = self.btn_1.sizeHint().height() + 20
        self.btn_1.setFixedSize(w, h)
        
        main_layout.addWidget(self.btn_1, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_2 = QPushButton("Control Manual")
        # btn_2.clicked.connect(start_acquisition)
        
        style = "QPushButton { "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: blue; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(0, 224, 224); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 0, 224); "
        style += "border-style: inset } "
        
        self.btn_2.setStyleSheet(style)
        self.btn_2.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_2.sizeHint().width() + 60
        h = self.btn_2.sizeHint().height() + 20
        self.btn_2.setFixedSize(w, h)
        
        main_layout.addWidget(self.btn_2, alignment = Qt.AlignCenter)
        
        
        # Button 01: Inicio de programa
        self.btn_3 = QPushButton("SMD válidos")
        # btn_3.clicked.connect(start_acquisition)
        
        style = "QPushButton { "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: blue; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(0, 224, 224); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 0, 224); "
        style += "border-style: inset } "
        
        self.btn_3.setStyleSheet(style)
        self.btn_3.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_3.sizeHint().width() + 60
        h = self.btn_3.sizeHint().height() + 20
        self.btn_3.setFixedSize(w, h)
        
        main_layout.addWidget(self.btn_3, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_4 = QPushButton("Estadísticas")
        # btn_4.clicked.connect(start_acquisition)
        
        style = "QPushButton { "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: blue; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(0, 224, 224); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 0, 224); "
        style += "border-style: inset } "
        
        self.btn_4.setStyleSheet(style)
        self.btn_4.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_4.sizeHint().width() + 60
        h = self.btn_4.sizeHint().height() + 20
        self.btn_4.setFixedSize(w, h)
        
        main_layout.addWidget(self.btn_4, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_5 = QPushButton("Comenzar")
        # btn_5.clicked.connect(start_acquisition)
        
        style = "QPushButton { "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: blue; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(0, 224, 224); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 0, 224); "
        style += "border-style: inset } "
        
        self.btn_5.setStyleSheet(style)
        self.btn_5.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_5.sizeHint().width() + 60
        h = self.btn_5.sizeHint().height() + 20
        self.btn_5.setFixedSize(w, h)
        
        main_layout.addWidget(self.btn_5, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_inicio = QPushButton("INICIO")
        # btn_3.clicked.connect(start_acquisition)
        w = self.btn_inicio.sizeHint().width()
        h = self.btn_inicio.sizeHint().height()
        self.btn_inicio.setFixedSize(w, h)
        # self.btn_inicio.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        main_layout.addWidget(self.btn_inicio, alignment = Qt.AlignCenter)
        
        self.setLayout(main_layout)

