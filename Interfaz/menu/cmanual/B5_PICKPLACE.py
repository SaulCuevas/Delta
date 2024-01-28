# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:19 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: PICK & PLACE
"""

import os
import sys
# Dirección de imagen
# path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    aux_path = os.path.join(path, 'Interfaz\code_aux')
else:
    aux_path = os.path.join(path, 'Interfaz/code_aux')
sys.path.insert(0, aux_path)

from PyQt5.QtCore import Qt,QTimer, QSize
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap, QFont, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDesktopWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QTabWidget,
    QLineEdit,
    QSlider,
    QCheckBox,
    QDoubleSpinBox,
    QSizePolicy)
import qtawesome as qta
from toggle import ToggleButton
import numpy as np

import ESP32_serial as esp

# Dirección de imagen
#path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    img_tool = os.path.join(path, 'imagenes\\tool_pp.png')
else:
    img_tool = os.path.join(path, 'imagenes/tool_pp.png')

class TOOL_P(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        print("\nCONTROL MANUAL: TOOL PICK & PLACE -> CREADA\n")
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        self.pnp_val = 0
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/15) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/20) # Valor de fuente 2 ajustado a tamaño pantalla
        self.icon_size = int(self.h/10) # Valor de icon size (button) ajustado a tamaño pantalla
        self.sw_size = int(self.h/8) # Valor de sw (button) ajustado a tamaño pantalla
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        action_layout = QVBoxLayout()
        action_widget = QWidget()
        action_widget.setLayout(action_layout)

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
    
        # Style Title Label
        st_lbl = "QLabel {"
        st_lbl += "background-color: white; "
        st_lbl += "border: 1px solid; "
        st_lbl += "font-family: Georgia; "
        st_lbl += f"font-size: {self.font_size1}pt; "
        st_lbl += "padding: 0px; "
        st_lbl += "}"

        # Style Normal Label
        st_normal = "QLabel {"
        st_normal += "border: 0px solid; "
        st_normal += "font-weight: bold; "
        st_normal += "font-family: Georgia; "
        st_normal += f"font-size: {self.font_size2}pt; "
        st_normal += "padding: 3px; "
        st_normal += "}"

        # Style SpinBox
        st_spb = "QSpinBox {"
        st_spb += "border: 1px solid; "
        st_spb += "font-family: Georgia; "
        st_spb += f"font-size: {self.font_size2}pt; "
        st_spb += "padding: 3px; "
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
        st_le += "padding: 0px; "
        st_le += "}"

        # Style Button
        st_btn = "QPushButton { "
        st_btn += "background-color: lightblue; "
        st_btn += "border-style: outset; "
        st_btn += "border-width: 2px; "
        st_btn += "border-radius: 5px; "
        st_btn += f"font-size: {self.font_size1}pt; "
        st_btn += "border-color: blue; "
        st_btn += "padding: 3px; }"
        
        st_btn += "QPushButton:hover { "
        st_btn += "background-color: rgb(0, 224, 224); "
        st_btn += "border-style: inset; } "
        
        st_btn += "QPushButton:pressed { "
        st_btn += "background-color: rgb(0, 0, 224); "
        st_btn += "border-style: inset; } "

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
        st_calib += "padding: 3px; }"
        
        st_calib += "QPushButton:hover { "
        st_calib += "background-color: rgb(10, 150, 150); "
        st_calib += "border-color: rgb(30, 255, 255); "
        st_calib += "border-style: groove; } "
        
        st_calib += "QPushButton:pressed { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset; } "
        
        st_calib += "QPushButton:checked { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset; } "
        
        st_calib += "QPushButton:disabled { "
        st_calib += "background-color: rgb(150, 150, 150); "
        st_calib += "border-style: dashed; "
        st_calib += "border-color: default; "
        st_calib += "border-width: 3px; "
        st_calib += "border-radius: 0px; } "

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
        action_layout.addWidget(self.lbl_control, alignment = Qt.AlignCenter)

        # Label 02: TEXTO CONTROL
        self.lbl_ch = QLabel("RAD/DEG")
        self.lbl_ch.adjustSize()
        self.lbl_ch.setStyleSheet(st_normal)
        top_layout.addWidget(self.lbl_ch, alignment = Qt.AlignCenter)
        
        # Switch 01: TOOGLE BUTTON para cambio de medida angulo en COORD LAYOUT
        self.sw_measure = ToggleButton(self.icon_size)    # Generar ToogleButton para cambio de angulo
        self.sw_measure.setStyleSheet("")    # Fijar estilo de widget
        self.sw_measure.clicked.connect(self.sw_angle)
        top_layout.addWidget(self.sw_measure, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MEASURE

        # Label 03: Texto Sensor
        self.lbl_sensor = QLabel("Sensor: ")
        self.lbl_sensor.setStyleSheet(st_normal)
        self.lbl_sensor.adjustSize()
        sensor_layout.addWidget(self.lbl_sensor, alignment = Qt.AlignCenter)

        # Edit Text 01: Lectura de Sensor
        self.edit_sensor = QLineEdit()
        self.edit_sensor.setStyleSheet(st_le)
        self.edit_sensor.setAlignment(Qt.AlignRight)
        self.edit_sensor.setReadOnly(True)
        w = 200
        h = self.edit_sensor.sizeHint().height() * 1.05
        self.edit_sensor.setFixedSize(w, h)
        sensor_layout.addWidget(self.edit_sensor, alignment = Qt.AlignCenter)

        # Label 04: Texto Radianes
        self.lbl_rad = QLabel("rad")
        self.lbl_rad.setStyleSheet(st_normal)
        self.lbl_rad.adjustSize()
        w = self.lbl_rad.sizeHint().width() * 1.1
        self.lbl_rad.setFixedWidth(w)
        sensor_layout.addWidget(self.lbl_rad, alignment = Qt.AlignCenter)

        # Label 05: Texto Posición
        self.lbl_angle = QLabel("Ángulo: ")
        self.lbl_angle.setStyleSheet(st_normal)
        self.lbl_angle.adjustSize()
        angle_layout.addWidget(self.lbl_angle, alignment = Qt.AlignCenter)

        # SpinBox 01: Control de Ángulo
        self.spb_angle = QSpinBox()
        self.spb_angle.setStyleSheet(st_spb)
        self.spb_angle.setMinimum(0)
        self.spb_angle.setMaximum(360)
        self.spb_angle.setSingleStep(1)
        self.spb_angle.setSuffix(" °")
        w = self.spb_angle.sizeHint().width() * 1.5
        h = int(0.4 * w)
        self.spb_angle.setFixedSize(w, h)
        self.spb_angle.setValue(0)
        # self.spb_angle.valueChanged.connect(self.spb_vel_changed)
        angle_layout.addWidget(self.spb_angle, alignment = Qt.AlignCenter)

        # Button 01: Enviar valor
        icon = qta.icon("mdi6.flag-triangle")
        self.btn_send = QPushButton(icon, "")
        self.btn_send.clicked.connect(self.move_pnp)
        self.btn_send.setStyleSheet(st_btn)
        self.btn_send.setIconSize(QSize(self.icon_size, self.icon_size))   # Ajustar tamaño de ícono
        w = self.btn_send.sizeHint().width() * 1.1
        h = self.btn_send.sizeHint().height() * 1.1
        self.btn_send.setFixedSize(w, h)
        angle_layout.addSpacing(10)
        angle_layout.addWidget(self.btn_send, alignment = Qt.AlignCenter)
        
        # Button 01: Activar Bomba de Vacío
        icon = qta.icon("mdi.wall-sconce-flat")
        self.btn_bv = QPushButton(icon, "")
        self.btn_bv.setIconSize(QSize(self.sw_size, self.sw_size))
        self.btn_bv.setStyleSheet(st_btn)
        w = self.btn_bv.sizeHint().width() * 1.1
        h = self.btn_bv.sizeHint().height() * 1.1
        self.btn_bv.setFixedSize(w, h)
        self.btn_bv.setCheckable(True)
        self.btn_bv.clicked.connect(self.sel_active)

        action_layout.addWidget(top_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(sensor_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(angle_widget, alignment = Qt.AlignCenter)
        action_layout.addWidget(self.btn_bv, alignment = Qt.AlignCenter)
        
        self.addStretch()
        self.addWidget(self.lbl, alignment = Qt.AlignCenter)
        self.addStretch()
        self.addWidget(action_widget, alignment = Qt.AlignCenter)
        self.addStretch()
        
    def sel_active(self):
        if self.btn_bv.isChecked():
            self.lbl_control.setText("ON")
            esp.encender_valvula(self.ser)
        else:
            self.lbl_control.setText("OFF")
            esp.apagar_valvula(self.ser)

    def move_pnp(self):
        x = self.spb_angle.value()
        angle = np.deg2rad(x)
        esp.mover_motor(self.ser, 4, angle)
    
    def sw_angle(self):
        if (self.sw_measure.toggle_on == False):
            self.pnp_val = self.pnp_val
            self.lbl_rad.setText("rad")
            text_pp = f"{self.pnp_val:.4f}"
        elif (self.sw_measure.toggle_on == True):
            self.pnp_val = np.rad2deg(self.pnp_val)
            self.lbl_rad.setText("°")
            text_pp = f"{self.pnp_val:.2f}"
        self.edit_sensor.setText(text_pp)        
        

        