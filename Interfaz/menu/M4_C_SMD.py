# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

INVENTARIO SMD
- Ventana muestra tabla con componentes SMD permitidos/válidos
  para ser usados en el ensamble de PCBs con el robot.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QDesktopWidget,
    QHeaderView)

# CLASE SMD - WIDGET
class SMD(QWidget):
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
        # Generación layouts generales
        main_layout = QVBoxLayout()

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Etiqueta para titulo de ventana INVENTARIO SMD
        # 02. Tab Widget 01: Pestaña para cambio de listados SMD
        # 03. Table Widget 01: Tabla para listado de componentes SMD - GENERAL
        # 04. Table Widget 02: Tabla para listado de componentes SMD - RESISTENCIAS
        # 05. Table Widget 03: Tabla para listado de componentes SMD - CAPACITORES
        # 06. Table Widget 04: Tabla para listado de componentes SMD - LEDs
        # 07. Table Widget 05: Tabla para listado de componentes SMD - TRANSISTORES
        # 08. Table Widget 06: Tabla para listado de componentes SMD - CIRCUITOS INTEGRADOS
        # 09. Button 01: Volver a MENU

    # ----- STYLE VARIABLES -----------------------------------------------------
        verde_oscuro = "rgb(35, 155, 86)"
        azul_claro = "rgb(84, 153, 199)"
        azul_oscuro = "rgb(21, 67, 96)"
        plata = "rgb(227, 228, 229)"
        gris = "rgb(207, 208, 209)"

        # Style Label Widgets
        st_label = "QLabel { "
        st_label += "background-color: lightgreen; "
        st_label += "border-style: none; "
        st_label += "font-weight: bold; "
        st_label += "font-family: Georgia; "
        st_label += f"font-size: {self.font_size2}pt; "
        st_label += "padding: 3px }"

        # Style Tab Widget
        st_tab = "QTabWidget::pane {"
        st_tab += "border-style: solid; "
        st_tab += "border-width: 0px; "
        st_tab += "border-color: black; "
        st_tab += "top: -1px; "
        st_tab += "}"

        st_tab += "QTabBar {"
        st_tab += "font-style: italic; "
        st_tab += "font-family: Georgia; "
        st_tab += f"font-size: {self.font_size4}pt; "
        st_tab += "spacing: 100; "
        st_tab += "}"

        st_tab += "QTabBar::tab {"
        st_tab += f"background: {gris}; "
        st_tab += "border-style: inset; "
        st_tab += "border-width: 1px; "
        st_tab += f"border-color: {gris}; "
        st_tab += "padding: 5px; "
        st_tab += "}"

        st_tab += "QTabBar::tab:selected { "
        st_tab += f"background: {plata}; "
        st_tab += "font-weight: bold; "
        st_tab += "font-style: normal; "
        st_tab += "border-style: outset; "
        st_tab += f"font-size: {self.font_size3}pt; "
        st_tab += "border-top-left-radius: 10px; "
        st_tab += "border-top-right-radius: 10px; "
        st_tab += "border-width: 5px; "
        st_tab += f"border-color: {gris}; "
        st_tab += "padding: 5px 0px; "
        st_tab += "bottom: -1px; "
        st_tab += "}"

        st_tab += "QTabBar::tab:!selected { "
        st_tab += "margin-top: 10px; "
        st_tab += "}"

        # Style Table Widget
        st_table = "QHeaderView::section {"
        st_table += "font-weight: bold; "
        st_table += "font-family: Georgia; "
        st_table += f"font-size: {self.font_size3}pt; "
        st_table += "}"

        st_table += "QScrollBar:vertical {"
        st_table += "width: 50px; "
        st_table += "}"

        st_table += "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {"
        st_table += "width: 30px; "
        st_table += "height: 30px; "
        st_table += "}"

        st_table += "QTableView {"
        st_table += "font-family: Georgia; "
        st_table += f"font-size: {self.font_size4}pt; "
        st_table += "}"

        # Style Button Widgets
        st_btn = "QPushButton { "
        st_btn += "background-color: lightgreen; "
        st_btn += "border-style: outset; "
        st_btn += f"border-width: {self.border_width}px; "
        st_btn += f"border-radius: {self.border_radius}px; "
        st_btn += "border-color: green; "
        st_btn += "font-weight: bold; "
        st_btn += "font-family: Georgia; "
        st_btn += f"font-size: {self.font_size2}pt; "
        st_btn += "padding: 3px }"

        st_btn += "QPushButton:hover { "
        st_btn += f"background-color: {verde_oscuro}; "
        st_btn += "border-color: green; "
        st_btn += "border-style: inset } "

        st_btn += "QPushButton:pressed { "
        st_btn += f"background-color: {azul_claro}; "
        st_btn += f"border-color: {azul_oscuro}; "
        st_btn += "border-style: inset } "

    # ----- PRINCIPAL WIDGET -----------------------------------------------------

        # Label 01: Etiqueta para titulo de ventana INVENTARIO SMD
        lbl_smd = QLabel("SMD Válidos") # Generar Label Ventana INVENTARIO SMD
        lbl_smd.setAlignment(Qt.AlignCenter)    # Alinear texto en el centro
        lbl_smd.setStyleSheet(st_label) # Fijar estilo de widget
        w = lbl_smd.sizeHint().width() + 10 # Guardar valor de ancho para widget
        h = lbl_smd.sizeHint().height() # Guardar valor de alto para widget
        lbl_smd.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(lbl_smd, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT PRINCIPAL

        # Tab Widget 01: Tabla para listado de componentes SMD
        tab_widget = QTabWidget()   # Generar TabWidget para listado SMD
        
        # Tabla 01: Lista componentes SMD - GENERAL
        table1= [
            {'Empaquetado': '01005', 'Componente': 'Resistencias,\nCapacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox \n(g/1000 pzas.)': '0.04', 'Imagen': '-'},
            {'Empaquetado': '0201', 'Componente': 'Resistencias, \nCapacitores', 'mm': '0.6 x 0.3', 'in': '0.02 x 0.01', 'Peso aprox \n(g/1000 pzas.)': '0.15', 'Imagen': '-'},
            {'Empaquetado': '0402', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.0 x 0.5', 'in': '0.04 x 0.02', 'Peso aprox \n(g/1000 pzas.)': '0.8', 'Imagen': '-'},
            {'Empaquetado': '0603', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.5 x 0.8', 'in': '0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '2', 'Imagen': '-'},
            {'Empaquetado': '0805', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '2.0 x 1.3', 'in': '0.08 x 0.05', 'Peso aprox \n(g/1000 pzas.)': '4', 'Imagen': '-'},
            {'Empaquetado': '1206', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '3.0 x 1.5', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '10', 'Imagen': '-'},
            {'Empaquetado': '1210', 'Componente': 'Resistencias, \nCapacitores', 'mm': '3.2 x 2.5', 'in': '0.125 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '16', 'Imagen': '-'},
            {'Empaquetado': '1806', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.5 x 1.6', 'in': '0.18 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '1812', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 3.0', 'in': '0.18 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '1825', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 6.4', 'in': '0.18 x 0.25', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '2010', 'Componente': 'Resistencias, \nCapacitores', 'mm': '5.0 x 2.5', 'in': '0.20 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '2512', 'Componente': 'Resistencias, \nCapacitores', 'mm': '6.3 x 3.2', 'in': '0.25 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '45', 'Imagen': '-'},
            {'Empaquetado': '2920', 'Componente': 'Resistencias, \nCapacitores', 'mm': '7.4 x 5.1', 'in': '0.29 x 0.20', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '3014', 'Componente': 'LEDs', 'mm': '3.0 x 1.4', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '3020', 'Componente': 'LEDs', 'mm': '3.0 x 2.0', 'in': '0.12 x 0.08', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '3528', 'Componente': 'LEDs', 'mm': '3.5 x 2.8', 'in': '0.14 x 0.11', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '5050', 'Componente': 'LEDs', 'mm': '5.0 x 5.0', 'in': '0.20 x 0.20', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '5730', 'Componente': 'LEDs', 'mm': '5.7 x 3.0', 'in': '0.23 x 0.12', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 23', 'Componente': 'Transitores', 'mm': '2.9 x 2.4 x 1.1', 'in': '0.12 x 0.10 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 89', 'Componente': 'Transitores', 'mm': '4.5 x 4.0 x 1.5', 'in': '0.18 x 0.16 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 143', 'Componente': 'Transitores', 'mm': '2.9 x 2.8 x 1.1', 'in': '0.12 x 0.11 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 223', 'Componente': 'Transitores', 'mm': '6.5 x 7.0 x 1.8', 'in': '0.26 x 0.28 x 0.07', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 323', 'Componente': 'Transitores', 'mm': '2.0 x 2.1 x 0.9', 'in': '0.08 x 0.08 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 523', 'Componente': 'Transitores', 'mm': '1.6 x 1.6 x 0.7', 'in': '0.06 x 0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SO - 8', 'Componente': 'Circuito Integrado', 'mm': '3.8 x 4.8', 'in': '0.15 x 0.19', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'TSSOP - 8', 'Componente': 'Circuito Integrado', 'mm': '3.1 x 4.5', 'in': '0.12 x 0.18', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SSOP - 8', 'Componente': 'Circuito Integrado', 'mm': '2.9 x 3.15', 'in': '0.12 x 0.12', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOP - 8', 'Componente': 'Circuito Integrado', 'mm': '6.5 x 5.6', 'in': '0.26 x 0.22', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 01

        # Tabla 02: Lista componentes SMD - RESISTENCIAS
        table2= [
            {'Empaquetado': '01005', 'Componente': 'Resistencias,\nCapacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox \n(g/1000 pzas.)': '0.04', 'Imagen': '-'},
            {'Empaquetado': '0201', 'Componente': 'Resistencias, \nCapacitores', 'mm': '0.6 x 0.3', 'in': '0.02 x 0.01', 'Peso aprox \n(g/1000 pzas.)': '0.15', 'Imagen': '-'},
            {'Empaquetado': '0402', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.0 x 0.5', 'in': '0.04 x 0.02', 'Peso aprox \n(g/1000 pzas.)': '0.8', 'Imagen': '-'},
            {'Empaquetado': '0603', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.5 x 0.8', 'in': '0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '2', 'Imagen': '-'},
            {'Empaquetado': '0805', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '2.0 x 1.3', 'in': '0.08 x 0.05', 'Peso aprox \n(g/1000 pzas.)': '4', 'Imagen': '-'},
            {'Empaquetado': '1206', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '3.0 x 1.5', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '10', 'Imagen': '-'},
            {'Empaquetado': '1210', 'Componente': 'Resistencias, \nCapacitores', 'mm': '3.2 x 2.5', 'in': '0.125 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '16', 'Imagen': '-'},
            {'Empaquetado': '1806', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.5 x 1.6', 'in': '0.18 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '1812', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 3.0', 'in': '0.18 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '1825', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 6.4', 'in': '0.18 x 0.25', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '2010', 'Componente': 'Resistencias, \nCapacitores', 'mm': '5.0 x 2.5', 'in': '0.20 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '2512', 'Componente': 'Resistencias, \nCapacitores', 'mm': '6.3 x 3.2', 'in': '0.25 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '45', 'Imagen': '-'},
            {'Empaquetado': '2920', 'Componente': 'Resistencias, \nCapacitores', 'mm': '7.4 x 5.1', 'in': '0.29 x 0.20', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 02

        # Tabla 03: Lista componentes SMD - CAPACITORES
        table3= [
            {'Empaquetado': '01005', 'Componente': 'Resistencias,\nCapacitores', 'mm': '0.4 x 0.2', 'in': '0.01 x 0.005', 'Peso aprox \n(g/1000 pzas.)': '0.04', 'Imagen': '-'},
            {'Empaquetado': '0201', 'Componente': 'Resistencias, \nCapacitores', 'mm': '0.6 x 0.3', 'in': '0.02 x 0.01', 'Peso aprox \n(g/1000 pzas.)': '0.15', 'Imagen': '-'},
            {'Empaquetado': '0402', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.0 x 0.5', 'in': '0.04 x 0.02', 'Peso aprox \n(g/1000 pzas.)': '0.8', 'Imagen': '-'},
            {'Empaquetado': '0603', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.5 x 0.8', 'in': '0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '2', 'Imagen': '-'},
            {'Empaquetado': '0805', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '2.0 x 1.3', 'in': '0.08 x 0.05', 'Peso aprox \n(g/1000 pzas.)': '4', 'Imagen': '-'},
            {'Empaquetado': '1206', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '3.0 x 1.5', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '10', 'Imagen': '-'},
            {'Empaquetado': '1210', 'Componente': 'Resistencias, \nCapacitores', 'mm': '3.2 x 2.5', 'in': '0.125 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '16', 'Imagen': '-'},
            {'Empaquetado': '1806', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.5 x 1.6', 'in': '0.18 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '1812', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 3.0', 'in': '0.18 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '1825', 'Componente': 'Resistencias, \nCapacitores', 'mm': '4.6 x 6.4', 'in': '0.18 x 0.25', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '2010', 'Componente': 'Resistencias, \nCapacitores', 'mm': '5.0 x 2.5', 'in': '0.20 x 0.10', 'Peso aprox \n(g/1000 pzas.)': '27', 'Imagen': '-'},
            {'Empaquetado': '2512', 'Componente': 'Resistencias, \nCapacitores', 'mm': '6.3 x 3.2', 'in': '0.25 x 0.125', 'Peso aprox \n(g/1000 pzas.)': '45', 'Imagen': '-'},
            {'Empaquetado': '2920', 'Componente': 'Resistencias, \nCapacitores', 'mm': '7.4 x 5.1', 'in': '0.29 x 0.20', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 03

        # Tabla 04: Lista componentes SMD - LEDS
        table4= [
            {'Empaquetado': '0402', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.0 x 0.5', 'in': '0.04 x 0.02', 'Peso aprox \n(g/1000 pzas.)': '0.8', 'Imagen': '-'},
            {'Empaquetado': '0603', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '1.5 x 0.8', 'in': '0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '2', 'Imagen': '-'},
            {'Empaquetado': '0805', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '2.0 x 1.3', 'in': '0.08 x 0.05', 'Peso aprox \n(g/1000 pzas.)': '4', 'Imagen': '-'},
            {'Empaquetado': '1206', 'Componente': 'LEDs, \nResistencias, \nCapacitores', 'mm': '3.0 x 1.5', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '10', 'Imagen': '-'},
            {'Empaquetado': '3014', 'Componente': 'LEDs', 'mm': '3.0 x 1.4', 'in': '0.12 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '3020', 'Componente': 'LEDs', 'mm': '3.0 x 2.0', 'in': '0.12 x 0.08', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '3528', 'Componente': 'LEDs', 'mm': '3.5 x 2.8', 'in': '0.14 x 0.11', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '5050', 'Componente': 'LEDs', 'mm': '5.0 x 5.0', 'in': '0.20 x 0.20', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': '5730', 'Componente': 'LEDs', 'mm': '5.7 x 3.0', 'in': '0.23 x 0.12', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 04

        # Tabla 05: Lista componentes SMD - TRANSISTORES
        table5= [
            {'Empaquetado': 'SOT - 23', 'Componente': 'Transitores', 'mm': '2.9 x 2.4 x 1.1', 'in': '0.12 x 0.10 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 89', 'Componente': 'Transitores', 'mm': '4.5 x 4.0 x 1.5', 'in': '0.18 x 0.16 x 0.06', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 143', 'Componente': 'Transitores', 'mm': '2.9 x 2.8 x 1.1', 'in': '0.12 x 0.11 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 223', 'Componente': 'Transitores', 'mm': '6.5 x 7.0 x 1.8', 'in': '0.26 x 0.28 x 0.07', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 323', 'Componente': 'Transitores', 'mm': '2.0 x 2.1 x 0.9', 'in': '0.08 x 0.08 x 0.04', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOT - 523', 'Componente': 'Transitores', 'mm': '1.6 x 1.6 x 0.7', 'in': '0.06 x 0.06 x 0.03', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 05

        # Tabla 06: Lista componentes SMD - CIRCUITO INTEGRADO
        table6= [
            {'Empaquetado': 'SO - 8', 'Componente': 'Circuito Integrado', 'mm': '3.8 x 4.8', 'in': '0.15 x 0.19', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'TSSOP - 8', 'Componente': 'Circuito Integrado', 'mm': '3.1 x 4.5', 'in': '0.12 x 0.18', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SSOP - 8', 'Componente': 'Circuito Integrado', 'mm': '2.9 x 3.15', 'in': '0.12 x 0.12', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
            {'Empaquetado': 'SOP - 8', 'Componente': 'Circuito Integrado', 'mm': '6.5 x 5.6', 'in': '0.26 x 0.22', 'Peso aprox \n(g/1000 pzas.)': '-', 'Imagen': '-'},
        ]   # Fin Tabla 06

        # Generar Widgets TABLE
        smd1 = QTableWidget(self)
        smd2 = QTableWidget(self)
        smd3 = QTableWidget(self)
        smd4 = QTableWidget(self)
        smd5 = QTableWidget(self)
        smd6 = QTableWidget(self)

        # Fijar estilos de widgets
        smd1.setStyleSheet(st_table)
        smd2.setStyleSheet(st_table)
        smd3.setStyleSheet(st_table)
        smd4.setStyleSheet(st_table)
        smd5.setStyleSheet(st_table)
        smd6.setStyleSheet(st_table)
        
        # Establecer número de columnas
        smd1.setColumnCount(6)
        smd2.setColumnCount(6)
        smd3.setColumnCount(6)
        smd4.setColumnCount(6)
        smd5.setColumnCount(6)
        smd6.setColumnCount(6)

        # Fijar títulos de tabla (HEADER)
        smd1.setHorizontalHeaderLabels(table1[0].keys())
        smd2.setHorizontalHeaderLabels(table2[0].keys())
        smd3.setHorizontalHeaderLabels(table3[0].keys())
        smd4.setHorizontalHeaderLabels(table4[0].keys())
        smd5.setHorizontalHeaderLabels(table5[0].keys())
        smd6.setHorizontalHeaderLabels(table6[0].keys())

        # Fijar conteo de filas
        smd1.setRowCount(len(table1))
        smd2.setRowCount(len(table2))
        smd3.setRowCount(len(table3))
        smd4.setRowCount(len(table4))
        smd5.setRowCount(len(table5))
        smd6.setRowCount(len(table6))

        # Llenado de TABLA 01
        row = 0
        for e in table1:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd1.setItem(row, 0, qitem0)
            smd1.setItem(row, 1, qitem1)
            smd1.setItem(row, 2, qitem2)
            smd1.setItem(row, 3, qitem3)
            smd1.setItem(row, 4, qitem4)
            smd1.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)
        
        # Llenado de TABLA 02
        row = 0
        for e in table2:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd2.setItem(row, 0, qitem0)
            smd2.setItem(row, 1, qitem1)
            smd2.setItem(row, 2, qitem2)
            smd2.setItem(row, 3, qitem3)
            smd2.setItem(row, 4, qitem4)
            smd2.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)
        
        # Llenado de TABLA 03
        row = 0
        for e in table3:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd3.setItem(row, 0, qitem0)
            smd3.setItem(row, 1, qitem1)
            smd3.setItem(row, 2, qitem2)
            smd3.setItem(row, 3, qitem3)
            smd3.setItem(row, 4, qitem4)
            smd3.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)
        
        # Llenado de TABLA 04
        row = 0
        for e in table4:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd4.setItem(row, 0, qitem0)
            smd4.setItem(row, 1, qitem1)
            smd4.setItem(row, 2, qitem2)
            smd4.setItem(row, 3, qitem3)
            smd4.setItem(row, 4, qitem4)
            smd4.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)
        
        # Llenado de TABLA 05
        row = 0
        for e in table5:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd5.setItem(row, 0, qitem0)
            smd5.setItem(row, 1, qitem1)
            smd5.setItem(row, 2, qitem2)
            smd5.setItem(row, 3, qitem3)
            smd5.setItem(row, 4, qitem4)
            smd5.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)
        
        # Llenado de TABLA 06
        row = 0
        for e in table6:
            qitem0 = QTableWidgetItem(e['Empaquetado'])
            qitem1 = QTableWidgetItem(e['Componente'])
            qitem2 = QTableWidgetItem(e['mm'])
            qitem3 = QTableWidgetItem(e['in'])
            qitem4 = QTableWidgetItem(e['Peso aprox \n(g/1000 pzas.)'])
            qitem5 = QTableWidgetItem(e['Imagen'])
            smd6.setItem(row, 0, qitem0)
            smd6.setItem(row, 1, qitem1)
            smd6.setItem(row, 2, qitem2)
            smd6.setItem(row, 3, qitem3)
            smd6.setItem(row, 4, qitem4)
            smd6.setItem(row, 5, qitem5)
            row += 1
            qitem0.setTextAlignment(Qt.AlignCenter)
            qitem1.setTextAlignment(Qt.AlignCenter)
            qitem2.setTextAlignment(Qt.AlignCenter)
            qitem3.setTextAlignment(Qt.AlignCenter)
            qitem4.setTextAlignment(Qt.AlignCenter)
            qitem5.setTextAlignment(Qt.AlignCenter)

        # Ajustar tamaño de columnas
        smd1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        smd2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        smd3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        smd4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        smd5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        smd6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ajustar tamaño de filas
        smd1.resizeRowsToContents()
        smd2.resizeRowsToContents()
        smd3.resizeRowsToContents()
        smd4.resizeRowsToContents()
        smd5.resizeRowsToContents()
        smd6.resizeRowsToContents()

        # Agregar tablas a pestañas
        tab_widget.addTab(smd1, "General")
        tab_widget.addTab(smd2, "Resistores")
        tab_widget.addTab(smd3, "Capacitores")
        tab_widget.addTab(smd4, "LEDs")
        tab_widget.addTab(smd5, "Transistores")
        tab_widget.addTab(smd6, "Circuitos Integrados")
        tab_widget.setStyleSheet(st_tab)

        # Fijar tamaño de pestañas
        w = self.w * 0.9
        h = self.h * 0.75
        tab_widget.setFixedSize(w, h)

        # Agregar pestaña con tablas a LAYOUT PRINCIPAL
        main_layout.addWidget(tab_widget, alignment = Qt.AlignCenter)
        
        # Button 01: Volver a MENU
        self.btn_start = QPushButton("Volver")  # Generar PushBUtton VOLVER A MENU
        self.btn_start.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_start.sizeHint().width() * 1.3 # Guardar valor de ancho para widget
        h = self.btn_start.sizeHint().height() + 10  # Guardar valor de alto para widget
        self.btn_start.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT PRINCIPAL
        
        # Fijar LAYOUT PRINCIPAL en widget SMD
        self.setLayout(main_layout)
        
