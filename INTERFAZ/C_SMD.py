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
    QTableWidget,
    QTableWidgetItem,
    QDesktopWidget,
    QLineEdit,
    QCheckBox,
    QDoubleSpinBox)



class SMD(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        
        main_layout = QVBoxLayout()

        # Label 01: Etiqueta para Selección de Puerto COM
        lbl_smd = QLabel("SMD Válidos")
        lbl_smd.setAlignment(Qt.AlignCenter)
        lbl_smd.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_smd.sizeHint().width() + 10
        h = lbl_smd.sizeHint().height()
        lbl_smd.setFixedSize(w, h)
        main_layout.addWidget(lbl_smd, alignment = Qt.AlignCenter)

        # Tab Widget
        tab_widget = QTabWidget()
        
        table1= [
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
            {'Empaquetado': '01005', 'Componente': 'Resistencias, Capacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox': '0.04', 'Imagen': '-'},
        ]
        
        smd1 = QTableWidget(self)

        smd1.setColumnCount(6)
        
        smd1.setHorizontalHeaderLabels(table1[0].keys())
        smd1.setRowCount(len(table1))

        row = 0
        for e in table1:
            smd1.setItem(row, 0, QTableWidgetItem(e['Empaquetado']))
            smd1.setItem(row, 1, QTableWidgetItem(e['Componente']))
            smd1.setItem(row, 2, QTableWidgetItem(e['mm']))
            smd1.setItem(row, 3, QTableWidgetItem(e['in']))
            smd1.setItem(row, 4, QTableWidgetItem(e['Peso aprox']))
            smd1.setItem(row, 5, QTableWidgetItem(e['Imagen']))
            row += 1
            
        smd2 = QTableWidget(self)
        smd3 = QTableWidget(self)
        smd4 = QTableWidget(self)
        smd5 = QTableWidget(self)
        smd6 = QTableWidget(self)
        
        tab_widget.addTab(smd1, "General")
        tab_widget.addTab(smd2, "Resistores")
        tab_widget.addTab(smd3, "Capacitores")
        tab_widget.addTab(smd4, "LED")
        tab_widget.addTab(smd5, "Transistores")
        tab_widget.addTab(smd6, "Circuito Integrado")
        
        w = self.w - 200
        h = self.h -200
        
        smd1.setColumnWidth(0, w * 0.1)
        smd1.setColumnWidth(1, w * 0.3)
        smd1.setColumnWidth(2, w * 0.15)
        smd1.setColumnWidth(3, w * 0.15)
        smd1.setColumnWidth(4, w * 0.1)
        smd1.setColumnWidth(5, w * 0.2)
        
        
        tab_widget.setFixedSize(w, h)
        
        main_layout.addWidget(tab_widget, alignment = Qt.AlignCenter)
        
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
        
        
        self.setLayout(main_layout)
        
