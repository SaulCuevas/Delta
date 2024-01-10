# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

ESTADÍSTICAS
- Ventana muestra tabla de datos de información relacionados con
  estadísticas de errores y tiempo de operación.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QDesktopWidget)

# CLASE ESTADISTICAS - WIDGET
class ESTADISTICAS(QWidget):
    # Constructor
    def __init__(self):
        # Configuración pantalla GUI
        super().__init__()
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        self.font_size1 = int(self.h/20) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/30) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/50) # Valor de fuente 3 ajustado a tamaño pantalla
        self.font_size4 = int(self.h/40) # Valor de fuente 4 ajustado a tamaño pantalla
        self.border_width = int(self.h/100) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/60) # Valor de radius width (button) ajustado a tamaño pantalla
        # Generación layouts generales
        main_layout = QVBoxLayout()

        # --- LISTA DE WIDGETS ---
        # 01. Label 01: Etiqueta para titulo de ventana ESTADÍSTICAS
        # 02. Table 01: Widget de tabla para registro de estadísticas
        # 03. Button 01: Volver a ventana de MENU

    # ----- STYLE VARIABLES -----------------------------------------------------
        verde_oscuro = "rgb(35, 155, 86)"
        azul_claro = "rgb(84, 153, 199)"
        azul_oscuro = "rgb(21, 67, 96)"

        # Style Label Widgets
        st_label = "QLabel { "
        st_label += "background-color: lightgreen; "
        st_label += "border-style: none; "
        st_label += "font-weight: bold; "
        st_label += "font-family: Georgia; "
        st_label += f"font-size: {self.font_size2}pt; "
        st_label += "padding: 3px }"

        # Style Table Widget
        st_table = "QHeaderView::section {"
        st_table += "font-weight: bold; "
        st_table += "font-family: Georgia; "
        st_table += f"font-size: {self.font_size2}pt; "
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
        
        # Label 01: Etiqueta para titulo de ventana ESTADÍSTICAS
        lbl_estadisticas = QLabel("ESTADÍSTICAS")   # Generar Label Ventana INVENTARIO SMD
        lbl_estadisticas.setAlignment(Qt.AlignCenter)   # Alinear texto en el centro
        lbl_estadisticas.setStyleSheet(st_label)    # Fijar estilo de widget
        w = lbl_estadisticas.sizeHint().width() * 1.1    # Guardar valor de ancho para widget
        h = lbl_estadisticas.sizeHint().height()    # Guardar valor de alto para widget
        lbl_estadisticas.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(lbl_estadisticas, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT PRINCIPAL
        
        # Table 01: Widget de tabla para registro de estadísticas
        stats_table = QTableWidget()
        labels = ['\tHoras', '\tMinutos', '\tUsuarios']   # Títulos de datos estadísticas a mostrar
        stats_table.setStyleSheet(st_table) # Fijar estilo de widget
        stats_table.setColumnCount(1)   # Establecer número de columnas
        stats_table.setRowCount(len(labels))    # Establecer número de filas
        stats_table.setVerticalHeaderLabels(labels) # Fijar valor de títulos estadísticas
        stats_table.verticalHeader().setVisible(True)   # Mostrar header Verticales (lateral)
        stats_table.horizontalHeader().setVisible(False)    # Ocultar header Horizontales (arriba)
        stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)    # Ajustar columnas a tamaño de widget
        stats_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)    # Permitir modificar ancho de columna
        w = stats_table.verticalHeader().sizeHint().width() * 1.5   # Obtener valor de ancho de columna HEADER
        h = stats_table.verticalHeader().sizeHint().height() * 1.5   # Obtener valor de alto de columna HEADER
        stats_table.verticalHeader().setFixedWidth(int(w))  # Fijar ancho de columna HEADER
        stats_table.verticalHeader().setDefaultSectionSize(int(h))  # Fijar ancho de columna HEADER
        
        # Fijar tamaño de tabla
        w = self.w * 0.85
        h = self.h * 0.7
        stats_table.setFixedSize(w, h)
        main_layout.addWidget(stats_table, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT PRINCIPAL
        
        # Button 01: Volver a ventana de MENU
        self.btn_start = QPushButton("Volver")  # Generar PushBUtton VOLVER A MENU
        self.btn_start.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_start.sizeHint().width() * 1.3 # Guardar valor de ancho para widget
        h = self.btn_start.sizeHint().height() * 1.1  # Guardar valor de alto para widget
        self.btn_start.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT PRINCIPAL
        
        # Fijar LAYOUT PRINCIPAL en widget ESTADISTICAS
        self.setLayout(main_layout)
        
