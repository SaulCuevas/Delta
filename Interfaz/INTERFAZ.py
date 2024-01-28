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

INTERFAZ
- Programa principal para ejecución de GUI en pantalla táctil.
"""

import os
import sys
print("INICIALIZANDO INTERFAZ ...\n")
print(f"Sistema: {os.name}\n")
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.name == 'nt':
    menu_path = os.path.join(path, 'Interfaz\menu')
else:
    menu_path = os.path.join(path, 'Interfaz/menu')
sys.path.insert(0, menu_path)
# Importar librerías para Ventanas GUI
import M0_INICIO as inicio
import M1_MENU as menu
import M2_A_TUTORIAL as tutorial
import M3_B_CMANUAL as cmanual
import M4_C_SMD as smd
import M5_D_ESTADISTICAS as statistics
import M6_E_COMENZAR as comenzar


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
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("DELTA-ASSYSBOT")
        self.setWindowIcon(pyGui.QIcon(inicio.icono))
        
        # myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ser = ""
        self.port = ""
        self.startINICIO()
        
# -----------------------------------------------------------------------------
    # FUNCIÓN: INICIO -> Animación al encendido del robot
    def startINICIO(self):
        self.INICIO = inicio.INICIO()   # Constructor INICIO
        self.setCentralWidget(self.INICIO)  # Fijar como widget central
        self.INICIO.btn_iniciar.clicked.connect(self.startMENU)   # Configuración al presionar botón de inicio
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------
    # FUNCIÓN: MENU -> Ventana menú de opciones
    def startMENU(self):
        self.MENU = menu.MENU() # Consturctor MENU
        self.setCentralWidget(self.MENU) # Fijar como widget central
        if self.ser != "":
            # Caso puerto ya seleccionado -> omite paso
            self.MENU.main_layout.setCurrentIndex(1)
        self.MENU.btn_accept.clicked.connect(self.get_ser)   # Configuración al presionar botón de selección puerto serial
        self.MENU.btn_1.clicked.connect(self.startTUTORIAL)   # Configuración al presionar botón de TUTORIAL
        self.MENU.btn_2.clicked.connect(self.startCMANUAL)   # Configuración al presionar botón de CONTROL MANUAL
        self.MENU.btn_3.clicked.connect(self.startSMD)   # Configuración al presionar botón de INVENTARIO SMD
        self.MENU.btn_4.clicked.connect(self.startESTADISTICAS)   # Configuración al presionar botón de ESTADÍSTICAS
        self.MENU.btn_5.clicked.connect(self.startCOMENZAR)   # Configuración al presionar botón de COMENZAR OPERACIÓN ROBOT
        self.MENU.btn_inicio.clicked.connect(self.startINICIO)   # Configuración al presionar botón de VOLVER A PANTALLA INICIO
        self.showMaximized() # Mostrar ventana maximizada
    
    # Función para mostrar puerto serial conectado
    def get_ser(self):
        self.ser = self.MENU.ser    # Obtener valor de puerto serial
        self.port = self.MENU.get_port()    # Obtener valor de dirección de puerto
        print(f"INTERFAZ: {self.ser}\n") # Imprimir valor de puerto serial
# -----------------------------------------------------------------------------
    # FUNCIÓN: TUTORIAL -> Ventana Tutorial para uso de robot
    def startTUTORIAL(self):
        self.TUTORIAL = tutorial.TUTORIAL() # Constructor TUTORIAL   
        self.setCentralWidget(self.TUTORIAL)    # Fijar como widget central
        self.TUTORIAL.btn_start.clicked.connect(self.startMENU) # Configuración al presionar botón VOLVER A MENÚ
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------
    # FUNCIÓN: CONTROL MANUAL -> Ventana para control manual de robot
    def startCMANUAL(self):
        self.CMANUAL = cmanual.CMANUAL(self.port)   # Constructor CONTROL MANUAL
        self.setCentralWidget(self.CMANUAL)     # Fijar como widget central
        self.CMANUAL.btn_start.clicked.connect(self.startMENU) # Configuración al presionar botón VOLVER A MENÚ
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------
    # FUNCIÓN: INVENTARIO SMD -> Ventana para mostrar tabla de componentes SMD válidos
    def startSMD(self):
        self.SMD = smd.SMD()    # Constructor SMD
        self.setCentralWidget(self.SMD) # Fijar como widget central
        self.SMD.btn_start.clicked.connect(self.startMENU)  # Configuración al presionar botón VOLVER A MENÚ
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------
    # FUNCIÓN: ESTADÍSTICAS -> Ventana para mostrar estadísticas de uso
    def startESTADISTICAS(self):
        self.ESTADISTICAS = statistics.ESTADISTICAS()   # Constructor ESTADISTICAS
        self.setCentralWidget(self.ESTADISTICAS)    # Fijar como widget central
        self.ESTADISTICAS.btn_start.clicked.connect(self.startMENU) # Configuración al presionar botón VOLVER A MENÚ
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------
    # FUNCIÓN: COMENZAR -> Ventana para comenzar uso de operación robot ensamblado de PCBs
    def startCOMENZAR(self):
        self.COMENZAR = comenzar.COMENZAR(self.ser) # Constructor COMENZAR
        self.setCentralWidget(self.COMENZAR)    # Fijar como widget central
        self.COMENZAR.btn_start.clicked.connect(self.startMENU) # Configuración al presionar botón VOLVER A MENÚ
        self.COMENZAR.btn_old.clicked.connect(self.user)    # Configuración al presionar botón USUARIO EXISTENTE
        self.showMaximized()    # Mostrar ventana maximizada
    
    # Función para mostrar inicio con usuario existente
    def user(self):
        self.archivos = self.COMENZAR.archivos # Constructor SELECCIÓN DE ARCHIVOS
        self.setCentralWidget(self.archivos)    # Fijar como widget central
        self.archivos.btn_start.clicked.connect(self.startMENU) # Configuración al presionar botón VOLVER A MENÚ
        self.showMaximized()    # Mostrar ventana maximizada
# -----------------------------------------------------------------------------

# INICIO APLICACIÓN PARA GUI
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    #window.showMaximized()
    app.exec()