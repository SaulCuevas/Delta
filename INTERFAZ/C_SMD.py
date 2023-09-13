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

import sys
from PyQt5.QtCore import Qt,QTimer
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QTabWidget,
    QLineEdit,
    QCheckBox,
    QDoubleSpinBox)
import matplotlib
matplotlib.use('Qt5Agg')


class SMD(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        
        main_layout = QVBoxLayout()

        # Label 01: Etiqueta para Selección de Puerto COM
        lbl_smd = QLabel("SMD Válidos")
        lbl_smd.setAlignment(Qt.AlignCenter)
        lbl_smd.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_smd.sizeHint().width() + 10
        h = lbl_smd.sizeHint().height()
        lbl_smd.setFixedSize(w, h)
        main_layout.addWidget(lbl_smd, alignment = Qt.AlignCenter)

        # Label 01: Imagen Bienvenida
        im = QPixmap("imagenes/delta.jpg")
        im = im.scaled(400, 400, Qt.KeepAspectRatio)
        self.lbl = QLabel()
        self.lbl.setPixmap(im)
        main_layout.addWidget(self.lbl, alignment = Qt.AlignCenter)
        
        
        # Button 01: Inicio de programa
        self.btn_start = QPushButton("Volver")

        style = "QPushButton { "
        style += "background-color: lightgreen; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: green; "
        # style += "font: bold 14px; "
        style += "padding: 2px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(224, 224, 0); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(224, 0, 0); "
        style += "border-style: inset } "
        
        self.btn_start.setStyleSheet(style)
        self.btn_start.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_start.sizeHint().width() + 100
        h = self.btn_start.sizeHint().height() + 5
        self.btn_start.setFixedSize(w, h)
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)
        
        
        self.setLayout(main_layout)
        
