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

@author: Spect
"""

import sys
from PyQt5.QtCore import Qt,QTimer
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDesktopWidget,
    QHBoxLayout,
    QVBoxLayout,
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
from toggle import ToggleButton


class CMANUAL(QWidget):
    # Constructor
    def __init__(self):
# ------- Configuración pantalla GUI --------------------------------------
        super().__init__()
        
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        
        # Layouts Principales
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        
        # Layouts Pantalla Control Manual
        h1_layout = QHBoxLayout()
        h2_layout = QHBoxLayout()
        
        # Layouts para Horizontal 1
        v1_layout = QVBoxLayout()
        v2_layout = QVBoxLayout()
        v3_layout = QVBoxLayout()
        v4_layout = QVBoxLayout()
        
        # Layouts para Horizontal 2
        v5_layout = QVBoxLayout()
        v6_layout = QVBoxLayout()
    
# ------- TITLE -----------------------------------------------------------

        main_layout.addStretch(1)

        # Label TITLE: Títutlo de WIDGET - CONTROL MANUAL
        lbl_cmanual = QLabel("CONTROL MANUAL")
        lbl_cmanual.setAlignment(Qt.AlignCenter)
        
        style = "QLabel { "
        style += "background-color: lightgreen; "
        style += "border-style: solid; "
        style += "border-width: 1px; "
        style += "border-color: black; "
        style += "font-weight: normal; "
        style += "font-family: Times New Roman; "
        style += "font-size: 8pt; "
        style += "padding: 0px }"
        
        lbl_cmanual.setStyleSheet(style)
        w = lbl_cmanual.sizeHint().width() + 10
        h = lbl_cmanual.sizeHint().height()
        lbl_cmanual.setFixedSize(w, h)
        main_layout.addWidget(lbl_cmanual, alignment = Qt.AlignCenter)
        main_layout.addStretch(1)

# ------- TOP LAYOUT ------------------------------------------------------
        
        top_layout.addStretch(1)
        
        top_coord = QLabel("COORD:")
        top_coord.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(top_coord)
        
        self.top_typecrd = QLabel("R")
        self.top_typecrd.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(self.top_typecrd)
        
        top_layout.addStretch(3)
        
        top_herr = QLabel("TOOL:")
        top_herr.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(top_herr)
        
        self.top_typeh = QLabel("N/C/S/P")
        self.top_typeh.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(self.top_typeh)
        
        top_layout.addStretch(3)
        
        top_vel = QLabel("VEL:")
        top_vel.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(top_vel)
        
        self.top_typev = QLabel("1/2/3/4")
        self.top_typev.setStyleSheet("border-width: 0px;")
        top_layout.addWidget(self.top_typev)
        
        top_layout.addStretch(1)
        
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        
        style = "QWidget { "
        style += "color: white; "
        style += "background-color: blue; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: black; "
        style += "border-spacing: 0px 0px; "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 12pt; "
        style += "margin: 0px; "
        style += "padding: 0px }"
        
        top_widget.setStyleSheet(style)
        # print(self.w)
        top_widget.setFixedWidth(self.w - 100)
        
        main_layout.addWidget(top_widget, alignment = Qt.AlignCenter)
        main_layout.addStretch(0)
        
# ------- H1 LAYOUT -------------------------------------------------------
    
    # ----- LAYOUT VERTICAL 1 ---------------------------------------------
    
        # Checkbox HERRAMIENTA
        self.chb_tool = QCheckBox("Herramienta:")
        # self.chb_tool.stateChanged.connect(self.click_tool)
        style = "QCheckBox { "
        style += "border: 1px solid black; "
        style += "background-color: bisque; "
        style += "font-weight: bold; "
        style += "font-family: Times New Roman; "
        style += "font-size: 11pt;}"
        self.chb_tool.setStyleSheet(style)
        w = self.chb_tool.sizeHint().width()
        h = self.chb_tool.sizeHint().height()
        self.chb_tool.setFixedSize(w, h)
        v1_layout.addWidget(self.chb_tool, alignment = Qt.AlignCenter)
        
        # ComboBox HERRAMIENTA
        self.cb_tool = QComboBox()
        items = ["NINGUNA", "CÁMARA", "SOLDADURA", "PICK & PLACE"]
        self.cb_tool.addItems(items)
        # self.cb_tool.currentTextChanged(self.change_tool)
        self.cb_tool.activated.connect(self.change_tool)
        style = "QComboBox { "
        style += "border: 1px solid black; "
        # style += "background-color: bisque; "
        # style += "margin-bottom: 10px; "
        # style += "font-weight: bold; "
        style += "font-family: Times New Roman; "
        style += "font-size: 11pt;}"
        self.cb_tool.setStyleSheet(style)
        self.cb_tool.adjustSize()
        w = self.cb_tool.sizeHint().width() + 10
        h = self.cb_tool.sizeHint().height()
        self.cb_tool.setFixedSize(w, h)
        v1_layout.addWidget(self.cb_tool, alignment = Qt.AlignCenter)
        
        v1_widget = QWidget()
        v1_widget.setLayout(v1_layout)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 1px; "
        style += "border-radius: 3px; "
        style += "border-color: black; "
        style += "font: 14px; "
        style += "padding: 2px }"
        
        v1_widget.setStyleSheet(style)
        
        w = v1_widget.sizeHint().width()
        h = v1_widget.sizeHint().height()
        v1_widget.setFixedSize(w, h)
        
    # ----- LAYOUT VERTICAL 2 ---------------------------------------------
        
        # Checkbox VELOCIDAD
        self.chb_vel = QCheckBox("Velocidad:")
        # self.chb_vel.stateChanged.connect(self.click_tool)
        style = "QCheckBox { "
        style += "border: 1px solid black; "
        style += "background-color: lightyellow; "
        # style += "margin-bottom: 10px; "
        style += "font-weight: bold; "
        style += "font-family: Times New Roman; "
        style += "font-size: 11pt;}"
        self.chb_vel.setStyleSheet(style)
        w = self.chb_vel.sizeHint().width()
        h = self.chb_vel.sizeHint().height()
        self.chb_vel.setFixedSize(w, h)
        v2_layout.addWidget(self.chb_vel, alignment = Qt.AlignCenter)
        
        # Slider VELOCIDAD
        self.sld_vel = QSlider(Qt.Horizontal)
        self.sld_vel.setRange(1,4)
        self.sld_vel.setTickPosition(QSlider.TicksBelow)
        self.sld_vel.setTickInterval(1)
        self.sld_vel.valueChanged.connect(self.change_vel)
        v2_layout.addWidget(self.sld_vel, alignment = Qt.AlignCenter)
        
        v2_widget = QWidget()
        v2_widget.setLayout(v2_layout)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 1px; "
        style += "border-radius: 3px; "
        style += "border-color: black; "
        style += "font: 14px; "
        style += "padding: 2px }"
        
        v2_widget.setStyleSheet(style)
        
        w = v2_widget.sizeHint().width()
        h = v2_widget.sizeHint().height()
        v2_widget.setFixedSize(w, h)
    
    # ----- LAYOUT VERTICAL 3 ---------------------------------------------
    
        x_layout = QHBoxLayout()
        y_layout = QHBoxLayout()
        z_layout = QHBoxLayout()
        
        x_widget = QWidget()
        y_widget = QWidget()
        z_widget = QWidget()
        
        x_widget.setLayout(x_layout)
        y_widget.setLayout(y_layout)
        z_widget.setLayout(z_layout)
        
        x_layout.setContentsMargins(0, 0, 0, 0)
        y_layout.setContentsMargins(0, 0, 0, 0)
        z_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label COORDENADAS ACTUALES
        act_coord = QLabel("ACTUALES")
        v3_layout.addWidget(act_coord, alignment = Qt.AlignCenter)
        
        # Label COORDENADAS X/M1
        self.lbl_x = QLabel("X:")
        self.lbl_x.setAlignment(Qt.AlignRight)
        self.lbl_x.setFixedWidth(50)
        x_layout.addWidget(self.lbl_x)
        
        # Valor COORDENADAS X/M1
        self.x_coord = QLineEdit("00.00")
        self.x_coord.setAlignment(Qt.AlignRight)
        self.x_coord.setReadOnly(True)
        self.x_coord.setFixedWidth(100)
        x_layout.addWidget(self.x_coord)
        
        # Label COORDENADAS Y/M2
        self.lbl_y = QLabel("Y:")
        self.lbl_y.setAlignment(Qt.AlignRight)
        self.lbl_y.setFixedWidth(50)
        y_layout.addWidget(self.lbl_y)
        
        # Valor COORDENADAS Y/M2
        self.y_coord = QLineEdit("00.00")
        self.y_coord.setAlignment(Qt.AlignRight)
        self.y_coord.setReadOnly(True)
        self.y_coord.setFixedWidth(100)
        y_layout.addWidget(self.y_coord)
        
        # Label COORDENADAS Z/M3
        self.lbl_z = QLabel("Z:")
        self.lbl_z.setAlignment(Qt.AlignRight)
        self.lbl_z.setFixedWidth(50)
        z_layout.addWidget(self.lbl_z)
        
        # Valor COORDENADAS Z/M3
        self.z_coord = QLineEdit("00.00")
        self.z_coord.setAlignment(Qt.AlignRight)
        self.z_coord.setReadOnly(True)
        self.z_coord.setFixedWidth(100)
        z_layout.addWidget(self.z_coord)
        
        v3_layout.addWidget(x_widget)
        v3_layout.addWidget(y_widget)
        v3_layout.addWidget(z_widget)
        v3_layout.setSpacing(0)
        v3_layout.setContentsMargins(0, 0, 0, 0)
            
        v3_widget = QWidget()
        v3_widget.setLayout(v3_layout)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 1px; "
        style += "border-radius: 3px; "
        style += "border-color: black; "
        style += "font: bold 14px; "
        style += "padding: 2px }"
        
        v3_widget.setStyleSheet(style)
        
        w = x_widget.sizeHint().width()
        h = x_widget.sizeHint().height()
        x_widget.setFixedSize(w, h)
        y_widget.setFixedSize(w, h)
        z_widget.setFixedSize(w, h)
        
        w = v3_widget.sizeHint().width()
        h = v3_widget.sizeHint().height()
        v3_widget.setFixedSize(w, h)
    
    # ----- LAYOUT VERTICAL 4 ---------------------------------------------
    
        # Checkbox NUEVA POSICIÓN
        self.chb_new = QCheckBox("Nueva:")
        # self.chb_new.stateChanged.connect(self.click_tool)
        w = self.chb_new.sizeHint().width()
        h = self.chb_new.sizeHint().height()
        self.chb_new.setFixedSize(w + 20, h)
        v4_layout.addWidget(self.chb_new, alignment = Qt.AlignCenter)
        
        # Valor NUEVAS COORD X/M1
        self.x_new = QLineEdit("00.00")
        self.x_new.setAlignment(Qt.AlignRight)
        self.x_new.setFixedWidth(100)
        v4_layout.addWidget(self.x_new, alignment = Qt.AlignCenter)
        
        # Valor NUEVAS COORD Y/M2
        self.y_new = QLineEdit("00.00")
        self.y_new.setAlignment(Qt.AlignRight)
        self.y_new.setFixedWidth(100)
        v4_layout.addWidget(self.y_new, alignment = Qt.AlignCenter)
        
        # Valor NUEVAS COORD Z/M3
        self.z_new = QLineEdit("00.00")
        self.z_new.setAlignment(Qt.AlignRight)
        self.z_new.setFixedWidth(100)
        v4_layout.addWidget(self.z_new, alignment = Qt.AlignCenter)
    
        v4_widget = QWidget()
        v4_widget.setLayout(v4_layout)
        
        v4_layout.setSpacing(0)
        v4_layout.setContentsMargins(0, 0, 0, 0)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: lightblue; "
        style += "border-style: outset; "
        style += "border-width: 1px; "
        style += "border-radius: 3px; "
        style += "border-color: black; "
        style += "font: 14px; "
        style += "padding: 2px }"
        
        v4_widget.setStyleSheet(style)
        
        w = v4_widget.sizeHint().width()
        h = v4_widget.sizeHint().height()
        v4_widget.setFixedSize(w, h)
    
    # ----- CONFIG LAYOUT -------------------------------------------------
    
        h1_layout.addStretch(2)
        h1_layout.addWidget(v1_widget)
        h1_layout.addStretch(2)
        h1_layout.addWidget(v2_widget)
        h1_layout.addStretch(2)
        h1_layout.addWidget(v3_widget)
        h1_layout.addStretch(1)
        h1_layout.addWidget(v4_widget)
        h1_layout.addStretch(2)
        
        h1_layout.setContentsMargins(0, 0, 0, 0)
        
        h1_widget = QWidget()
        h1_widget.setLayout(h1_layout)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: rgb(220, 220, 220); "
        style += "border-style: solid; "
        style += "border-width: 1px; "
        style += "border-bottom-width: 0px; "
        style += "border-radius: 0px; "
        style += "border-color: black; "
        style += "font-weight: normal; "
        style += "font-family: Georgia; "
        style += "font-size: 12pt; "
        style += "margin: 0px; "
        style += "padding: 0px }"
        
        h1_widget.setStyleSheet(style)
        h1_widget.setFixedWidth(self.w - 100)
        
        main_layout.addWidget(h1_widget, alignment = Qt.AlignCenter)
        main_layout.addStretch(0)
    
# ------- H2 LAYOUT -------------------------------------------------------
    
    # ----- LAYOUT VERTICAL 5 ---------------------------------------------
    
        x_btn_layout = QHBoxLayout()
        y_btn_layout = QHBoxLayout()
        z_btn_layout = QHBoxLayout()
        sw_coord_layout = QHBoxLayout()

        x_btn_widget = QWidget()
        y_btn_widget = QWidget()
        z_btn_widget = QWidget()
        sw_coord_widget = QWidget()

        x_btn_widget.setLayout(x_btn_layout)      
        y_btn_widget.setLayout(y_btn_layout)      
        z_btn_widget.setLayout(z_btn_layout)      
        sw_coord_widget.setLayout(sw_coord_layout)
        
        # BUTTON X+ : Desplazamiento en X positivo coordenadas rectangulares
        self.btn_xp = QPushButton("X+")
        style = "QPushButton { "
        style += "background-color: rgb(41, 128, 185); "
        style += "border-style: outset; "
        style += "border-width: 5px; "
        style += "border-radius: 20px; "
        style += "border-color: rgb(26, 82, 118); "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 25pt; "
        # style += "margin: 10px; "
        style += "padding: 10px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(155, 89, 182); "
        style += "border-color: rgb(187, 143, 206); "
        style += "border-style: groove } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(192, 57, 43); "
        style += "border-color: rgb(231, 76, 60); "
        style += "border-style: inset } "
        
        self.btn_xp.setStyleSheet(style)
        w = self.btn_xp.sizeHint().width()
        self.btn_xp.setFixedSize(w + 10, w)
        x_btn_layout.addWidget(self.btn_xp, alignment = Qt.AlignCenter)
        
        # BUTTON X- : Desplazamiento en X negativo coordenadas rectangulares
        self.btn_xn = QPushButton("X-")
        self.btn_xn.setStyleSheet(style)
        self.btn_xn.setFixedSize(w + 10, w)
        x_btn_layout.addWidget(self.btn_xn, alignment = Qt.AlignCenter)
        
        # BUTTON Y+ : Desplazamiento en Y positivo coordenadas rectangulares
        self.btn_yp = QPushButton("Y+")
        self.btn_yp.setStyleSheet(style)
        self.btn_yp.setFixedSize(w + 10, w)
        y_btn_layout.addWidget(self.btn_yp, alignment = Qt.AlignCenter)
        
        # BUTTON Y- : Desplazamiento en Y negativo coordenadas rectangulares
        self.btn_yn = QPushButton("Y-")
        self.btn_yn.setStyleSheet(style)
        self.btn_yn.setFixedSize(w + 10, w)
        y_btn_layout.addWidget(self.btn_yn, alignment = Qt.AlignCenter)
        
        # BUTTON Z+ : Desplazamiento en Z positivo coordenadas rectangulares
        self.btn_zp = QPushButton("Z+")
        self.btn_zp.setStyleSheet(style)
        self.btn_zp.setFixedSize(w + 10, w)
        z_btn_layout.addWidget(self.btn_zp, alignment = Qt.AlignCenter)
        
        # BUTTON Z- : Desplazamiento en Z negativo coordenadas rectangulares
        self.btn_zn = QPushButton("Z-")
        self.btn_zn.setStyleSheet(style)
        self.btn_zn.setFixedSize(w + 10, w)
        z_btn_layout.addWidget(self.btn_zn, alignment = Qt.AlignCenter)
        
        # SWITCH: TOOGLE BUTTON CAMBIO DE COORDENADAS
        self.sw_coord = ToggleButton()
        self.sw_coord.clicked.connect(self.change_coord)      
        sw_coord_layout.addWidget(self.sw_coord, alignment = Qt.AlignCenter)
        
        self.lbl_typecrd = QLabel("RECTANGULARES")
        self.lbl_typecrd.setAlignment(Qt.AlignCenter)
        style = "QLabel { "
        style += "font-family: Georgia; "
        style += "font-size: 15pt; "
        style += "padding: 0px }"
        self.lbl_typecrd.setStyleSheet(style)
        w = self.lbl_typecrd.sizeHint().width() + 10
        h = self.lbl_typecrd.sizeHint().height() + 10
        self.lbl_typecrd.setFixedSize(w, h)
        sw_coord_layout.addWidget(self.lbl_typecrd, alignment = Qt.AlignCenter)
        
        v5_layout.addWidget(x_btn_widget, alignment = Qt.AlignCenter)
        v5_layout.addWidget(y_btn_widget, alignment = Qt.AlignCenter)
        v5_layout.addWidget(z_btn_widget, alignment = Qt.AlignCenter)
        v5_layout.addWidget(sw_coord_widget, alignment = Qt.AlignCenter)   
        v5_layout.setSpacing(0)
        v5_layout.setContentsMargins(0, 0, 0, 0)
        
        w = sw_coord_widget.sizeHint().width()
        h = sw_coord_widget.sizeHint().height()
        bh = x_btn_widget.sizeHint().height()
        x_btn_widget.setFixedSize(w, bh)
        y_btn_widget.setFixedSize(w, bh)
        z_btn_widget.setFixedSize(w, bh)
        sw_coord_widget.setFixedSize(w, h)
    
        v5_widget = QWidget()
        v5_widget.setLayout(v5_layout)
        
        w = v5_widget.sizeHint().width()
        h = v5_widget.sizeHint().height()
        v5_widget.setFixedSize(w, h)
    
    # ----- LAYOUT VERTICAL 6 ---------------------------------------------
    
        # Label PANEL DE HERRAMIENTA
        lbl_panel = QLabel("Panel de Herramientas")
        v6_layout.addWidget(lbl_panel, alignment = Qt.AlignCenter)
    
        v6_widget = QWidget()
        v6_widget.setLayout(v6_layout)
        
    # ----- CONFIG LAYOUT -------------------------------------------------
        
        h2_layout.addWidget(v5_widget)
        h2_layout.addWidget(v6_widget)
        
        h2_widget = QWidget()
        h2_widget.setLayout(h2_layout)
        
        style = "QWidget { "
        style += "color: black; "
        style += "background-color: rgb(220, 220, 220); "
        style += "border-style: solid; "
        style += "border-width: 1px; "
        style += "border-radius: 0px; "
        style += "border-color: black; "
        style += "font-weight: normal; "
        style += "font-family: Georgia; "
        style += "font-size: 12pt; "
        style += "margin: 0px; "
        style += "padding: 0px }"
        
        h2_widget.setStyleSheet(style)
        h2_widget.setFixedWidth(self.w - 100)
        
        main_layout.addWidget(h2_widget, alignment = Qt.AlignCenter)
        main_layout.addStretch(2)
    
# ------- SALIDA ----------------------------------------------------------
        
        # Button 01: Inicio de programa
        self.btn_start = QPushButton("Volver")

        style = "QPushButton { "
        style += "background-color: lightgreen; "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: green; "
        # style += "font: bold 14px; "
        style += "padding: 2px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(224, 224, 0); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(224, 0, 0); "
        style += "border-style: inset } "
        
        self.btn_start.setStyleSheet(style)
        self.btn_start.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_start.sizeHint().width() + 100
        h = self.btn_start.sizeHint().height() + 5
        self.btn_start.setFixedSize(w, h)
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)
        main_layout.addStretch(1)
        
# ------- MAIN LAYOUT -----------------------------------------------------
        
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
    
    
# ------- FUNCIONES ADICIONALES -------------------------------------------
    
    # FUNCIÓN PARA CAMBIO DE COORDENADAS
    def change_coord(self, on_off):
        if on_off == False:
            self.top_typecrd.setText('R')
            self.lbl_x.setText("X:")
            self.lbl_y.setText("Y:")
            self.lbl_z.setText("Z:")
            self.lbl_typecrd.setText('RECTANGULARES')
        else:
            self.top_typecrd.setText('M')
            self.lbl_x.setText("M1:")
            self.lbl_y.setText("M2:")
            self.lbl_z.setText("M3:")
            self.lbl_typecrd.setText('MOTORES')
    
    # FUNCIÓN PARA CAMBIO DE HERRAMIENTA
    def change_tool(self, x):
        value = self.cb_tool.currentText()
        if value == "NINGUNA":
            self.top_typeh.setText("N")
        elif value == "CÁMARA":
            self.top_typeh.setText("C")
        elif value == "SOLDADURA":
            self.top_typeh.setText("S")
        elif value == "PICK & PLACE":
            self.top_typeh.setText("P")
            
    # FUNCIÓN PARA CAMBIO DE VELOCIDAD
    def change_vel(self, value):
        # print(value)
        if value == 1:
            self.top_typev.setText("1")
        elif value == 2:
            self.top_typev.setText("2")
        elif value == 3:
            self.top_typev.setText("3")
        elif value == 4:
            self.top_typev.setText("4")
        
