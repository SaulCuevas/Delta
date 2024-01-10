# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

MENU
- Ventana que muestra botones de operación para manipulación
  de robot. Despliegue de opciones para interactuar con el ususario.
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
    QStackedLayout,
    QMessageBox,
    QPushButton)
import serial
import sys
import os
import glob
import qtawesome as qta

# Dirección de imagen
# path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    aux_path = os.path.join(path, 'Interfaz\code_aux')
else:
    aux_path = os.path.join(path, 'Interfaz/code_aux')
sys.path.insert(0, aux_path)
import ESP32_serial as esp




# CLASE MENU - WIDGET
class MENU(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()  # Dimension general width pantalla
        self.h = QDesktopWidget().screenGeometry().height() # Dimension general height pantalla
        self.font_size1 = int(self.h/20) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/30) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/50) # Valor de fuente 3 ajustado a tamaño pantalla
        self.font_size4 = int(self.h/40) # Valor de fuente 4 ajustado a tamaño pantalla
        self.border_width = int(self.h/100) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/60) # Valor de radius width (button) ajustado a tamaño pantalla
        # Inicialización de Variables
        self.ser = ""
        self.com_port = ""
        # Generación layouts generales
        self.main_layout = QStackedLayout() # LAYOUT general
        special_layout = QVBoxLayout()  # LAYOUT 1 -> selección puerto
        menu_layout = QVBoxLayout() # LAYOUT 2 -> menu general de interfaz
        regreso_layout= QHBoxLayout()   # LAYOUT 2.1 -> buttons para regreso a INICIO y cambiar puerto
        # Generación widgets para layouts
        special_widget = QWidget()  # Widget para LAYOUT 1
        menu_widget = QWidget() # Widget  para LAYOUT 2
        regreso_widget= QWidget()   # Widget para LAYOUT 2.1
        special_widget.setLayout(special_layout) # Fijar LAYOUT 1 a Widget
        menu_widget.setLayout(menu_layout)  # Fijar LAYOUT 2 a Widget
        regreso_widget.setLayout(regreso_layout)  # Fijar LAYOUT 2.1 a Widget

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Etiqueta para Selección de Puerto COM
        # 02. ComboBox 01: Selección de Puerto COM
        # 03. Button 01: Elegir Puerto
        # 04. Button 02: Inicio de TUTORIAL
        # 05. Button 03: Inicio de CONTROL MANUAL
        # 06. Button 04: Inicio de INVENTARIO SMD
        # 07. Button 05: Inicio de ESTADISTICAS
        # 08. Button 06: Inicio de COMENZAR OPERACION ENSAMBLE PCBs
        # 09. Button 07: Volver pantalla principal INICIO
        # 10. Button 08: Volver SELECCION PUERTO

    # ----- STYLE WIDGET -----------------------------------------------------
        cyan = "rgb(0, 224, 224)"
        azul = "rgb(0, 0, 224)"
        plata = "rgb(227, 228, 229)"
        
        icon = qta.icon("mdi.usb-port")

        # Style Label Widgets
        st_label = "QLabel { "
        st_label += "background-color: lightgreen; "
        st_label += "border-style: none; "
        st_label += "font-weight: bold; "
        st_label += "font-family: Georgia; "
        st_label += f"font-size: {self.font_size1}pt; "
        st_label += "padding: 3px }"

        # Style ComboBox Widgets
        st_cb = "QComboBox { "
        st_cb += "background-color: lightgreen; "
        st_cb += "border-style: none; "
        st_cb += "font-weight: normal; "
        st_cb += "font-family: Georgia; "
        st_cb += f"font-size: {self.font_size2}pt; "
        st_cb += "padding: 5px 5px 5px 20px; }"

        st_cb += "QComboBox::drop-down:button {"
        #st_cb += "background-color: red; "
        st_cb += "width: 60px; }"

        # Style Button Widgets
        st_btn = "QPushButton { "
        st_btn += "background-color: lightblue; "
        st_btn += "font-weight: bold; "
        st_btn += "font-family: Georgia; "
        st_btn += f"font-size: {self.font_size2}pt; "
        st_btn += "border-style: outset; "
        st_btn += f"border-width: {self.border_width}px; "
        st_btn += f"border-radius: {self.border_radius}px; "
        st_btn += "border-color: blue; "
        st_btn += "padding: 3px }"
        
        st_btn += "QPushButton:hover { "
        st_btn += f"background-color: {cyan}; "
        st_btn += "border-style: inset } "
        
        st_btn += "QPushButton:pressed { "
        st_btn += f"background-color: {azul}; "
        st_btn += "border-style: inset } "

        # Style Button Widgets (alt)
        st_alt = "QPushButton { "
        st_alt += f"background-color: {plata}; "
        st_alt += "font-weight: bold; "
        st_alt += "font-family: Georgia; "
        st_alt += f"font-size: {self.font_size4}pt; "
        st_alt += "padding: 10px }"
        
        st_alt += "QPushButton:hover { "
        st_alt += "background-color: rgb(0, 224, 224); "
        st_alt += "border-style: inset } "
        
        st_alt += "QPushButton:pressed { "
        st_alt += "background-color: rgb(0, 0, 224); "
        st_alt += "border-style: inset } "

    # ------ SPECIAL WIDGET ------------------------------------------------------

        # Label 01: Etiqueta para Selección de Puerto COM
        lbl_com_port = QLabel("COM port:")  # Generar Label PORT
        lbl_com_port.setAlignment(Qt.AlignCenter)   # Alinear texto al centro
        lbl_com_port.setStyleSheet(st_label)    # Fijar estilo de widget
        w = lbl_com_port.sizeHint().width() * 1.05    # Guardar valor de ancho para widget
        h = lbl_com_port.sizeHint().height()    # Guardar valor de alto para widget
        lbl_com_port.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        special_layout.addWidget(lbl_com_port, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT ESPECIAL-> seleccion puerto

        # ComboBox 01: Selección de Puerto COM
        self.cb_port = QComboBox()  # Generar ComboBox PORT
        self.items = ["SELECCIONAR"]    # Inicializacion de Lista de puertos
        self.cb_port.addItems(self.items)   # Anexar lista de puertos al ComboBox
        # self.cb_port.view().setRowHidden(0, True) # Ocultar primer elemento lista
        self.cb_port.addItems(self.serial_ports()) # Anexar valores de funcion para detectar puertos
        self.cb_port.activated.connect(self.add_port)   # Enlazar con funcion para anexar puerto
        self.cb_port.setStyleSheet(st_cb) # Fijar estilo de widget
        w = int(self.w * 0.3) # Guardar valor de ancho para widget
        h = self.cb_port.sizeHint().height() * 2    # Guardar valor de alto para widget
        self.cb_port.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        special_layout.addWidget(self.cb_port, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT ESPECIAL-> seleccion puerto
        
        # Button 01: Elegir Puerto
        self.btn_accept = QPushButton("Elegir") # Generar PushBUtton ELEGIR PORT
        self.btn_accept.clicked.connect(self.gotoMenu)  # Conectar a funcion para IR A MENU
        self.btn_accept.setStyleSheet(st_btn)   # Fijar estilo de widget
        w = self.btn_accept.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_accept.sizeHint().height() * 1.2 # Guardar valor de alto para widget
        self.btn_accept.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        special_layout.addWidget(self.btn_accept, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT ESPECIAL-> seleccion puerto

    # ------ MENU WIDGET ---------------------------------------------------------

        # Button 02: Inicio de TUTORIAL
        self.btn_1 = QPushButton("Tutorial")    # Generar PushBUtton TUTORIAL
        self.btn_1.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_1.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_1.sizeHint().height() * 1.3 # Guardar valor de alto para widget
        self.btn_1.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        menu_layout.addWidget(self.btn_1, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MENU
        
        # Button 03: Inicio de CONTROL MANUAL
        self.btn_2 = QPushButton("Control Manual")  # Generar PushBUtton CONTROL MANUAL
        self.btn_2.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_2.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_2.sizeHint().height() * 1.3 # Guardar valor de alto para widget
        self.btn_2.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        menu_layout.addWidget(self.btn_2, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MENU
        
        # Button 04: Inicio de INVENTARIO SMD
        self.btn_3 = QPushButton("SMD válidos") # Generar PushBUtton INVENTARIO SMD
        self.btn_3.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_3.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_3.sizeHint().height() * 1.3 # Guardar valor de alto para widget
        self.btn_3.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        menu_layout.addWidget(self.btn_3, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MENU
        
        # Button 05: Inicio de ESTADISTICAS
        self.btn_4 = QPushButton("Estadísticas")    # Generar PushBUtton ESTADÍSTICAS
        self.btn_4.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_4.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_4.sizeHint().height() * 1.3 # Guardar valor de alto para widget
        self.btn_4.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        menu_layout.addWidget(self.btn_4, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MENU
        
        # Button 06: Inicio de COMENZAR OPERACION ENSAMBLE PCBs
        self.btn_5 = QPushButton("Comenzar")    # Generar PushBUtton COMENZAR PROCESO ENSAMBLADO PCBs
        self.btn_5.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_5.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_5.sizeHint().height() * 1.3 # Guardar valor de alto para widget
        self.btn_5.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        menu_layout.addWidget(self.btn_5, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MENU
        
        # ------ REGRESO WIDGET ------------------------------------------------------

        # Button 07: Volver pantalla principal INICIO
        self.btn_inicio = QPushButton("INICIO") # Generar PushBUtton VOLVER A INICIO
        self.btn_inicio.setStyleSheet(st_alt)   # Fijar estilo de widget
        w = self.btn_inicio.sizeHint().width() * 1.3  # Guardar valor de ancho para widget
        h = self.btn_inicio.sizeHint().height() * 1.2 # Guardar valor de alto para widget
        self.btn_inicio.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        regreso_layout.addWidget(self.btn_inicio, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT REGRESO

        # Button 08: Volver SELECCION PUERTO
        self.btn_puerto = QPushButton(icon, "") # Generar PushButton VOLVER A SELECCION PUERTO
        self.btn_puerto.setIconSize(QSize(self.font_size1 * 1.5, self.font_size1 * 1.5))
        self.btn_puerto.clicked.connect(self.select_port)
        self.btn_puerto.setStyleSheet(st_alt)   # Fijar estilo de widget
        w = self.btn_puerto.sizeHint().width() * 1.05  # Guardar valor de ancho para widget
        self.btn_puerto.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        regreso_layout.addWidget(self.btn_puerto, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT REGRESO
        
        menu_layout.addWidget(regreso_widget, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT MENU
        
        # Configuración de LAYOUT PRINCIPAL
        self.main_layout.addWidget(special_widget)  # Index(0) -> LAYOUT SPECIAL: seleccion de puerto
        self.main_layout.addWidget(menu_widget) # Index(1) -> LAYOUT MENU: opciones de operacion para robot
        self.setLayout(self.main_layout)    # Fijar LAYOUT PRINCIPAL a widget

# ---- FUNCIONES DE CONTROL ---------------------------------------------------------------------

    # Función para determinar los puertos disponibles
    def serial_ports(self) -> list:
        if (sys.platform.startswith('win')):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif (sys.platform.startswith('linux') or sys.platform.startswith('cygwin')):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif (sys.platform.startswith('darwin')):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        # print(result)
        return result
    
    # Función para añadir puerto
    def add_port(self):
        self.com_port = self.cb_port.currentText()
        print(self.com_port)

    # Función para continuar a menú
    def gotoMenu(self):
        try:
            self.ser = esp.start_serial(self.com_port)
            # print(self.ser)
            self.main_layout.setCurrentIndex(1)
            esp.stop_serial(self.ser)
        except:
            dlg_port = QMessageBox(self)
            dlg_port.setWindowTitle("COM Port Error!")
            dlg_port.setText("Fallo al establecer conexión")
            dlg_port.exec()

    # Función para obtener valor de puerto conectado
    def get_port(self):
        return self.com_port
    
    # Función para volver a SELECCION DE PUERTO
    def select_port(self):
        self.main_layout.setCurrentIndex(0)

