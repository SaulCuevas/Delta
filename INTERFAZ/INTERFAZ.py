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

import Z0_INICIO as inicio
import Z1_MENU as menu
import A_TUTORIAL as tutorial
import B_CMANUAL as cmanual
import C_SMD as smd
import D_ESTADISTICAS as statistics
import E_COMENZAR as comenzar

import PyQt5.QtGui as pyGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow)


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        self.setWindowTitle("DELTA-ASSYSBOT")
        self.setWindowIcon(pyGui.QIcon('delta.jpg'))
        # self.setFixedSize(1024, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.startINICIO()
        
# -----------------------------------------------------------------------------

    def startINICIO(self):
        self.INICIO = inicio.INICIO()
        self.setCentralWidget(self.INICIO)
        self.INICIO.btn_start.clicked.connect(self.startMENU)
        self.show()
        
# -----------------------------------------------------------------------------
        
    def startMENU(self):
        self.MENU = menu.MENU()
        self.setCentralWidget(self.MENU)
        self.MENU.btn_1.clicked.connect(self.startTUTORIAL)
        self.MENU.btn_2.clicked.connect(self.startCMANUAL)
        self.MENU.btn_3.clicked.connect(self.startSMD)
        self.MENU.btn_4.clicked.connect(self.startESTADISTICAS)
        self.MENU.btn_5.clicked.connect(self.startCOMENZAR)
        self.MENU.btn_inicio.clicked.connect(self.startINICIO)
        self.show()

# -----------------------------------------------------------------------------

    def startTUTORIAL(self):
        self.TUTORIAL = tutorial.TUTORIAL()
        self.setCentralWidget(self.TUTORIAL)
        self.TUTORIAL.btn_start.clicked.connect(self.startMENU)
        self.show()

# -----------------------------------------------------------------------------

    def startCMANUAL(self):
        self.CMANUAL = cmanual.CMANUAL()
        self.setCentralWidget(self.CMANUAL)
        self.CMANUAL.btn_start.clicked.connect(self.startMENU)
        self.show()

# -----------------------------------------------------------------------------

    def startSMD(self):
        self.SMD = smd.SMD()
        self.setCentralWidget(self.SMD)
        self.SMD.btn_start.clicked.connect(self.startMENU)
        self.show()

# -----------------------------------------------------------------------------

    def startESTADISTICAS(self):
        self.ESTADISTICAS = statistics.ESTADISTICAS()
        self.setCentralWidget(self.ESTADISTICAS)
        self.ESTADISTICAS.btn_start.clicked.connect(self.startMENU)
        self.show()

# -----------------------------------------------------------------------------

    def startCOMENZAR(self):
        self.COMENZAR = comenzar.COMENZAR()
        self.setCentralWidget(self.COMENZAR)
        self.COMENZAR.btn_start.clicked.connect(self.startMENU)
        self.show()
        
# -----------------------------------------------------------------------------

        
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    window.showMaximized()
    app.exec()
    
