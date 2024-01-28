# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:19 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: INVENTARIO
"""


import os
import sys
from PyQt5.QtCore import Qt, QSize
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QPushButton,
    QLineEdit)
import qtawesome as qta
from toggle import ToggleButton
import numpy as np

import ESP32_serial as esp

# Dirección de imagen
#path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    img_tool = os.path.join(path, 'imagenes\\tool_inv.png')
else:
    img_tool = os.path.join(path, 'imagenes/tool_inv.png')

class INVENTORY(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        print("\nCONTROL MANUAL: TOOL INVENTARIO -> CREADA\n")
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        self.invent_val = 0
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/12) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/18) # Valor de fuente 2 ajustado a tamaño pantalla
        self.border_width = int(self.h/150) # Valor de border width (button) ajustado a tamaño pantalla
        self.icon_size = int(self.h/8) # Valor de icon size (button) ajustado a tamaño pantalla
        self.sw_size = int(self.h/5) # Valor de sw (button) ajustado a tamaño pantalla
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Generar LAYOUT de ACTION BUTTONS
        action_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        sensor_layout = QHBoxLayout()
        sensor_widget = QWidget()
        sensor_widget.setLayout(sensor_layout)
        angle_layout = QHBoxLayout()
        angle_widget = QWidget()
        angle_widget.setLayout(angle_layout)
        
    # ---- STYLES --------------------------

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
        #st_spb += "border-width: 1px "
        st_spb += "}"

        st_spb += "QSpinBox::down-button  {"
        st_spb += "width: 30px; "
        #st_spb += "border-width: 1px "
        st_spb += "}"

        # Style LineEdit
        st_le = "QLineEdit {"
        st_le += "background-color: white; "
        st_le += "border: 1px solid; "
        st_le += "font-family: Georgia; "
        st_le += f"font-size: {self.font_size1}pt; "
        st_le += "padding: 0px "
        st_le += "}"

        # Style Button
        st_btn = "QPushButton { "
        st_btn += "background-color: lightblue; "
        st_btn += "border-style: outset; "
        st_btn += "border-width: 2px; "
        st_btn += "border-radius: 5px; "
        st_btn += "font-size: 15pt; "
        st_btn += "border-color: blue; "
        st_btn += "padding: 3px }"
        
        st_btn += "QPushButton:hover { "
        st_btn += "background-color: rgb(0, 224, 224); "
        st_btn += "border-style: inset } "
        
        st_btn += "QPushButton:pressed { "
        st_btn += "background-color: rgb(0, 0, 224); "
        st_btn += "border-style: inset } "


    # ---- LAYOUT PRINCIPAL ----------------

        # Label 01: Imagen Carrito
        # print(f"B1: {img_tool}")
        im = QPixmap(img_tool)
        h = self.h * 0.8
        im = im.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl = QLabel()
        self.lbl.setPixmap(im)
        self.addStretch(1)
        self.addWidget(self.lbl, alignment = Qt.AlignCenter)
        self.addStretch(2)
        
        # Label 02: TEXTO CONTROL
        self.lbl_control = QLabel("RAD/DEG")
        self.lbl_control.adjustSize()
        self.lbl_control.setStyleSheet(st_normal)
        top_layout.addWidget(self.lbl_control, alignment = Qt.AlignCenter)
        
        # Switch 01: TOOGLE BUTTON para cambio de medida angulo en COORD LAYOUT
        self.sw_measure = ToggleButton(self.sw_size)    # Generar ToogleButton para cambio de angulo
        self.sw_measure.setStyleSheet("")    # Fijar estilo de widget
        self.sw_measure.clicked.connect(self.sw_angle)
        top_layout.addWidget(self.sw_measure, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MEASURE

        # Label 03: Texto Sensor
        self.lbl_sensor = QLabel("Sensor:")
        self.lbl_sensor.adjustSize()
        self.lbl_sensor.setStyleSheet(st_normal)
        sensor_layout.addWidget(self.lbl_sensor, alignment = Qt.AlignCenter)

        # Edit Text 01: Lectura de Sensor Radianes
        self.edit_sensor = QLineEdit()
        self.edit_sensor.setStyleSheet(st_le)
        self.edit_sensor.setReadOnly(True)
        self.edit_sensor.setFixedWidth(self.w * 0.3)
        sensor_layout.addWidget(self.edit_sensor, alignment = Qt.AlignCenter)

        # Label 04: Texto Radianes
        self.lbl_rad = QLabel("rad")
        self.lbl_rad.adjustSize()
        w = self.lbl_rad.sizeHint().width() * 5
        self.lbl_rad.setFixedWidth(w)
        self.lbl_rad.setStyleSheet(st_normal)
        sensor_layout.addWidget(self.lbl_rad, alignment = Qt.AlignCenter)

        # Label 05: Texto Posición
        self.lbl_angle = QLabel("Ángulo:")
        self.lbl_angle.adjustSize()
        self.lbl_angle.setStyleSheet(st_normal)
        angle_layout.addWidget(self.lbl_angle, alignment = Qt.AlignCenter)

        # SpinBox 01: Control de Ángulo
        self.spb_angle = QSpinBox()
        self.spb_angle.setStyleSheet(st_spb)
        self.spb_angle.setMinimum(0)
        self.spb_angle.setMaximum(360)
        self.spb_angle.setSingleStep(1)
        self.spb_angle.setSuffix(" °")
        w = self.spb_angle.sizeHint().width() * 1.2
        h = int(0.4 * w)
        self.spb_angle.setFixedSize(w, h)
        self.spb_angle.setValue(0)
        # self.spb_angle.valueChanged.connect(self.spb_vel_changed)
        angle_layout.addWidget(self.spb_angle, alignment = Qt.AlignCenter)

        # Button 01: Enviar valor
        icon = qta.icon("mdi6.flag-triangle")
        self.btn_send = QPushButton(icon, "")
        self.btn_send.clicked.connect(self.move_inventory)
        self.btn_send.setStyleSheet(st_btn)
        self.btn_send.setIconSize(QSize(self.icon_size, self.icon_size))   # Ajustar tamaño de ícono
        w = self.btn_send.sizeHint().width() * 1.1
        h = self.btn_send.sizeHint().height() * 1.1
        self.btn_send.setFixedSize(w, h)
        angle_layout.addSpacing(10)
        angle_layout.addWidget(self.btn_send, alignment = Qt.AlignCenter)

        action_layout.addWidget(top_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(sensor_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(angle_widget, alignment = Qt.AlignCenter)
        
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        
        self.addWidget(action_widget, alignment = Qt.AlignCenter)
        self.addStretch(1)
        
        
    def move_inventory(self):
        x = self.spb_angle.value()
        angle = np.deg2rad(x)
        esp.mover_motor(self.ser, 6, angle)

    def sw_angle(self):
        if (self.sw_measure.toggle_on == False):
            self.invent_val = self.invent_val
            self.lbl_rad.setText("rad")
            text_inv = f"{self.invent_val:.4f}"
        elif (self.sw_measure.toggle_on == True):
            self.invent_val = np.rad2deg(self.invent_val)
            self.lbl_rad.setText("°")
            text_inv = f"{self.invent_val:.2f}"
        self.edit_sensor.setText(text_inv)
        
        

        