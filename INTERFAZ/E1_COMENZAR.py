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
    QStackedLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QCheckBox,
    QDoubleSpinBox)
import matplotlib
matplotlib.use('Qt5Agg')




class ARCHIVOS(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        
        self.stacked_layout = QStackedLayout()
        
        main_layout = QVBoxLayout()
        table_layout = QVBoxLayout()
        
        file_layout = QHBoxLayout()
        btns_layout = QHBoxLayout()
        layers_layout = QHBoxLayout()
        
        file_widget = QWidget()
        btns_widget = QWidget()
        layers_widget = QWidget()
        
    # ----- MAIN LAYOUT -------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_comenzar = QLabel("ARCHIVOS")
        lbl_comenzar.setAlignment(Qt.AlignCenter)
        lbl_comenzar.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_comenzar.sizeHint().width() + 10
        h = lbl_comenzar.sizeHint().height()
        lbl_comenzar.setFixedSize(w, h)
        main_layout.addWidget(lbl_comenzar, alignment = Qt.AlignCenter)
        
        file_widget.setLayout(file_layout)
        btns_widget.setLayout(btns_layout)
        layers_widget.setLayout(layers_layout)
        main_layout.addWidget(file_widget, alignment = Qt.AlignCenter)
        main_layout.addWidget(btns_widget, alignment = Qt.AlignCenter)
        main_layout.addWidget(layers_widget, alignment = Qt.AlignCenter)


        # Label 01: Etiqueta previa a nombre carpeta
        self.lbl_carp = QLabel("Carpeta: ")
        file_layout.addWidget(self.lbl_carp, alignment = Qt.AlignCenter)
        
        # Line Edit: SELECCIÓN DE CARPETA
        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(True)
        h = self.lineEdit.sizeHint().height()
        self.lineEdit.setFixedSize(self.w * 0.7, h)
        file_layout.addWidget(self.lineEdit, alignment = Qt.AlignCenter)
        
        
        # BUTTON 1: Seleccionar carpeta
        self.btn_file = QPushButton("File")
        style = "QPushButton { "
        style += "background-color: rgb(41, 128, 185); "
        style += "border-style: outset; "
        style += "border-width: 5px; "
        style += "border-radius: 5px; "
        style += "border-color: rgb(26, 82, 118); "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 12pt; "
        # style += "margin: 10px; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(155, 89, 182); "
        style += "border-color: rgb(187, 143, 206); "
        style += "border-style: groove } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(192, 57, 43); "
        style += "border-color: rgb(231, 76, 60); "
        style += "border-style: inset } "
        
        self.btn_file.setStyleSheet(style)
        w = self.btn_file.sizeHint().width()
        h = self.btn_file.sizeHint().height()
        self.btn_file.setFixedSize(w + 10, h)
        file_layout.addWidget(self.btn_file, alignment = Qt.AlignCenter)
        
        self.btn_file.clicked.connect(self.open_file)
        
        
        # BUTTON 2: ACTUALIZAR
        self.btn_act = QPushButton("Actualizar")
        style = "QPushButton { "
        style += "background-color: rgb(231, 76, 60); "
        style += "border-style: outset; "
        style += "border-width: 3px; "
        style += "border-radius: 5px; "
        style += "border-color: rgb(255, 20, 20); "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 20pt; "
        # style += "margin: 10px; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(20, 80, 160); "
        style += "border-color: rgb(0, 100, 255); "
        style += "border-style: groove } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(40, 160, 40); "
        style += "border-color: rgb(50, 255, 50); "
        style += "border-style: inset } "
        
        style += "QPushButton:disabled { "
        style += "background-color: rgb(150, 150, 150); "
        style += "border-style: dashed; "
        style += "border-color: default; "
        style += "border-width: 3px; "
        style += "border-radius: 0px } "
        
        
        self.btn_act.setStyleSheet(style)
        w = self.btn_act.sizeHint().width()
        h = self.btn_act.sizeHint().height()
        self.btn_act.setFixedSize(w + 25, h + 10)
        self.btn_act.clicked.connect(self.actualizar)
        btns_layout.addStretch(0)
        btns_layout.addWidget(self.btn_act, alignment = Qt.AlignCenter)
        
        # BUTTON 3: CONTINUAR
        self.btn_continuar = QPushButton("Continuar")        
        self.btn_continuar.setStyleSheet(style)
        w = self.btn_continuar.sizeHint().width()
        h = self.btn_continuar.sizeHint().height()
        self.btn_continuar.setFixedSize(w + 25, h + 10)
        self.btn_continuar.clicked.connect(self.continuar)
        btns_layout.addStretch(0)
        btns_layout.addWidget(self.btn_continuar, alignment = Qt.AlignCenter)
        btns_layout.addStretch(0)
        # btns_layout.setContentsMargins(0, 0, 0, 0)
        btns_widget.setFixedWidth(self.w)
        
        
        # BUTTON 4: TOP LAYER
        self.btn_top = QPushButton("Top")
        style = "QPushButton { "
        style += "background-color: rgb(40, 160, 40); "
        style += "border-style: outset; "
        style += "border-width: 3px; "
        style += "border-radius: 5px; "
        style += "border-color: rgb(50, 255, 50); "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 30pt; "
        # style += "margin: 10px; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(10, 150, 150); "
        style += "border-color: rgb(30, 255, 255); "
        style += "border-style: groove } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(100, 30, 150); "
        style += "border-color: rgb(150, 0, 255); "
        style += "border-style: inset } "
        
        style += "QPushButton:checked { "
        style += "background-color: rgb(100, 30, 150); "
        style += "border-color: rgb(150, 0, 255); "
        style += "border-style: inset } "
        
        style += "QPushButton:disabled { "
        style += "background-color: rgb(150, 150, 150); "
        style += "border-style: dashed; "
        style += "border-color: default; "
        style += "border-width: 3px; "
        style += "border-radius: 0px } "
        
        
        self.btn_top.setStyleSheet(style)
        w1 = self.btn_top.sizeHint().width()
        h1 = self.btn_top.sizeHint().height()
        self.btn_top.setCheckable(True)
        self.btn_top.clicked.connect(self.sel_top)
        layers_layout.addStretch(0)
        layers_layout.addWidget(self.btn_top, alignment = Qt.AlignCenter)
        
        # BUTTON 5: BOTTOM LAYER
        self.btn_bottom = QPushButton("Bottom")        
        self.btn_bottom.setStyleSheet(style)
        w2 = self.btn_bottom.sizeHint().width()
        h2 = self.btn_bottom.sizeHint().height()
        if (w1 > w2):
            self.btn_top.setFixedSize(w1 + 150, h1 + 50)
            self.btn_bottom.setFixedSize(w1 + 150, h1 + 50)
        else:
            self.btn_top.setFixedSize(w2 + 150, h2 + 50)
            self.btn_bottom.setFixedSize(w2 + 150, h2 + 50)
        self.btn_bottom.setCheckable(True)
        self.btn_bottom.clicked.connect(self.sel_bottom)
        layers_layout.addStretch(0)
        layers_layout.addWidget(self.btn_bottom, alignment = Qt.AlignCenter)
        layers_layout.addStretch(0)
        # btns_layout.setContentsMargins(0, 0, 0, 0)
        layers_widget.setFixedWidth(self.w)
        
        
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
        
        # Inicio botones desactivados
        self.btn_act.setDisabled(True)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setDisabled(True)
        self.btn_bottom.setDisabled(True)
        
    # ----- TABLE LAYOUT ------------------------------------------------------
        
        # Table Widget
        comps_table = QTableWidget()
        
        labels = ['Nombre', 'Tipo', 'Valor', 'Empaquetado', 'Imagen']
        
        comps_table.setColumnCount(len(labels))
        comps_table.setRowCount(1)
        comps_table.setHorizontalHeaderLabels(labels)
        comps_table.verticalHeader().setVisible(True)
        comps_table.horizontalHeader().setVisible(True)
        
        w = self.w - 200
        h = self.h -200
        comps_table.setFixedSize(w, h)
        
        table_layout.addWidget(comps_table, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_back = QPushButton("Atrás")

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
        
        self.btn_back.setStyleSheet(style)
        self.btn_back.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_back.sizeHint().width() + 100
        h = self.btn_back.sizeHint().height() + 5
        self.btn_back.setFixedSize(w, h)
        self.btn_back.clicked.connect(self.back)
        table_layout.addWidget(self.btn_back, alignment = Qt.AlignCenter)
        
    # ----- CONFIGURACION -----------------------------------------------------
        main_widget = QWidget()
        table_widget = QWidget()
        main_widget.setLayout(main_layout)
        table_widget.setLayout(table_layout)
        self.stacked_layout.addWidget(main_widget)
        self.stacked_layout.addWidget(table_widget)
        
        self.setLayout(self.stacked_layout)
        
        
    def open_file(self):
        # self.file_name = QFileDialog.getOpenFileName(None, "Open", "", "CSV Files (*.csv)")
        self.file_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.lineEdit.setText(self.file_name)
        self.btn_act.setDisabled(False)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setDisabled(True)
        self.btn_bottom.setDisabled(True)
        
    def actualizar(self):
        self.btn_top.setDisabled(False)
        self.btn_bottom.setDisabled(False)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setChecked(False)
        self.btn_bottom.setChecked(False)
        
    def sel_top(self):
        if self.btn_top.isChecked():
            self.btn_bottom.setDisabled(True)
            self.btn_continuar.setDisabled(False)
        else:
            self.btn_bottom.setDisabled(False)
            self.btn_continuar.setDisabled(True)
        
    def sel_bottom(self):
        if self.btn_bottom.isChecked():
            self.btn_top.setDisabled(True)
            self.btn_continuar.setDisabled(False)
        else:
            self.btn_top.setDisabled(False)
            self.btn_continuar.setDisabled(True)
            
    def continuar(self):
        self.stacked_layout.setCurrentIndex(1)
        
    def back(self):
        self.stacked_layout.setCurrentIndex(0)
