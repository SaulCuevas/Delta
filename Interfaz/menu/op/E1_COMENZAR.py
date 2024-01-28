# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

VENTANA COMENZAR OPERACIÓN DELTA
"""

import os
import sys

# Dirección de imagen
# path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    aux_path = os.path.join(path, 'Interfaz\code_aux')
    disk = os.path.join(path, 'imagenes\disco.png')
    plate_hex = os.path.join(path, 'imagenes\hex.png')
    plate_trian = os.path.join(path, 'imagenes\\trian.png')
else:
    aux_path = os.path.join(path, 'Interfaz/code_aux')
    disk = os.path.join(path, 'imagenes/disco.png')
    plate_hex = os.path.join(path, 'imagenes/hex.png')
    plate_trian = os.path.join(path, 'imagenes/trian.png')
    
sys.path.insert(0, aux_path)

if os.name != 'nt':
    from picamera2 import Picamera2
    from picamera2.previews.qt import QGlPicamera2

import interprete_gerber as gbr
import special_table as tbl
import ESP32_serial as esp
import DeltaEcuaciones as eq
import SVA_PCB
import SVA_SMD
import Trayectorias
import chess
from time import sleep
import numpy as np

from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal, QPoint
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

import TEXT_OVERLAY as txt
import BUTTON_OVERLAY as btn
import ScrollableLabel as scroll_lbl

      

class ARCHIVOS(QWidget):
    # Constructor
    def __init__(self, ser):
        # Configuración pantalla GUI
        super().__init__()
        
        # self.thread = ProgressThread()
        self.ser = ser
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        
        self.top = True
        self.x = 1
        self.num = 1
        self.fotos = []
        self.contador = -1
        self.puntos = []

        self.stacked_layout = QStackedLayout()
        self.control_layout = QHBoxLayout()
        
        main_layout = QVBoxLayout()
        table_layout = QVBoxLayout()
        pcb_layout = QVBoxLayout()
        disk_layout = QVBoxLayout()
        plate_layout = QVBoxLayout()
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
        main_layout.addStretch(0)


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
        self.btn_continuar.clicked.connect(self.pcb_ready)
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
            self.btn_top.setFixedSize(w1 * 1.5, h1 * 1.2)
            self.btn_bottom.setFixedSize(w1 * 1.5, h1 * 1.2)
        else:
            self.btn_top.setFixedSize(w2 * 1.5, h2 * 1.2)
            self.btn_bottom.setFixedSize(w2 * 1.5, h2 * 1.2)
        self.btn_bottom.setCheckable(True)
        self.btn_bottom.clicked.connect(self.sel_bottom)
        layers_layout.addStretch(0)
        layers_layout.addWidget(self.btn_bottom, alignment = Qt.AlignCenter)
        layers_layout.addStretch(0)
        # btns_layout.setContentsMargins(0, 0, 0, 0)
        layers_widget.setFixedWidth(self.w)
        
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
        
        w = self.w * 0.9
        h = self.h * 0.6
        self.comps_table.setFixedSize(w, h)
        
        table_layout.addWidget(self.comps_table, alignment = Qt.AlignCenter)
        
        btn_table_layout = QHBoxLayout()
        btn_table_widget = QWidget()
        btn_table_widget.setLayout(btn_table_layout)
        btn_table_widget.setFixedWidth(self.w)
        
        table_layout.addWidget(btn_table_widget, alignment = Qt.AlignCenter)
        table_layout.addStretch()

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
        
        btn_pcb_widget.setLayout(btn_pcb_layout)
        btn_pcb_widget.setFixedWidth(self.w)
        
        pcb_layout.addWidget(btn_pcb_widget, alignment = Qt.AlignCenter)
        pcb_layout.addStretch()
        
        
    # ----- DISK LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_disk = QLabel("DISCO")
        lbl_disk.setAlignment(Qt.AlignCenter)
        lbl_disk.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_disk.sizeHint().width() * 1.1
        h = lbl_disk.sizeHint().height()
        lbl_disk.setFixedSize(w, h)
        disk_layout.addWidget(lbl_disk, alignment = Qt.AlignCenter)
        

        im = txt.DISK_IMG()
        im.setStyleSheet("border: 1px solid")
        disk_layout.addWidget(im, alignment = Qt.AlignCenter)

        # Label 01: Etiqueta para Nombre Ventana
        lbl_ready_disk = QLabel("Preparando para colocación de componentes...")
        lbl_ready_disk.setAlignment(Qt.AlignCenter)
        lbl_ready_disk.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_ready_disk.sizeHint().width() * 1.1
        h = lbl_ready_disk.sizeHint().height()
        lbl_ready_disk.setFixedSize(w, h)
        disk_layout.addWidget(lbl_ready_disk, alignment = Qt.AlignCenter)

    # ----- PLATE LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_plate = QLabel("PLATOS")
        lbl_plate.setAlignment(Qt.AlignCenter)
        lbl_plate.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_plate.sizeHint().width() * 1.1
        h = lbl_plate.sizeHint().height()
        lbl_plate.setFixedSize(w, h)
        plate_layout.addWidget(lbl_plate, alignment = Qt.AlignCenter)
        

        im_plate = btn.PLATE_IMG()
        im_plate.setStyleSheet("border: 1px solid")
        plate_layout.addWidget(im_plate, alignment = Qt.AlignCenter)

        # Label 01: Etiqueta para Nombre Ventana
        lbl_ready_plate = QLabel("Componentes a colocar en Platos")
        lbl_ready_plate.setAlignment(Qt.AlignCenter)
        lbl_ready_plate.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_ready_plate.sizeHint().width() * 1.1
        h = lbl_ready_plate.sizeHint().height()
        lbl_ready_plate.setFixedSize(w, h)
        plate_layout.addWidget(lbl_ready_plate, alignment = Qt.AlignCenter)
    
    # ----- PROCESS LAYOUT ------------------------------------------------------
        
        # Label 01: Etiqueta para Nombre Ventana
        lbl_final = QLabel("EJECUCIÓN")
        lbl_final.setAlignment(Qt.AlignCenter)
        lbl_final.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        w = lbl_final.sizeHint().width() * 1.1
        h = lbl_final.sizeHint().height()
        lbl_final.setFixedSize(w, h)
        final_layout.addWidget(lbl_final, alignment = Qt.AlignCenter)

        # Scrollabel Label
        self.sc_lbl = scroll_lbl.ScrollLabel(self)
        self.text = "INICIANDO ...\n"
        self.sc_lbl.setFixedSize(self.w * 0.9, self.h * 0.6)
        final_layout.addWidget(self.sc_lbl, alignment = Qt.AlignCenter)
        

    # ---- CONTROL LAYOUT -----------------------------------------------------

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
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.btn_back, alignment = Qt.AlignCenter)
        self.control_layout.addStretch()

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
        self.control_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)
        self.control_layout.addStretch()
        
        # Button 02: Continuar programa
        self.btn_cont = QPushButton("Continuar")
        self.btn_cont.setStyleSheet(style)
        self.btn_cont.setFont(QFont("Georgia", 10, QFont.Bold))
        w = self.btn_cont.sizeHint().width() * 1.5
        h = self.btn_cont.sizeHint().height() * 1.05
        self.btn_cont.setFixedSize(w, h)
        self.btn_cont.clicked.connect(self.continuar)
        self.control_layout.addWidget(self.btn_cont, alignment = Qt.AlignCenter)
        self.control_layout.addStretch()

        

    # ----- CONFIGURACION -----------------------------------------------------
        main_widget = QWidget()
        table_widget = QWidget()
        pcb_widget = QWidget()
        disk_widget = QWidget()
        plate_widget = QWidget()
        final_widget = QWidget()
        
        main_widget.setLayout(main_layout)
        table_widget.setLayout(table_layout)
        pcb_widget.setLayout(pcb_layout)
        disk_widget.setLayout(disk_layout)
        plate_widget.setLayout(plate_layout)
        final_widget.setLayout(final_layout)
        self.stacked_layout.addWidget(main_widget)
        self.stacked_layout.addWidget(table_widget)
        self.stacked_layout.addWidget(pcb_widget)
        self.stacked_layout.addWidget(disk_widget)
        self.stacked_layout.addWidget(plate_widget)
        self.stacked_layout.addWidget(final_widget)

        stacked_widget = QWidget()
        stacked_widget.setMaximumHeight(self.h * 0.8)
        self.control_widget = QWidget()
        stacked_widget.setLayout(self.stacked_layout)
        self.control_widget.setLayout(self.control_layout)
        comenzar_layout = QVBoxLayout()
        comenzar_layout.addWidget(stacked_widget, alignment = Qt.AlignCenter)
        comenzar_layout.addWidget(self.control_widget, alignment = Qt.AlignCenter)

        self.control_widget.hide()
        self.setLayout(comenzar_layout)
        
        
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
        top_im = top_im.scaled(self.h * 0.5, self.h * 0.5, Qt.KeepAspectRatio)
        #top_im = top_im.scaled(size, size, Qt.KeepAspectRatio)
        bottom_im = QPixmap('board-bottom.png')
        bottom_im = bottom_im.scaled(self.h * 0.5, self.h * 0.5, Qt.KeepAspectRatio)
        #bottom_im = bottom_im.scaled(size, size, Qt.KeepAspectRatio)
        
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
            
    def pcb_ready(self):
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

        self.control_widget.show()
        self.btn_start.hide()

        
    def back(self):
        if self.stacked_layout.currentIndex() == 1:
            self.stacked_layout.setCurrentIndex(0)
        elif self.stacked_layout.currentIndex() == 2:
            self.stacked_layout.setCurrentIndex(1)
        elif self.stacked_layout.currentIndex() == 3:
            self.stacked_layout.setCurrentIndex(2)
        
    def continuar(self):
        if self.stacked_layout.currentIndex() == 1:
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
            im = im.scaled(self.h * 0.5, self.h * 0.5, Qt.KeepAspectRatio)
            self.lbl.setPixmap(im)
            self.lbl.adjustSize()
        elif self.stacked_layout.currentIndex() == 2:
            self.stacked_layout.setCurrentIndex(3)
        elif self.stacked_layout.currentIndex() == 3:
            self.stacked_layout.setCurrentIndex(4)
        elif self.stacked_layout.currentIndex() == 4:
            self.stacked_layout.setCurrentIndex(5)
        elif self.stacked_layout.currentIndex() == 5:
            self.contador += 1
            if self.contador == 0:
                self.sc_lbl.setText(self.text)
            else:
                self.execute(self.contador)

    def execute(self, x):
        if (x == 1):
            # 1. Conexión con cámara
            text1 = "\n1. Iniciando conexión con cámara ... \n"
            self.text += text1
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            try:
                # Set up camera and application
                self.picam2 = Picamera2()
                # preview_config = self.picam2.create_preview_configuration(main={"size": (800, 600)})
                preview_config = self.picam2.create_preview_configuration(main={"size": (2592, 1944)})
                self.picam2.configure(preview_config)
                self.qpicamera2 = QGlPicamera2(self.picam2, width = 200, height = 150, keep_ar = True)
                h = self.h * 0.9
                w = (2592/1944) * h
                self.qpicamera2.setFixedSize(w, h)
                self.qpicamera2.done_signal.connect(self.capture_done)
                self.cam_layout.addWidget(self.qpicamera2)
                text1 = "Conexión completa :))\n"
            except:
                dlg_port = QMessageBox()
                dlg_port.setWindowTitle("CAM Error!")
                dlg_port.setText("Fallo al establecer conexión")
                dlg_port.exec()
                text1 = "CAM ERROR -> Fallo en conexión"
            self.text += text1
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 2):
            # 2. Enviar Herramienta e Inventario a HOME 
            text2 = "2. Enviando Herramienta e Inventario a HOME ...\n"
            self.text += text2
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.tool_HOME()
            text2 = "HERRAMIENTA COMPLETADO RUTINA HOME\n"
            self.text += text2
            sleep(0.5)
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.move_inventory(0)
            text2 = "INVENTARIO COMPLETADO RUTINA HOME\n"
            self.text += text2
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 3):
            # 3. Enviar posición HOME ROBOT (x = 0, y = 0, z = 180)
            text3 = "\n3. Enviando robot a HOME ...\n"
            self.text += text3
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.pos_robot(0, 0, 190)
            text3 = "ROBOT COMPLETADO RUTINA HOME\n"
            self.text += text3
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 4):
            # 4. Captura de imagen
            text4 = "\n 4. Capturando imagen PCB ...\n"
            self.text += text4
            sleep(0.5)
            self.sc_lbl.setText(self.text)
            self.capture_image()
            text4 = "IMAGEN PCB CAPTURADA EXITOSAMENTE\n"
            self.text += text4
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 5):
            # 5. Enviar a posición CAPTURA INVENTARIO
            text5 = "\n5. Enviando robot a CAPTURA INVENTARIO ...\n"
            self.text += text5
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.pos_robot(45, -65, 187)
            text5 = "ROBOT POSICIONADO SOBRE INVENTARIO\n"
            self.text += text5
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 6):
            # 6. Tomar foto INVENTARIO Cuadrante 1
            text6 = "\n 6. Tomando foto INVENTARIO Cuadrante 1 ...\n"
            self.text += text6
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.capture_image()
            text6 = "CAPTURA COMPLETADA\n"
            self.text += text6
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 7):
            # 7. Girar inventario a 90°
            text7 = "\n 7. Girando INVENTARIO a 90° ...\n"
            self.text += text7
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.move_inventory(90)
            text6 = "POSICIONAMIENTO DE INVENTARIO COMPLETADO\n"
            self.text += text6
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 8):
            # 8. Tomar foto INVENTARIO Cuadrante 2
            text8 = "\n 8. Tomando foto INVENTARIO Cuadrante 2 ...\n"
            self.text += text8
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.capture_image()
            text8 = "CAPTURA COMPLETADA\n"
            self.text += text8
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 9):
            # 9. Girar inventario a 180°
            text9 = "\n 9. Girando INVENTARIO a 180° ...\n"
            self.text += text9
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.move_inventory(180)
            text8 = "POSICIONAMIENTO DE INVENTARIO COMPLETADO\n"
            self.text += text8
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 10):
            # 10. Tomar foto INVENTARIO Cuadrante 3
            text10 = "\n 10. Tomando foto INVENTARIO Cuadrante 3 ...\n"
            self.text += text10
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.capture_image()
            text10 = "CAPTURA COMPLETADA\n"
            self.text += text10
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 11):
            # 11. Girar inventario a 270°
            text11 = "\n 11. Girando INVENTARIO a 270° ...\n"
            self.text += text11
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.move_inventory(270)
            text11 = "POSICIONAMIENTO DE INVENTARIO COMPLETADO\n"
            self.text += text11
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 12):
            # 12. Tomar foto INVENTARIO Cuadrante 4
            text12 = "\n 12. Tomando foto INVENTARIO Cuadrante 4 ...\n"
            self.text += text12
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.capture_image()
            text12 = "CAPTURA COMPLETADA\n"
            self.text += text12
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 13):
            # 13. Regresar Inventario a HOME (0°)
            text13 = "\n 13. Girando INVENTARIO a HOME ...\n"
            self.text += text13
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.move_inventory(0)
            text13 = "POSICIONAMIENTO HOME (0°) DE INVENTARIO COMPLETADO\n"
            self.text += text13
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 14):
            # 14. Regresar robot a HOME (x = 0, y = 0, z = 190)
            text14 = "\n 14. Posicionando robot en HOME ...\n"
            self.text += text14
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            self.pos_robot(0, 0, 190)
            text14 = "ROBOT POSICIONADO EN HOME EXITOSAMENTE\n"
            self.text += text14
            sleep(0.5)
            self.sc_lbl.setText(self.text)
        elif (x == 15):
            # 15. RUTAS: CARPETA CAM, FOTO PCB, BOOLEANO TOP/BOTTOM, LISTA COMPONENTES, FOTO CUADRANTES (4)
            text15 = "\n 15. Comenzando análisis de SVA ...\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            # Llamar SVA_PCB.inicioSVA
            text15 = f"DATO 01: {self.file_name}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 02: {self.fotos[0]}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 03: {self.top}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 04: {self.new_list}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 05: {self.fotos[1]}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 06: {self.fotos[2]}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 07: {self.fotos[3]}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            text15 = f"DATO 08: {self.fotos[4]}\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            # Calcular 
            self.puntos = SVA_PCB.inicioSVA(self.file_name, self.fotos[0], self.top, self.new_list, self.fotos[1], self.fotos[2], self.fotos[3], self.fotos[4])
            text15 = "PUNTOS CALCULADOS CORRECTAMENTE\n"
            self.text += text15
            self.sc_lbl.setText(self.text)
        elif (x == 16):
            # 16. Calcular Trayectorias
            text16 = "\n 16. Calculando Trayectorias ...\n"
            self.text += text16
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            Trayectorias.calc_trayectorias_ps_no_t(func = Trayectorias.bezier_no_t, operaciones = self.puntos[:,0], Ps = self.puntos[:,1:4], vel_deseada = self.puntos[:,4])
            text16 = "CALCULO COMPLETADO EXITOSAMENTE\n"
            self.text += text16
            self.sc_lbl.setText(self.text)
        elif (x == 17):
            # 17. Enviar Trayectorias
            text17 = "\n 17. Enviando Trayectorias ...\n"
            self.text += text17
            self.sc_lbl.setText(self.text)
            sleep(0.5)
            esp.enviar_trayectoria(self.ser)
            text17 = "PROCESO COMPLETADO\n"
            self.text += text17
            self.sc_lbl.setText(self.text)
        else:
            print(f"Paso {x} NO existe !!!")


    def clean_buffer(self):
        temp = esp.read_ESP32(self.ser)
            #print(temp[0:4])
        while(temp != "ready"):
            if temp != "":
                print(f"R{self.x}-> {temp}")
            temp = esp.read_ESP32(self.ser)
        print(f"R{self.x}-> {temp}")
        self.x += 1

    def tool_HOME(self):
        esp.HOME_herramienta(self.ser)
        sleep(0.01)
        self.clean_buffer()
        esp.cambio_herramienta(self.ser, 0)
        sleep(0.01)
        self.clean_buffer()

    def move_inventory(self, x):
        angle = np.deg2rad(x)
        esp.mover_motor(self.ser, 6, angle)
        sleep(0.01)
        self.clean_buffer()

    def pos_robot(self, x, y ,z):
        q1, q2, q3, err = eq.DeltaIK(px = x, py = y, pz = z)
        print(f"ERROR POS: {err}")
        esp.mover_brazos(self.ser, q1, q2, q3)
        sleep(0.01)
        self.clean_buffer()

    def capture_image(self):
        print("FOTO")
        self.picam2.capture_request(signal_function = self.qpicamera2.signal_done)

    def capture_done(self, job):
        request = self.picam2.wait(job)
        text = "FOTO_" + self.num + ".png"
        request.save("main", text)
        request.release()
        # print(os.getcwd())
        # img_foto = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FOTO.png")
        img_foto = os.path.join(os.getcwd(), text)
        new = chess.generate_undistort(img_foto, 1)
        self.fotos.append(new)
        self.num += 1
