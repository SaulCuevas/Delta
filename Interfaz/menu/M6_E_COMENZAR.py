# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

COMENZAR
- Ventana muestra inicio de operación de ensamblado de PCBs.
  Desde selección de usuario (nuevo o existente), selección
  de archivos gerber, ordenamiento de componentes y monitoreo.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton)

import op.E1_COMENZAR as archivos


# CLASE COMENZAR - WIDGET
class COMENZAR(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        self.font_size1 = int(self.h/20) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/30) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/50) # Valor de fuente 3 ajustado a tamaño pantalla
        self.font_size4 = int(self.h/40) # Valor de fuente 4 ajustado a tamaño pantalla
        self.border_width = int(self.h/100) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/60) # Valor de radius width (button) ajustado a tamaño pantalla
        # Inicializacion de variables
        self.archivos = archivos.ARCHIVOS()
        # Generación layouts generales
        main_layout = QVBoxLayout()

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Etiqueta para titulo de ventana COMENZAR
        # 02. Button 01: NUEVO USUARIO
        # 03. Button 02: USUARIO EXISTENTE
        # 04. Button 03: Volver a ventana de MENU

    # ----- STYLE VARIABLES -----------------------------------------------------
        verde_oscuro = "rgb(35, 155, 86)"
        azul_claro = "rgb(84, 153, 199)"
        azul_oscuro = "rgb(21, 67, 96)"

        # Style Label Widgets
        st_label = "QLabel { "
        st_label += "background-color: lightgreen; "
        st_label += "border-style: none; "
        st_label += "font-weight: bold; "
        st_label += "font-family: Georgia; "
        st_label += f"font-size: {self.font_size2}pt; "
        st_label += "padding: 3px }"

        # Style Button Widgets
        st_btn = "QPushButton { "
        st_btn += "background-color: lightgreen; "
        st_btn += "border-style: outset; "
        st_btn += f"border-width: {self.border_width}px; "
        st_btn += f"border-radius: {self.border_radius}px; "
        st_btn += "border-color: green; "
        st_btn += "font-weight: bold; "
        st_btn += "font-family: Georgia; "
        st_btn += f"font-size: {self.font_size2}pt; "
        st_btn += "padding: 3px }"

        st_btn += "QPushButton:hover { "
        st_btn += f"background-color: {verde_oscuro}; "
        st_btn += "border-color: green; "
        st_btn += "border-style: inset } "

        st_btn += "QPushButton:pressed { "
        st_btn += f"background-color: {azul_claro}; "
        st_btn += f"border-color: {azul_oscuro}; "
        st_btn += "border-style: inset } "

        # Style Button Widgets (ALT)
        st_alt = "QPushButton { "
        st_alt += "background-color: rgb(41, 128, 185); "
        st_alt += "border-style: outset; "
        st_alt += "border-width: 5px; "
        st_alt += "border-radius: 20px; "
        st_alt += "border-color: rgb(26, 82, 118); "
        st_alt += "font-weight: bold; "
        st_alt += "font-family: Georgia; "
        st_alt += "font-size: 25pt; "
        st_alt += "padding: 10px }"
        
        st_alt += "QPushButton:hover { "
        st_alt += "background-color: rgb(155, 89, 182); "
        st_alt += "border-color: rgb(187, 143, 206); "
        st_alt += "border-style: groove } "
        
        st_alt += "QPushButton:pressed { "
        st_alt += "background-color: rgb(192, 57, 43); "
        st_alt += "border-color: rgb(231, 76, 60); "
        st_alt += "border-style: inset } "

    # ----- PRINCIPAL WIDGET -----------------------------------------------------
        
        # Label 01: Etiqueta para titulo de ventana COMENZAR
        lbl_comenzar = QLabel("COMENZAR")   # Generar Label Ventana COMENZAR
        lbl_comenzar.setAlignment(Qt.AlignCenter)   # Alinear texto en el centro
        lbl_comenzar.setStyleSheet(st_label)    # Fijar estilo de widget
        w = lbl_comenzar.sizeHint().width() + 10    # Guardar valor de ancho para widget
        h = lbl_comenzar.sizeHint().height()    # Guardar valor de alto para widget
        lbl_comenzar.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(lbl_comenzar, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT PRINCIPAL
        
        # Button 01: NUEVO USUARIO
        self.btn_new = QPushButton("Nuevo Usuario") # Generar PushBUtton NUEVO USUARIO
        self.btn_new.setStyleSheet(st_alt)   # Fijar estilo de widget
        w = self.btn_new.sizeHint().width() # Guardar valor de ancho para widget
        h = self.btn_new.sizeHint().height()    # Guardar valor de alto para widget
        self.btn_new.setFixedSize(w + 10, h + 10)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_new, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT PRINCIPAL
        
        # Button 02: USUARIO EXISTENTE
        self.btn_old = QPushButton("Usuario Existente") # Generar PushBUtton USUARIO EXISTENTE
        self.btn_old.setStyleSheet(st_alt)   # Fijar estilo de widget
        w = self.btn_old.sizeHint().width() # Guardar valor de ancho para widget
        h = self.btn_old.sizeHint().height()    # Guardar valor de alto para widget
        self.btn_old.setFixedSize(w + 10, h + 10)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_old, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT PRINCIPAL
        
        # Button 03: Volver a ventana de MENU
        self.btn_start = QPushButton("Volver")  # Generar PushBUtton VOLVER A MENU  
        self.btn_start.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_start.sizeHint().width() * 1.3 # Guardar valor de ancho para widget
        h = self.btn_start.sizeHint().height() + 10  # Guardar valor de alto para widget
        self.btn_start.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT PRINCIPAL
        
        # Fijar LAYOUT PRINCIPAL en widget COMENZAR
        self.setLayout(main_layout)
        
        
# -----------------------------------------------------------------------------


        
# -----------------------------------------------------------------------------
        
        
