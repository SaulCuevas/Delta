# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

INICIO
- Ventana para inicio de programa al encendido del robot.
  Muestra animación previo al uso del robot para interacción
  con el usuario.
"""

# Líbrerías
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QDesktopWidget)
import os

# Dirección de imagen
# path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    img_delta = os.path.join(path, 'Interfaz\imagenes\delta.jpg')
else:
    img_delta = os.path.join(path, 'Interfaz/imagenes/delta.jpg')

# CLASE INICIO - WIDGET
class INICIO(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()  # Dimension general width pantalla
        self.h = QDesktopWidget().screenGeometry().height() # Dimension general height pantalla
        self.font_size = int(self.h/30) # Valor de fuente ajustado a tamaño pantalla
        self.border_width = int(self.h/100) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/60) # Valor de radius width (button) ajustado a tamaño pantalla
        # Generación layouts generales
        inicio_layout = QVBoxLayout()

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Imagen Bienvenida
        # 02. Button 01: Inicio de programa

    # ----- STYLE WIDGET -----------------------------------------------------
        verde_oscuro = "rgb(35, 155, 86)"
        azul_claro = "rgb(84, 153, 199)"
        azul_oscuro = "rgb(21, 67, 96)"

        # Style Button Widgets
        style = "QPushButton { "
        style += "background-color: lightgreen; "
        style += "border-style: outset; "
        style += f"border-width: {self.border_width}px; "
        style += f"border-radius: {self.border_radius}px; "
        style += "border-color: green; "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += f"font-size: {self.font_size}pt; "
        style += "padding: 3px }"

        style += "QPushButton:hover { "
        style += f"background-color: {verde_oscuro}; "
        style += "border-color: green; "
        style += "border-style: inset } "

        style += "QPushButton:pressed { "
        style += f"background-color: {azul_claro}; "
        style += f"border-color: {azul_oscuro}; "
        style += "border-style: inset } "

    # ----- INICIO WIDGET -----------------------------------------------------

        # Label 01: Imagen Bienvenida
        im = QPixmap(img_delta) # Generar PIXMAP para imagen/video inicio
        im = im.scaled(self.h - 100, self.h - 100, Qt.KeepAspectRatio)  # Escalar imagen al tamaño deseado conforme relación de pantalla
        self.lbl = QLabel() # Generar Label para contener PIXMAP (imagen)
        self.lbl.setPixmap(im) # Fijar imagen de pixmap a Label
        self.lbl.adjustSize()   # AJustar tamaño label automático
        inicio_layout.addWidget(self.lbl, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT INICIO
        
        # Button 01: Inicio de programa
        self.btn_iniciar = QPushButton("INICIAR")   # Generar PushButton de INICIO
        self.btn_iniciar.setStyleSheet(style) # Fijar estilo de Widget
        w = self.btn_iniciar.sizeHint().width() * 1.35  # Guardar valor de ancho para button
        h = self.btn_iniciar.sizeHint().height() * 1.05 # Guardar valor de alto para button
        self.btn_iniciar.setFixedSize(w, h) # AJustar valores de ancho (w) y alto (h) para button
        inicio_layout.addWidget(self.btn_iniciar, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT INICIO
    
        self.setLayout(inicio_layout) # Fijar layout principal para widget INICIO
        
