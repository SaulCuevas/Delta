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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel)


# Dirección de imagen
path = os.getcwd()
img_tool = os.path.join(path, 'Interfaz/imagenes/delta.jpg')

class DESACTIVADO(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
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

        # Label 01: Imagen Carrito
        print(img_tool)
        im = QPixmap(img_tool)
        h = int(self.h * 0.8)
        im = im.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl = QLabel()
        self.lbl.setPixmap(im)
        self.lbl.setStyleSheet("border: 1px dotted;")
        self.lbl.adjustSize()   # AJustar tamaño label automático
        w = im.size().width()
        h = im.size().height()
        self.lbl.setFixedSize(w, h)
        self.addStretch()
        self.addWidget(self.lbl, alignment = Qt.AlignCenter)
        self.addStretch()
        
    
        
        

        