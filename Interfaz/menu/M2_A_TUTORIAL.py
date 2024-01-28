# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TUTORIAL
- Ventana enlazada con página web para mostrar contenido de
  tutorial didáctico (en teoría)
"""

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QDesktopWidget)

# CLASE TUTORIAL - WIDGET
class TUTORIAL(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        print("\nVENTANA -TUTORIAL- CREADA\n")
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()  # Dimension general width pantalla
        self.h = QDesktopWidget().screenGeometry().height() # Dimension general height pantalla
        self.font_size = int(self.h/30) # Valor de fuente ajustado a tamaño pantalla
        self.border_width = int(self.h/100) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/60) # Valor de radius width (button) ajustado a tamaño pantalla
        # Generación layouts generales
        main_layout = QVBoxLayout() # LAYOUT general

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Etiqueta para titulo de ventana TUTORIAL
        # 02. WebView 01: Ventana Navegador para TUTORIAL web
        # 03. Button 01: Volver a MENU

    # ----- STYLE WIDGET -----------------------------------------------------
        verde_oscuro = "rgb(35, 155, 86)"
        azul_claro = "rgb(84, 153, 199)"
        azul_oscuro = "rgb(21, 67, 96)"

        # Style Label Widgets
        st_label = "QLabel { "
        st_label += "background-color: lightgreen; "
        st_label += "border-style: none; "
        st_label += "font-weight: bold; "
        st_label += "font-family: Georgia; "
        st_label += f"font-size: {self.font_size}pt; "
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
        st_btn += f"font-size: {self.font_size}pt; "
        st_btn += "padding: 3px }"

        st_btn += "QPushButton:hover { "
        st_btn += f"background-color: {verde_oscuro}; "
        st_btn += "border-color: green; "
        st_btn += "border-style: inset } "

        st_btn += "QPushButton:pressed { "
        st_btn += f"background-color: {azul_claro}; "
        st_btn += f"border-color: {azul_oscuro}; "
        st_btn += "border-style: inset } "

    # ------ SPECIAL WIDGET ------------------------------------------------------

        # Label 01: Etiqueta para titulo de ventana TUTORIAL
        lbl_tutorial = QLabel("TUTORIAL")   # Generar Label Ventana TUTORIAL
        lbl_tutorial.setAlignment(Qt.AlignCenter)   # Alinear texto en el centro
        lbl_tutorial.setStyleSheet(st_label)    # Fijar estilo de widget
        w = lbl_tutorial.sizeHint().width() * 1.3    # Guardar valor de ancho para widget
        h = lbl_tutorial.sizeHint().height() * 1.05   # Guardar valor de alto para widget
        lbl_tutorial.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(lbl_tutorial, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT GENERAL

        # WebView 01: Widget para el navegador
        self.webview = QWebEngineView() # Generar widget WebView
        self.webview.setUrl(QUrl("https://delta-assysbot.firebaseapp.com")) # Fijar página web destino
        # self.webview.setUrl(QUrl("https://www.recursospython.com/"))  # Página ejemplo
        self.webview.setFixedSize(self.w * 0.9, self.h * 0.75)   # Ajustar valores de ancho (w) y alto (h) para button
        main_layout.addWidget(self.webview, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT GENERAL
        
        # Button 01: Inicio de programa
        self.btn_start = QPushButton("Volver")  # Generar PushBUtton VOLVER A MENU
        self.btn_start.setStyleSheet(st_btn)    # Fijar estilo para widget
        w = self.btn_start.sizeHint().width() * 1.3 # Guardar valor de ancho para widget
        h = self.btn_start.sizeHint().height() * 1.05  # Guardar valor de alto para widget
        self.btn_start.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT GENERAL
        
        # Fijar LAYOUT PRINCIPAL en widget TUTORIAL
        self.setLayout(main_layout)
        