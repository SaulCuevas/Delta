# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:19 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: DESACTIVADO
"""


import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel)


# Dirección de imagen
#path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    delta_tt1 = os.path.join(path, 'imagenes\delta_tt1.jpg')
    delta_tt2 = os.path.join(path, 'imagenes\delta_tt2.png')
else:
    delta_tt1 = os.path.join(path, 'imagenes/delta_tt1.jpg')
    delta_tt2 = os.path.join(path, 'imagenes/delta_tt2.png')

class DESACTIVADO(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        print("\nCONTROL MANUAL: TOOL DESACTIVADA -> CREADA\n")
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/20) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/30) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/40) # Valor de fuente 3 ajustado a tamaño pantalla
        self.font_size4 = int(self.h/50) # Valor de fuente 4 ajustado a tamaño pantalla
        self.font_size5 = int(self.h/60) # Valor de fuente 5 ajustado a tamaño pantalla
        self.font_size6 = int(self.h/70) # Valor de fuente 6 ajustado a tamaño pantalla
        self.border_width = int(self.h/150) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/100) # Valor de radius width (button) ajustado a tamaño pantalla
        self.pad = int(self.h/150) # Valor de padding
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        
    # ---- STYLES --------------------------
    
    # ---- LAYOUT PRINCIPAL ----------------

        # Label 01: Imagen Delta TT1
        im_tt1 = QPixmap(delta_tt1)
        h = int(self.h * 0.8)
        im_tt1 = im_tt1.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl_tt1 = QLabel()
        self.lbl_tt1.setPixmap(im_tt1)
        self.lbl_tt1.setStyleSheet("border: 1px dotted;")
        self.lbl_tt1.adjustSize()   # AJustar tamaño label automático
        w = im_tt1.size().width()
        h = im_tt1.size().height()
        self.lbl_tt1.setFixedSize(w, h)
        self.addStretch()
        self.addWidget(self.lbl_tt1, alignment = Qt.AlignCenter)
        self.addStretch()

        # Label 02: Imagen Delta TT2
        im_tt2 = QPixmap(delta_tt2)
        h = int(self.h * 0.8)
        im_tt2 = im_tt2.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl_tt2 = QLabel()
        self.lbl_tt2.setPixmap(im_tt2)
        self.lbl_tt2.setStyleSheet("border: 1px dotted;")
        self.lbl_tt2.adjustSize()   # AJustar tamaño label automático
        w = im_tt2.size().width()
        h = im_tt2.size().height()
        self.lbl_tt2.setFixedSize(w, h)
        self.addStretch()
        self.addWidget(self.lbl_tt2, alignment = Qt.AlignCenter)
        self.addStretch()
        
    
        
        

        