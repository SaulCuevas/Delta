# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:19 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: SOLDADURA
"""


import os
from PyQt5.QtCore import Qt, QSize
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QPushButton,
    QLineEdit)
import qtawesome as qta

import ESP32_serial as esp

# Dirección de imagen
#path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    img_tool = os.path.join(path, 'imagenes\\tool_soldadura.png')
else:
    img_tool = os.path.join(path, 'imagenes/tool_soldadura.png')

class TOOL_S(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        print("\nCONTROL MANUAL: TOOL SOLDADURA -> CREADA\n")
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        self.amplitud = 0
        self.periodo = 1000000
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/10) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/15) # Valor de fuente 2 ajustado a tamaño pantalla
        self.icon_size = int(self.h/5) # Valor de icon size (button) ajustado a tamaño pantalla
        self.sw_size = int(self.h/5) # Valor de sw (button) ajustado a tamaño pantalla
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        params_layout = QVBoxLayout()
        params_widget = QWidget()
        params_widget.setLayout(params_layout)
        periodo_layout = QHBoxLayout()
        periodo_widget = QWidget()
        periodo_widget.setLayout(periodo_layout)
        amplitud_layout = QHBoxLayout()
        amplitud_widget = QWidget()
        amplitud_widget.setLayout(amplitud_layout)

        action_layout = QVBoxLayout()
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        
    # ---- STYLES --------------------------
    
        # Style Title Label
        st_lbl = "QLabel {"
        st_lbl += "background-color: white; "
        st_lbl += "border: 1px solid; "
        st_lbl += "font-family: Georgia; "
        st_lbl += f"font-size: {self.font_size1}pt; "
        st_lbl += "padding: 0px "
        st_lbl += "}"

        # Style Normal Label
        st_normal = "QLabel {"
        st_normal += "border: 0px solid; "
        st_normal += "font-weight: bold; "
        st_normal += "font-family: Georgia; "
        st_normal += f"font-size: {self.font_size2}pt; "
        st_normal += "padding: 3px "
        st_normal += "}"

        # Style SpinBox
        st_spb = "QSpinBox {"
        st_spb += "border: 1px solid; "
        st_spb += "font-family: Georgia; "
        st_spb += f"font-size: {self.font_size2}pt; "
        st_spb += "padding: 3px "
        st_spb += "}"

        st_spb += "QSpinBox::up-button  {"
        st_spb += "width: 30px; "
        st_spb += "}"

        st_spb += "QSpinBox::down-button  {"
        st_spb += "width: 30px; "
        st_spb += "}"

        # Style LineEdit
        st_le = "QLineEdit {"
        st_le += "background-color: white; "
        st_le += "border: 1px solid; "
        st_le += "font-family: Georgia; "
        st_le += f"font-size: {self.font_size2}pt; "
        st_le += "padding: 0px "
        st_le += "}"

        # Style Button
        st_btn = "QPushButton { "
        st_btn += "background-color: lightblue; "
        st_btn += "border-style: outset; "
        st_btn += "border-width: 2px; "
        st_btn += "border-radius: 5px; "
        st_btn += f"font-size: {self.font_size1}pt; "
        st_btn += "border-color: blue; "
        st_btn += "padding: 3px }"
        
        st_btn += "QPushButton:hover { "
        st_btn += "background-color: rgb(0, 224, 224); "
        st_btn += "border-style: inset } "
        
        st_btn += "QPushButton:pressed { "
        st_btn += "background-color: rgb(0, 0, 224); "
        st_btn += "border-style: inset } "

        # Style Button Calibración
        st_calib = "QPushButton { "
        st_calib += "background-color: rgb(250, 60, 60); "
        st_calib += "border-style: outset; "
        st_calib += "border-width: 3px; "
        st_calib += "border-radius: 5px; "
        st_calib += "border-color: rgb(250, 200, 200); "
        st_calib += "font-weight: bold; "
        st_calib += "font-family: Georgia; "
        st_btn += f"font-size: {self.font_size2}pt; "
        # st_calib += "margin: 10px; "
        st_calib += "padding: 3px }"
        
        st_calib += "QPushButton:hover { "
        st_calib += "background-color: rgb(10, 150, 150); "
        st_calib += "border-color: rgb(30, 255, 255); "
        st_calib += "border-style: groove } "
        
        st_calib += "QPushButton:pressed { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset } "
        
        st_calib += "QPushButton:checked { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset } "
        
        st_calib += "QPushButton:disabled { "
        st_calib += "background-color: rgb(150, 150, 150); "
        st_calib += "border-style: dashed; "
        st_calib += "border-color: default; "
        st_calib += "border-width: 3px; "
        st_calib += "border-radius: 0px } "

    # ---- LAYOUT PRINCIPAL ----------------

        # Label 01: Imagen Carrito
        im = QPixmap(img_tool)
        h = self.h * 0.8
        im = im.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl = QLabel()
        self.lbl.setPixmap(im)
        
        # Label 02: TEXTO CONTROL
        self.lbl_control = QLabel("OFF")
        self.lbl_control.setStyleSheet(st_lbl)
        self.lbl_control.adjustSize()
        
        # Label 03: Texto Periodo PWM
        self.lbl_periodo = QLabel("Periodo: ")
        self.lbl_periodo.setStyleSheet(st_normal)
        self.lbl_periodo.adjustSize()
        periodo_layout.addWidget(self.lbl_periodo)

        # Edit Text 02: Lectura de Periodo
        self.edit_periodo = QLineEdit(str(self.periodo))
        self.edit_periodo.adjustSize()
        validator = QIntValidator(0, 10000000)
        self.edit_periodo.setValidator(validator)
        self.edit_periodo.setStyleSheet(st_le)
        self.edit_periodo.setAlignment(Qt.AlignRight)
        w = 200
        h = self.edit_periodo.sizeHint().height() * 1.05
        self.edit_periodo.setFixedSize(w, h)
        periodo_layout.addWidget(self.edit_periodo, alignment = Qt.AlignCenter)

        # Label 04: Texto segundos Periodo
        self.lbl_time = QLabel("us")
        self.lbl_time.setStyleSheet(st_normal)
        self.lbl_time.adjustSize()
        periodo_layout.addWidget(self.lbl_time)

        # Label 05: Texto Ciclo Útil PWM
        self.lbl_dutycycle = QLabel("Amplitud: ")
        self.lbl_dutycycle.setStyleSheet(st_normal)
        self.lbl_dutycycle.adjustSize()
        amplitud_layout.addWidget(self.lbl_dutycycle)

        # SpinBox 01: Control de Amplitud
        self.spb_amplitud = QSpinBox()
        self.spb_amplitud.setMinimum(0)
        self.spb_amplitud.setMaximum(100)
        self.spb_amplitud.setSingleStep(1)
        self.spb_amplitud.setStyleSheet(st_spb)
        w = self.spb_amplitud.sizeHint().width() * 1.15
        h = int(0.4 * w)
        self.spb_amplitud.setFixedSize(w, h)
        self.spb_amplitud.setValue(self.amplitud)
        self.spb_amplitud.valueChanged.connect(self.spb_amplitud_changed)
        amplitud_layout.addWidget(self.spb_amplitud, alignment = Qt.AlignCenter)

        # Label 06: Texto Porcentaje Ciclo Útil
        self.lbl_per = QLabel("%")
        self.lbl_per.setStyleSheet(st_normal)
        self.lbl_per.adjustSize()
        amplitud_layout.addWidget(self.lbl_per)

        params_layout.addWidget(self.lbl_control, alignment = Qt.AlignCenter)
        params_layout.addWidget(periodo_widget, alignment = Qt.AlignCenter)
        params_layout.addWidget(amplitud_widget, alignment = Qt.AlignCenter)
        
        # Button 01: Desplazar hacia arriba
        icon = qta.icon("mdi.arrow-up-bold-hexagon-outline")
        self.btn_up = QPushButton(icon, "")
        self.btn_up.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_up.sizeHint().width() * 1.1
        h = self.btn_up.sizeHint().height() * 1.1
        self.btn_up.setFixedSize(w, h)
        self.btn_up.setStyleSheet(st_btn)
        self.btn_up.pressed.connect(self.move_up)
        self.btn_up.released.connect(self.move_off)
        action_layout.addWidget(self.btn_up, alignment = Qt.AlignCenter)
        
        # Button 02: Desplazar en sentido antihorario
        icon = qta.icon("mdi.arrow-down-bold-hexagon-outline")
        self.btn_down = QPushButton(icon, "")
        self.btn_down.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_down.sizeHint().width() * 1.1
        h = self.btn_down.sizeHint().height() * 1.1
        self.btn_down.setFixedSize(w, h)
        self.btn_down.setStyleSheet(st_btn)
        self.btn_down.pressed.connect(self.move_down)
        self.btn_down.released.connect(self.move_off)
        action_layout.addWidget(self.btn_down, alignment = Qt.AlignCenter)
        
        
        self.addStretch()
        self.addWidget(self.lbl, alignment = Qt.AlignCenter)
        self.addStretch()
        self.addWidget(params_widget, alignment = Qt.AlignCenter)
        self.addStretch()
        self.addWidget(action_widget, alignment = Qt.AlignCenter)
        self.addStretch()
        
        
        
    # Función para identificar desplazamiento hacia arriba
    def move_up(self):
        self.lbl_control.setText("UP")
        amplitud = float(self.amplitud)
        periodo = float(self.edit_periodo.text())
        esp.pulso_soldadura(self.ser, amplitud, periodo)
            
    # Función para identificar desplazamiento hacia abajo
    def move_down(self):
        self.lbl_control.setText("DOWN")
        amplitud = float(self.amplitud)
        periodo = float(self.edit_periodo.text())
        esp.pulso_soldadura(self.ser, -amplitud, periodo)
        
    # Función para identificar desplazamiento nulo
    def move_off(self):
        self.lbl_control.setText("OFF")
        
    # Función para cambio valor SpinBox
    def spb_amplitud_changed(self, val):
        self.amplitud = val

        

        