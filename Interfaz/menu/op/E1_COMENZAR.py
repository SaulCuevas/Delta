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

import interprete_gerber as gbr
import special_table as tbl

from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap, QFont, QIcon
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
    QDialog,
    QProgressDialog,
    QLineEdit,
    QCheckBox,
    QDoubleSpinBox)

import qtawesome as qta
import time

      

class ARCHIVOS(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        
        # self.thread = ProgressThread()
        
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        
        self.top = True
        
        self.stacked_layout = QStackedLayout()
        
        main_layout = QVBoxLayout()
        table_layout = QVBoxLayout()
        pcb_layout = QVBoxLayout()
        final_layout = QVBoxLayout()
        
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
        w = lbl_comenzar.sizeHint().width() * 1.1
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
        w = self.btn_file.sizeHint().width() * 1.1
        h = self.btn_file.sizeHint().height()
        self.btn_file.setFixedSize(w, h)
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
        w = self.btn_act.sizeHint().width() * 1.2
        h = self.btn_act.sizeHint().height() * 1.1
        self.btn_act.setFixedSize(w, h)
        self.btn_act.clicked.connect(self.actualizar)
        btns_layout.addStretch(0)
        btns_layout.addWidget(self.btn_act, alignment = Qt.AlignCenter)
        
        # BUTTON 3: CONTINUAR
        self.btn_continuar = QPushButton("Continuar")        
        self.btn_continuar.setStyleSheet(style)
        w = self.btn_continuar.sizeHint().width() * 1.2
        h = self.btn_continuar.sizeHint().height() * 1.1
        self.btn_continuar.setFixedSize(w, h)
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
        w = self.btn_start.sizeHint().width() * 1.5
        h = self.btn_start.sizeHint().height() * 1.05
        self.btn_start.setFixedSize(w, h)
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)
        
        # Inicio botones desactivados
        self.btn_act.setDisabled(True)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setDisabled(True)
        self.btn_bottom.setDisabled(True)
        
    # ----- TABLE LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_table = QLabel("COMPONENTES")
        lbl_table.setAlignment(Qt.AlignCenter)
        lbl_table.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_table.sizeHint().width() * 1.1
        h = lbl_table.sizeHint().height()
        lbl_table.setFixedSize(w, h)
        table_layout.addWidget(lbl_table, alignment = Qt.AlignCenter)
    
        # Table Widget
        self.comps_table = tbl.ReorderableTable()
        
        labels = ['Nombre', 'Tipo', 'Valor', 'Empaquetado', 'Imagen']
        
        self.comps_table.setColumnCount(len(labels))
        self.comps_table.setRowCount(1)
        self.comps_table.setHorizontalHeaderLabels(labels)
        self.comps_table.verticalHeader().setVisible(True)
        self.comps_table.horizontalHeader().setVisible(True)
        
        w = self.w - 200
        h = self.h - 200
        self.comps_table.setFixedSize(w, h)
        
        table_layout.addWidget(self.comps_table, alignment = Qt.AlignCenter)
        
        btn_table_layout = QHBoxLayout()
        btn_table_widget = QWidget()
        
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
        w = self.btn_back.sizeHint().width() * 1.5
        h = self.btn_back.sizeHint().height() * 1.05
        self.btn_back.setFixedSize(w, h)
        self.btn_back.clicked.connect(self.back)
        btn_table_layout.addStretch(0)
        btn_table_layout.addWidget(self.btn_back, alignment = Qt.AlignCenter)
        btn_table_layout.addStretch(0)
        
        # Button 02: Continuar programa
        self.btn_cont = QPushButton("Continuar")
        self.btn_cont.setStyleSheet(style)
        self.btn_cont.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_cont.sizeHint().width() * 1.5
        h = self.btn_cont.sizeHint().height() * 1.05
        self.btn_cont.setFixedSize(w, h)
        self.btn_cont.clicked.connect(self.cont)
        btn_table_layout.addWidget(self.btn_cont, alignment = Qt.AlignCenter)
        btn_table_layout.addStretch(0)
        
        btn_table_widget.setLayout(btn_table_layout)
        btn_table_widget.setFixedWidth(self.w)
        
        table_layout.addWidget(btn_table_widget, alignment = Qt.AlignCenter)

    # ----- PCB LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_pcb = QLabel("PCB")
        lbl_pcb.setAlignment(Qt.AlignCenter)
        lbl_pcb.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_pcb.sizeHint().width() * 1.1
        h = lbl_pcb.sizeHint().height()
        lbl_pcb.setFixedSize(w, h)
        pcb_layout.addWidget(lbl_pcb, alignment = Qt.AlignCenter)
    
        # Image Widget
        self.lbl = QLabel()
        pcb_layout.addWidget(self.lbl, alignment = Qt.AlignCenter)
        
        
        btn_pcb_layout = QHBoxLayout()
        btn_pcb_widget = QWidget()
        
        # Button 01: Inicio de programa
        self.btn_pcb_back = QPushButton("Atrás")

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
        
        self.btn_pcb_back.setStyleSheet(style)
        self.btn_pcb_back.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_pcb_back.sizeHint().width() * 1.5
        h = self.btn_pcb_back.sizeHint().height() * 1.05
        self.btn_pcb_back.setFixedSize(w, h)
        self.btn_pcb_back.clicked.connect(self.back_pcb)
        btn_pcb_layout.addStretch(0)
        btn_pcb_layout.addWidget(self.btn_pcb_back, alignment = Qt.AlignCenter)
        btn_pcb_layout.addStretch(0)
        
        # Button 02: Continuar programa
        self.btn_pcb_cont = QPushButton("Continuar")
        self.btn_pcb_cont.setStyleSheet(style)
        self.btn_pcb_cont.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_pcb_cont.sizeHint().width() * 1.5
        h = self.btn_pcb_cont.sizeHint().height() * 1.05
        self.btn_pcb_cont.setFixedSize(w, h)
        self.btn_pcb_cont.clicked.connect(self.cont_pcb)
        btn_pcb_layout.addWidget(self.btn_pcb_cont, alignment = Qt.AlignCenter)
        btn_pcb_layout.addStretch(0)
        
        btn_pcb_widget.setLayout(btn_pcb_layout)
        btn_pcb_widget.setFixedWidth(self.w)
        
        pcb_layout.addWidget(btn_pcb_widget, alignment = Qt.AlignCenter)
        
        
    # ----- PROCESS LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_final = QLabel("EJECUCIÓN")
        lbl_final.setAlignment(Qt.AlignCenter)
        lbl_final.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_final.sizeHint().width() * 1.1
        h = lbl_final.sizeHint().height()
        lbl_final.setFixedSize(w, h)
        final_layout.addWidget(lbl_final, alignment = Qt.AlignCenter)
        
        # Button 01: Inicio de programa
        self.btn_final_back = QPushButton("Atrás")

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
        
        self.btn_final_back.setStyleSheet(style)
        self.btn_final_back.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_final_back.sizeHint().width() * 1.5
        h = self.btn_final_back.sizeHint().height() * 1.05
        self.btn_final_back.setFixedSize(w, h)
        self.btn_final_back.clicked.connect(self.back_final)
        final_layout.addWidget(self.btn_final_back, alignment = Qt.AlignCenter)

        
    # ----- CONFIGURACION -----------------------------------------------------
        main_widget = QWidget()
        table_widget = QWidget()
        pcb_widget = QWidget()
        final_widget = QWidget()
        
        main_widget.setLayout(main_layout)
        table_widget.setLayout(table_layout)
        pcb_widget.setLayout(pcb_layout)
        final_widget.setLayout(final_layout)
        self.stacked_layout.addWidget(main_widget)
        self.stacked_layout.addWidget(table_widget)
        self.stacked_layout.addWidget(pcb_widget)
        self.stacked_layout.addWidget(final_widget)
        
        self.setLayout(self.stacked_layout)
        
        
    def open_file(self):
        # self.file_name = QFileDialog.getOpenFileName(None, "Open", "", "CSV Files (*.csv)")
        self.file_name = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.lineEdit.setText(self.file_name)
        self.btn_act.setDisabled(False)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setDisabled(True)
        self.btn_bottom.setDisabled(True)
        # print(self.file_name)
        contenido = os.listdir(self.file_name)
        # print(contenido)
        # y = []
        # for x in contenido:
            # y += [os.path.splitext(x)]
        # print(y)
        ext = [".GBL", ".GTL", ".DRL", "back.csv", "front.csv", ".GKO", ".GBO", ".GTO", ".GBS", ".GTS", ".GBP", ".GTP"]
        count = []
        # y = [x for x in contenido if x.endswith(tuple(ext))]
        for x in contenido:
            y = list(filter(x.endswith, ext))
            # print(str(y) + "; " + str(len(y)))
            if len(y) > 0:
                count += y
        # print(count)
        miss = [x for x in ext if x not in count]
        a = len(miss)
        message = "Missing: " + str(a) + " files"
        detail =  "Requiere archivos " + str(miss)
        # print(message)
        if a != 0:
            self.btn_act.setDisabled(True)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(message)
            msg.setInformativeText(detail)
            msg.setWindowTitle("Carpeta No Válida")
            msg.setWindowIcon(qta.icon("ei.eye-open"))
            
            # print(msg.objectName())
            # child = msg.findChildren(QWidget)
            # print(child)
            # for x in child:
            #     print(x.objectName())
            
            # style = "#qt_msgbox_label{width: " + str(self.w) + "; border: 2px solid blue;}"
            style = "#qt_msgbox_informativelabel{min-width: 300px;}"
            # style += "#qt_msgboxex_icon_label{width: " + str(self.w) + "; border: 2px solid blue;}"
            msg.setStyleSheet(style)
            
            msg.exec()
        
    def actualizar(self):
                    
        self.btn_top.setDisabled(False)
        self.btn_bottom.setDisabled(False)
        self.btn_continuar.setDisabled(True)
        self.btn_top.setChecked(False)
        self.btn_bottom.setChecked(False)
        
        
        gbr.genImage(self.file_name, True)
        size = (self.w / 2) * 0.9

        top_im = QPixmap('board-top.png')
        #top_im = top_im.scaled(600, 600, Qt.KeepAspectRatio)
        top_im = top_im.scaled(size, size, Qt.KeepAspectRatio)
        bottom_im = QPixmap('board-bottom.png')
        #bottom_im = bottom_im.scaled(600, 600, Qt.KeepAspectRatio)
        bottom_im = bottom_im.scaled(size, size, Qt.KeepAspectRatio)
        
        top_lbl = QLabel()
        bot_lbl = QLabel()
        
        top_lbl.setPixmap(top_im)
        bot_lbl.setPixmap(bottom_im)
        
        top_ly = QVBoxLayout()
        bot_ly = QVBoxLayout()
        
        lbl1 = QLabel("Top")
        style = "QLabel { "
        style += "font-weight: bold; "
        style += "font-family: Georgia; "
        style += "font-size: 30pt; "
        style += "padding: 3px }"
        lbl1.setStyleSheet(style)
        lbl2 = QLabel("Bottom")
        lbl2.setStyleSheet(style)
        
        top_ly.addWidget(top_lbl, alignment = Qt.AlignCenter)
        top_ly.addWidget(lbl1, alignment = Qt.AlignCenter)
        bot_ly.addWidget(bot_lbl, alignment = Qt.AlignCenter)
        bot_ly.addWidget(lbl2, alignment = Qt.AlignCenter)
        
        self.btn_top.setLayout(top_ly)
        self.btn_bottom.setLayout(bot_ly)
        
        w = top_lbl.sizeHint().width() * 1.1
        h = top_lbl.sizeHint().height() + lbl1.sizeHint().height() * 1.2
    
        self.btn_top.setFixedSize(w, h)
        self.btn_bottom.setFixedSize(w, h)
    
        
    def sel_top(self):
        if self.btn_top.isChecked():
            self.btn_bottom.setDisabled(True)
            self.btn_continuar.setDisabled(False)
            self.top = True
        else:
            self.btn_bottom.setDisabled(False)
            self.btn_continuar.setDisabled(True)
            self.top = False
        
    def sel_bottom(self):
        if self.btn_bottom.isChecked():
            self.btn_top.setDisabled(True)
            self.btn_continuar.setDisabled(False)
            self.top = False
        else:
            self.btn_top.setDisabled(False)
            self.btn_continuar.setDisabled(True)
            self.top = True
            
    def continuar(self):
        self.stacked_layout.setCurrentIndex(1)
        self.lista = gbr.obtener_pnp(self.file_name, self.top)
        # table = gbr.genImageList(self.file_name, self.top)
        # print(self.lista)
        # print(type(self.lista))
        
        table = []
        for componente in self.lista:
            # print(type(componente))
            # print(vars(componente))
            table.append(vars(componente))
        
        # print(table)
        # print(type(table))
        
        self.comps_table.setColumnCount(len(table[0]))
        self.keys = list(table[0].keys())
        self.comps_table.setHorizontalHeaderLabels(self.keys)
        self.comps_table.setRowCount(len(table))
        
        self.comps_table.setDragEnabled(True)
        self.comps_table.setAcceptDrops(True)
        self.comps_table.viewport().setAcceptDrops(True)
        self.comps_table.setDropIndicatorShown(True)
        self.comps_table.setDefaultDropAction(Qt.MoveAction)
        self.comps_table.setSelectionMode(QTableWidget.SingleSelection)
        self.comps_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.comps_table.setDragDropMode(QTableWidget.InternalMove)
        self.comps_table.setDragDropOverwriteMode(False)
        
        # print(keys)
        # print(len(keys))
        
        row = 0
        for e in table:
            for i in range(0,len(self.keys)):
                x = str(e[self.keys[i]])
                self.comps_table.setItem(row, i, QTableWidgetItem(x))
                # print(i)
                # print(keys[i])
                # print(e[keys[i]])
            row += 1

        
    def back(self):
        self.stacked_layout.setCurrentIndex(0)
        
    def back_pcb(self):
        self.stacked_layout.setCurrentIndex(1)
        
    def back_final(self):
        self.stacked_layout.setCurrentIndex(2)
        
    def cont(self):
        rows = self.comps_table.rowCount()
        # print(rows)
        # print(self.keys)
        columns = len(self.keys)
        # print(columns)  
        # print(self.comps_table.item(0, 0).text())
        # print(self.comps_table.item(rows - 1, columns - 1).text())
        
        self.new_list = []
        for i in range(0, rows):
            x = {}
            for j in range(0, columns):
                
                if j < columns - 1:    
                    text = self.comps_table.item(i, j).text()
                else:
                    text = str(i + 1)
                x[self.keys[j]] = text
            self.new_list.append(x)
            # print(type(x))
        
        # print(self.new_list)
        # print(type(self.new_list))
        
        self.stacked_layout.setCurrentIndex(2)    
        gbr.genImageList(self.file_name, self.top, self.new_list)
        im = QPixmap("board-list.png")
        im = im.scaled(self.w * 0.95, self.w * 0.95, Qt.KeepAspectRatio)
        self.lbl.setPixmap(im)
        self.lbl.adjustSize()
        
    def cont_pcb(self):
        self.stacked_layout.setCurrentIndex(3)    


        

