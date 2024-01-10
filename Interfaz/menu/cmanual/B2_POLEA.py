# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 14:27:44 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: POLEA
"""

import os
import sys
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
    img_tool = os.path.join(path, 'imagenes\\tool_ninguna.png')
else:
    img_tool = os.path.join(path, 'imagenes/tool_ninguna.png')

class TOOL_N(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/18) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/22) # Valor de fuente 2 ajustado a tamaño pantalla
        self.icon_size = int(self.h/13) # Valor de icon size (button) ajustado a tamaño pantalla
        self.sw_size = int(self.h/8) # Valor de sw (button) ajustado a tamaño pantalla
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.distance = 0.0
        # Herramienta seleccionada
        self.tool = 0
        print("E1")
        print(self.ser)
        esp.cambio_herramienta(self.ser, self.tool)
        print("E2")
        # T : Seleccion de herramienta
        # 0 - mover motor M5 a pos de Camara
        # 1 - mover motor M5 a pos de Dispensador
        # 2 - mover motor M5 a pos de Manipulador PnP
        
        # general_layout = QHBoxLayout()
        action_layout = QVBoxLayout()
        action_layout.setSpacing(0)
        sensor_layout = QHBoxLayout()
        amplitud_layout = QHBoxLayout()
        periodo_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        sensor_widget = QWidget()
        amplitud_widget = QWidget()
        periodo_widget = QWidget()
        btn_widget = QWidget()
        sensor_widget.setLayout(sensor_layout)
        amplitud_widget.setLayout(amplitud_layout)
        periodo_widget.setLayout(periodo_layout)
        btn_widget.setLayout(btn_layout)
        
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
        im = QPixmap(img_tool)
        h = self.h * 0.8
        self.lbl = QLabel()
        im = im.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl.setPixmap(im)
        self.addStretch()
        self.addWidget(self.lbl, alignment = Qt.AlignCenter)
        self.addStretch()
        
        # Label 02: TEXTO CONTROL
        self.lbl_control = QLabel("OFF")
        self.lbl_control.setStyleSheet(st_lbl)
        self.lbl_control.adjustSize()
        action_layout.addWidget(self.lbl_control, alignment = Qt.AlignCenter)

        # Button 01: Enviar a HOME
        icon = qta.icon("ei.home")
        self.btn_home = QPushButton(icon, "")
        self.btn_home.setStyleSheet(st_btn)
        self.btn_home.setIconSize(QSize(self.icon_size, self.icon_size))
        w = self.btn_home.sizeHint().width() * 1.1
        h = self.btn_home.sizeHint().height() * 1.1
        self.btn_home.setFixedSize(w, h)
        self.btn_home.clicked.connect(self.send_home)
        self.btn_home.pressed.connect(self.text_home)
        self.btn_home.released.connect(self.spin_off)
        sensor_layout.addWidget(self.btn_home, alignment = Qt.AlignCenter)

        # Label 03: TEXTO SENSOR
        self.lbl_sensor = QLabel("SENSOR: ")
        self.lbl_sensor.setStyleSheet(st_normal)
        self.lbl_sensor.adjustSize()
        w = self.lbl_sensor.sizeHint().width() * 1.1
        h = self.lbl_sensor.sizeHint().height() * 1.05
        self.lbl_sensor.setFixedSize(w, h)
        sensor_layout.addWidget(self.lbl_sensor, alignment = Qt.AlignCenter)

        # Edit Text 01: Lectura de Sensor
        self.edit_sensor = QLineEdit()
        self.edit_sensor.setStyleSheet(st_le)
        self.edit_sensor.setReadOnly(True)
        w = self.edit_sensor.sizeHint().width() * 1.1
        h = self.edit_sensor.sizeHint().height() * 1.05
        self.edit_sensor.setFixedSize(w, h)
        sensor_layout.addWidget(self.edit_sensor, alignment = Qt.AlignCenter)

        # Label 04: TEXTO AMPLITUD
        self.lbl_amplitud = QLabel("Amplitud: ")
        self.lbl_amplitud.setStyleSheet(st_normal)
        self.lbl_amplitud.adjustSize()
        w = self.lbl_sensor.sizeHint().width() * 1.1
        h = self.lbl_sensor.sizeHint().height() * 1.05
        self.lbl_sensor.setFixedSize(w, h)
        amplitud_layout.addWidget(self.lbl_amplitud, alignment = Qt.AlignCenter)

        # SpinBox 01: Control de Amplitud
        self.spb_amplitud = QSpinBox()
        self.spb_amplitud.setMinimum(0)
        self.spb_amplitud.setMaximum(100)
        self.spb_amplitud.setSingleStep(1)
        self.spb_amplitud.setStyleSheet(st_spb)
        w = self.spb_amplitud.sizeHint().width() * 1.15
        h = int(0.4 * w)
        self.spb_amplitud.setFixedSize(w, h)
        self.spb_amplitud.setValue(0)
        self.spb_amplitud.valueChanged.connect(self.spb_amplitud_changed)
        amplitud_layout.addWidget(self.spb_amplitud, alignment = Qt.AlignCenter)
        
        # Label 03: TEXTO PERIODO
        self.lbl_periodo = QLabel("Periodo: ")
        self.lbl_periodo.setStyleSheet(st_normal)
        self.lbl_periodo.adjustSize()
        w = self.lbl_periodo.sizeHint().width() * 1.1
        h = self.lbl_periodo.sizeHint().height() * 1.05
        self.lbl_periodo.setFixedSize(w, h)
        periodo_layout.addWidget(self.lbl_periodo, alignment = Qt.AlignCenter)

        # Edit Text 02: Lectura de Periodo
        self.edit_periodo = QLineEdit("1000000")
        validator = QIntValidator(0, 10000000)
        self.edit_periodo.setValidator(validator)
        self.edit_periodo.setStyleSheet(st_le)
        self.edit_periodo.setAlignment(Qt.AlignRight)
        w = self.edit_periodo.sizeHint().width() * 1.1
        h = self.edit_periodo.sizeHint().height() * 1.05
        self.edit_periodo.setFixedSize(w, h)
        periodo_layout.addWidget(self.edit_periodo, alignment = Qt.AlignCenter)

        # Label 04: Texto MicroSegundos
        self.lbl_us = QLabel("us")
        self.lbl_us.adjustSize()
        w = self.lbl_us.sizeHint().width() * 5
        self.lbl_us.setFixedWidth(w)
        self.lbl_us.setStyleSheet(st_normal)
        periodo_layout.addWidget(self.lbl_us, alignment = Qt.AlignCenter)

        # Button 01: Desplazar en sentido antihorario
        icon = qta.icon("mdi.cog-counterclockwise")
        self.btn_countercw = QPushButton(icon, "")
        self.btn_countercw.setStyleSheet(st_btn)
        self.btn_countercw.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_countercw.sizeHint().width() * 1.1
        h = self.btn_countercw.sizeHint().height() * 1.1
        self.btn_countercw.setFixedSize(w, h)
        self.btn_countercw.pressed.connect(self.spin_countercw)
        self.btn_countercw.released.connect(self.spin_off)
        btn_layout.addWidget(self.btn_countercw, alignment = Qt.AlignCenter)
        
        # Button 02: Desplazar en sentido horario
        icon = qta.icon("mdi.cog-clockwise")
        self.btn_clockwise = QPushButton(icon, "")
        self.btn_clockwise.setStyleSheet(st_btn)
        self.btn_clockwise.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_clockwise.sizeHint().width() * 1.1
        h = self.btn_clockwise.sizeHint().height() * 1.1
        self.btn_clockwise.setFixedSize(w, h)
        self.btn_clockwise.pressed.connect(self.spin_clockwise)
        self.btn_clockwise.released.connect(self.spin_off)
        btn_layout.addWidget(self.btn_clockwise, alignment = Qt.AlignCenter)

        w = btn_widget.sizeHint().width() * 1.5
        btn_widget.setFixedWidth(w)
        
        action_layout.addWidget(sensor_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(amplitud_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(periodo_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(btn_widget, alignment = Qt.AlignCenter)
        action_layout.addStretch()

        action_layout.setSpacing(0)
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        
        self.addWidget(action_widget, alignment = Qt.AlignCenter)
        self.addStretch()
        
        
        
    # Función para identificar giro en sentido horario
    def spin_clockwise(self):
        self.lbl_control.setText("CLOCKWISE")
        amplitud = int(self.spb_amplitud.text())
        periodo = int(self.edit_periodo.text())
        esp.giro_cw(self.ser, 5, amplitud, periodo)
            
    # Función para identificar giro en sentido antihorario
    def spin_countercw(self):
        self.lbl_control.setText("COUNTER CW")
        amplitud = int(self.spb_amplitud.text())
        periodo = int(self.edit_periodo.text())
        esp.giro_ccw(self.ser, 5, amplitud, periodo)
        
    # Función para identificar giro apagado
    def spin_off(self):
        self.lbl_control.setText("OFF")

    # Función para identificar cambio a homw
    def text_home(self):
        self.lbl_control.setText("HOME")
        
    # Función para cambio valor SpinBox
    def spb_amplitud_changed(self, val_vel):
        self.vel = val_vel

    # Función para enviar a HOME
    def send_home(self):
        esp.HOME_herramienta(self.ser)
        

        