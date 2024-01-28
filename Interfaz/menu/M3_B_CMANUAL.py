# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:14:09 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

CONTROL MANUAL
- Ventana muestra botones para control y monitoreo de sensores
  y actuadores del sistema. Utilizada para pruebas y mantenimiento,
  con lo que se puede verificar el correcto funcionamiento de cada
  elemento.
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
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QLabel,
    QWidget,
    QComboBox,
    QPushButton,
    QDialog,
    QLineEdit,
    QSlider,
    QCheckBox)
from toggle import ToggleButton
import qtawesome as qta
import numpy as np
from time import sleep

import cmanual.B0_DESACTIVADO as desactivado
import cmanual.B1_INVENTARIO as inventario
import cmanual.B2_POLEA as tool_polea
import cmanual.B3_CAMERA as tool_camera
import cmanual.B4_SOLDADURA as tool_solder
import cmanual.B5_PICKPLACE as tool_pp

import ESP32_serial as esp
import DeltaEcuaciones as eq

# CLASE CONTROL MANUAL - WIDGET
class CMANUAL(QWidget):
    # Constructor
    def __init__(self, port):
        # Configuración pantalla GUI
        super().__init__()
        print("\nVENTANA -CONTROL MANUAL- CREADA\n")
        # Inicializacion de variables
        validator = QDoubleValidator(-999.99, 999.99, 100)  # Inicialización validador dato numérico
        validator.setNotation(QDoubleValidator.StandardNotation)    # Fijar tipo de notación (ESTANDAR, sin abreviaturas ni exponentes)
        self.port = port    # Guardar valor de puerto para envío de instrucciones
        self.ser = esp.start_serial(self.port)  # Inicialización de Puerto Serial
        self.period = 100   # Valor de periodo para lectura de encoders
        self.timer = QTimer()   # Inicialización de Timer
        self.timer.setInterval(self.period) # Fijar intervalo de timer a periodo
        self.timer.timeout.connect(self.read_encoders)  # Conectar timer a función
        self.inc = 0.00 # Inicialización de incremento para posición
        self.last_tool = 1  # Guardar valor de última herramienta
        self.encoders = True    # Bandera para lectura de encoders
        # Set Point de coordenada
        self.x_sp = 0.00
        self.y_sp = 0.00
        self.z_sp = 0.00
        # Set Point ángulos de motor
        self.m1_rad_sp = 0.00
        self.m1_deg_sp = 0.00
        self.m2_rad_sp = 0.00
        self.m2_deg_sp = 0.00
        self.m3_rad_sp = 0.00
        self.m3_deg_sp = 0.00
        # Valor medido de coordenada
        self.x_val = 0.00 # Motor 1
        self.y_val = 0.00 # Motor 2
        self.z_val = 0.00 # Motor 3
        # Valor medido ángulos de motor
        self.pnp_val = 0.00 # Motor 4
        self.chtool_val = 0.00 # Motor 5
        self.invent_val = 0.00 # Motor 6
        # Obtener dimensiones pantalla
        self.w = QDesktopWidget().screenGeometry().width()
        self.h = QDesktopWidget().screenGeometry().height()
        self.font_size1 = int(self.h/20) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/30) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/40) # Valor de fuente 3 ajustado a tamaño pantalla
        self.font_size4 = int(self.h/50) # Valor de fuente 4 ajustado a tamaño pantalla
        self.font_size5 = int(self.h/60) # Valor de fuente 5 ajustado a tamaño pantalla
        self.font_size6 = int(self.h/70) # Valor de fuente 6 ajustado a tamaño pantalla
        self.border_width = int(self.h/150) # Valor de border width (button) ajustado a tamaño pantalla
        self.border_radius = int(self.h/100) # Valor de radius width (button) ajustado a tamaño pantalla
        self.pad = int(self.h/150) # Valor de padding
        # Generación layouts generales
        main_layout = QVBoxLayout()
        # TOP LAYOUT Y WIDGET
        top_layout = QHBoxLayout()
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        # MIDDLE LAYOUTS Y WIDGETS
        middle_layout = QHBoxLayout()
        middle_widget = QWidget()
        middle_widget.setLayout(middle_layout)
        ml_tool_layout = QVBoxLayout()
        ml_tool_widget = QWidget()
        ml_tool_widget.setLayout(ml_tool_layout)
        ml_vel_layout = QVBoxLayout()
        ml_vel_widget = QWidget()
        ml_vel_widget.setLayout(ml_vel_layout)
        ml_coord_layout = QVBoxLayout()
        ml_coord_widget = QWidget()
        ml_coord_widget.setLayout(ml_coord_layout)
        ml_action_layout = QVBoxLayout()
        ml_action_widget = QWidget()
        ml_action_widget.setLayout(ml_action_layout)
        ml_new_layout = QVBoxLayout()
        ml_new_widget = QWidget()
        ml_new_widget.setLayout(ml_new_layout)
        # BOTTOM LAYOUTS Y WIDGETS
        bottom_layout = QHBoxLayout()
        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        self.cpos_layout = QVBoxLayout()
        cpos_widget = QWidget()
        cpos_widget.setLayout(self.cpos_layout)
        self.tool_layout = QStackedLayout()
        tool_widget = QWidget()
        tool_widget.setLayout(self.tool_layout)
    
        # --- LISTA DE WIDGETS ------
        # 01. Label 01: Títutlo de WIDGET - CONTROL MANUAL
        # 02. Label 02: Etiqueta Coordenadas TOP LAYOUT
        # 03. Label 03: Valor Coordenadas TOP LAYOUT
        # 04. Label 04: Etiqueta Herramienta TOP LAYOUT
        # 05. Label 05: Valor Herramienta TOP LAYOUT
        # 06. Label 06: Etiqueta Velocidad TOP LAYOUT
        # 07. Label 07: Valor Velocidad TOP LAYOUT
        # 08. Checkbox 01: Activar/Desactivar HERRAMIENTA LAYOUT
        # 09. ComboBox 01: Selección de HERRAMIENTA LAYOUT
        # 10. Checkbox 02: Activar/Desactivar cambio de VELOCIDAD LAYOUT
        # 11. Slider 01: Ajustar valor de VELOCIDAD
        # 12. Label 08: Ticks para Slider 01
        # 13. Label 09: Valor de VELOCIDAD seleccionada
        # 14. Label 10: Etiqueta de titulo para coordenadas actuales COORD LAYOUT
        # 15. Switch 01: TOOGLE BUTTON para cambio de medida angulo en COORD LAYOUT
        # 16. Label 11: Etiqueta coordenadas X/M1 COORD LAYOUT
        # 17. LineEdit 01: Valor FIJO coordenadas X/M1 COORD LAYOUT
        # 18. LineEdit 02: Valor MEDIDO coordenadas X/M1 COORD LAYOUT
        # 19. Label 12: Dimension coordenadas X/M1 COORD LAYOUT
        # 20. Label 13: Etiqueta coordenadas Y/M2 COORD LAYOUT
        # 21. LineEdit 03: Valor FIJO coordenadas Y/M2 COORD LAYOUT
        # 22. LineEdit 04: Valor MEDIDO coordenadas Y/M2 COORD LAYOUT
        # 23. Label 14: Dimension coordenadas Y/M2 COORD LAYOUT
        # 24. Label 15: Etiqueta coordenadas Z/M3 COORD LAYOUT
        # 25. LineEdit 05: Valor FIJO coordenadas Y/M2 COORD LAYOUT
        # 26. LineEdit 06: Valor MEDIDO coordenadas Z/M3 COORD LAYOUT
        # 27. Label 16: Dimension coordenadas Z/M3 COORD LAYOUT
        # 28. Button 01: Flecha de acción -> fijar nuevas coordenadas ACTION LAYOUT
        # 29. Button 02: Flecha de acción -> enviar comando a PORT ACTION LAYOUT
        # 30. Label 17: Etiqueta de titulo para coordenadas nuevas NEW LAYOUT
        # 31. LineEdit 07: Valor NUEVO coordenadas X/M1 NEW LAYOUT
        # 32. LineEdit 08: Valor NUEVO coordenadas Y/M2 NEW LAYOUT
        # 33. LineEdit 09: Valor NUEVO coordenadas Z/M3 NEW LAYOUT
        # 34. Button 03 [M1-]: Desplazamiento negativo en Motor 1
        # 35. Button 04 [M1+]: Desplazamiento positivo en Motor 1
        # 36. Button 05 [M2-]: Desplazamiento negativo en Motor 2
        # 37. Button 06 [M2+]: Desplazamiento positivo en Motor 2
        # 38. Button 07 [M3-]: Desplazamiento negativo en Motor 3
        # 39. Button 08 [M3+]: Desplazamiento positivo en Motor 3
        # 40. Button 09 [X-]: Desplazamiento en X negativo coordenadas rectangulares
        # 41. Button 10 [X+]: Desplazamiento en X positivo coordenadas rectangulares
        # 42. Button 11 [Y-]: Desplazamiento en Y negativo coordenadas rectangulares
        # 43. Button 12 [Y+]: Desplazamiento en Y positivo coordenadas rectangulares
        # 44. Button 13 [Z-]: Desplazamiento en Z negativo coordenadas rectangulares
        # 45. Button 14 [Z+]: Desplazamiento en Z positivo coordenadas rectangulares
        # 46. Switch 02: TOOGLE BUTTON para cambio de coordenadas CONTROL POS LAYOUT
        # 47. Label 18: Etiqueta de tipo de COORDENADAS actual
        # 48. Label 19: Etiqueta panel de herramientas TOOL LAYOUT
        # 49. Button 15: Iniciar uso de CONTROL MANUAL
        # 50. Label 20: Etiqueta herramienta desactivada TOOL LAYOUT
        # 51. Widget 01: DISABLE TOOL WIDGET
        # 52. Label 21: Etiqueta herramiental inventario TOOL LAYOUT
        # 53. Widget 02: INVENTORY TOOL WIDGET
        # 54. Label 22: Etiqueta herramiental riel y polea TOOL LAYOUT
        # 55. Widget 03: POLEA TOOL WIDGET
        # 56. Label 23: Etiqueta herramienta cámara TOOL LAYOUT
        # 57. Widget 04: CAMERA TOOL WIDGET
        # 58. Label 24: Etiqueta herramienta soldadura TOOL LAYOUT
        # 59. Widget 05: SOLDADURA TOOL WIDGET
        # 60. Label 25: Etiqueta herramienta p&p TOOL LAYOUT
        # 61. Widget 06: PICK & PLACE TOOL WIDGET
        # 62. Button 16: Volver a MENU

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
        st_label += f"font-size: {self.font_size6}pt; "
        st_label += "padding: 3px; "
        st_label += "}"

        # Style TOP WIDGET
        st_top = "QWidget { "
        st_top += "color: white; "
        st_top += "background-color: blue; "
        st_top += "border-style: outset; "
        st_top += "border-width: 2px; "
        st_top += "border-radius: 5px; "
        st_top += "border-color: black; "
        st_top += "font-weight: bold; "
        st_top += "font-family: Georgia; "
        st_top += f"font-size: {self.font_size4}pt; "
        st_top += "margin: 0px; "
        st_top += "padding: 0px; "
        st_top += "}"

        # Style CheckBox
        st_chb = "QCheckBox { "
        st_chb += "border: 0px solid black; "
        st_chb += "spacing: 5px; "
        st_chb += "}"

        st_chb += "QCheckBox::indicator { "
        st_chb += f"width: {self.font_size2}px; "
        st_chb += f"height: {self.font_size2}px; "
        st_chb += "border: 3px solid; "
        st_chb += "border-color: rgb(20, 60, 100); "
        st_chb += f"border-radius: {self.font_size5}px; "
        st_chb += "}"

        st_chb += "QCheckBox::indicator:disabled { "
        st_chb += "border-color: rgb(150,150,150); "
        st_chb += "}"

        st_chb += "QCheckBox::indicator:checked { "
        st_chb += "background-color: rgb(40, 200, 110); "
        st_chb += "}"
        
        st_chb += "QCheckBox:enabled { "
        st_chb += "font-weight: bold; "
        st_chb += "font-family: Times New Roman; "
        st_chb += f"font-size: {self.font_size2}pt; "
        st_chb += "}"

        st_chb += "QCheckBox:disabled {"
        st_chb += "color: rgb(150,150,150); "
        st_chb += "}"

        # Style de ComboBox
        st_cb = "QComboBox { "
        st_cb += "font-family: Times New Roman; "
        st_cb += f"font-size: {self.font_size3}pt; "
        st_cb += "}"

        st_cb += "QComboBox:enabled { "
        st_cb += "border: 2px solid black; "
        st_cb += "background-color: white; "
        st_cb += "}"

        st_cb += "QComboBox:disabled { "
        st_cb += "border: 2px dotted black; "
        st_cb += "}"

        # Style MULTIPLE MIDDLE WIDGETS (TOOL/VEL)
        st_mmlw = "QWidget { "
        st_mmlw += "color: black; "
        #st_mmlw += "background-color: lightblue; "
        st_mmlw += "border-style: solid; "
        st_mmlw += "border-width: 0px; "
        st_mmlw += "border-right-width: 1px; "
        st_mmlw += "border-radius: 0px; "
        st_mmlw += "border-color: black; "
        st_mmlw += "font: 14px; "
        st_mmlw += "padding: 2px; "
        st_mmlw += "}"

        # Style ACTION MIDDLE WIDGETS
        st_amlw = "QWidget { "
        st_amlw += "color: black; "
        #st_amlw += "background-color: lightblue; "
        st_amlw += "border-style: solid; "
        st_amlw += "border-width: 0px; "
        st_amlw += "border-left-width: 1px; "
        st_amlw += "border-right-width: 1px; "
        st_amlw += "border-radius: 0px; "
        st_amlw += "border-color: black; "
        st_amlw += "font: 14px; "
        st_amlw += "padding: 2px; "
        st_amlw += "}"

        # Style NEW COORD WIDGET
        st_nmlw = "QWidget { "
        st_nmlw += "color: black; "
        #st_nmlw += "background-color: lightblue; "
        st_nmlw += "border-style: solid; "
        st_nmlw += "border-width: 0px; "
        st_nmlw += "border-radius: 0px; "
        st_nmlw += "border-color: black; "
        st_nmlw += "font: 14px; "
        st_nmlw += "padding: 2px; "
        st_nmlw += "}"

        # Style COORD MIDDLE WIDGETS
        st_cml = "QWidget { "
        st_cml += "color: black; "
        #st_cml += "background-color: lightblue; "
        st_cml += "border-style: dotted; "
        st_cml += "border-width: 0px; "
        st_cml += "border-radius: 0px; "
        st_cml += "border-color: black; "
        st_cml += "font: bold 14px; "
        st_cml += "padding: 2px; "
        st_cml += "}"

        # Style Slider
        h = 10
        st_sld = "QSlider {"
        st_sld += "border: 0px; "
        st_sld += f"margin-top: {h+1}px; "
        st_sld += f"margin-bottom: {h+1}px; "
        st_sld += "}"

        st_sld += "QSlider::groove:horizontal {"
        st_sld += "border: 1px solid #000088; "
        st_sld += f"height: {h}px; "
        st_sld += "background: white; "
        st_sld += f"margin: {h // 4}px 0;"
        st_sld += f"border-radius: {int(h * 0.4)}px; "
        st_sld += "}"

        st_sld += "QSlider::handle:horizontal {"
        st_sld += "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc); "
        st_sld += "border: 2px solid; "
        st_sld += f"width: {h*3}px; "
        st_sld += f"margin: {h * 1.5 * -1} 0; "
        st_sld += f"border-radius: {int(h * 0.4)}px; "
        st_sld += "}"

        st_sld += "QSlider::add-page:horizontal {"
        st_sld += "background: #fff; "
        st_sld += "border: 1px solid #777; "
        st_sld += f"height: {h}px; "
        st_sld += "}"

        st_sld += "QSlider::sub-page:horizontal {"
        st_sld += "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #66e, stop: 1 #bbf); "
        st_sld += "background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, stop: 0 #bbf, stop: 1 #55f); "
        st_sld += "border: 1px solid #777; "
        st_sld += f"height: {h}px; "
        st_sld += "}"

        st_sld += "QSlider::add-page:horizontal:disabled {"
        st_sld += "background: #eee; "
        st_sld += "border-color: #999; "
        st_sld += "}"

        st_sld += "QSlider::sub-page:horizontal:disabled {"
        st_sld += "background: #bbb; "
        st_sld += "border-color: #999; "
        st_sld += "}"

        st_sld += "QSlider::handle:horizontal:disabled {"
        st_sld += "background: #eee; "
        st_sld += "border: 1px solid #aaa; "
        st_sld += "}"

        # Style Label ALT VEL
        st_lbl_alt = "QLabel {"
        st_lbl_alt += "font-family: Georgia; "
        st_lbl_alt += f"font-size: {self.font_size3}pt; "
        st_lbl_alt += "font-style: italic; "
        st_lbl_alt += "padding: 0px; "
        st_lbl_alt += "margin: 0px; "
        st_lbl_alt += "border: 0px dotted; "
        st_lbl_alt += "}"

        # Style Action Button
        st_act_btn = "QPushButton:enabled { "
        st_act_btn += "background-color: rgb(40, 150, 40); "
        st_act_btn += "border-style: outset; "
        st_act_btn += "border-width: 2px; "
        st_act_btn += "border-radius: 5px; "
        st_act_btn += "border-color: green; "
        st_act_btn += "padding: 3px; "
        st_act_btn += "}"
        
        st_act_btn += "QPushButton:hover { "
        st_act_btn += "background-color: rgb(220, 220, 0); "
        st_act_btn += "border-style: inset; "
        st_act_btn += "}"
        
        st_act_btn += "QPushButton:pressed { "
        st_act_btn += "background-color: rgb(0, 80, 220); "
        st_act_btn += "border-style: inset; "
        st_act_btn += "}"

        # Style MIDDLE WIDGET
        st_middle = "QWidget { "
        st_middle += "color: black; "
        st_middle += "background-color: rgb(220, 220, 220); "
        st_middle += "border-style: solid; "
        st_middle += "border-width: 1px; "
        st_middle += "border-bottom-width: 1px; "
        st_middle += "border-radius: 0px; "
        st_middle += "border-color: black; "
        st_middle += "font-weight: normal; "
        st_middle += "font-family: Georgia; "
        st_middle += "font-size: 12pt; "
        st_middle += "margin: 0px; "
        st_middle += "padding: 0px; "
        st_middle += "}"

        # Style Motor Button
        st_btn_motor = "QPushButton { "
        st_btn_motor += "border-style: outset; "
        st_btn_motor += "border-width: 5px; "
        st_btn_motor += "border-radius: 20px; "
        st_btn_motor += "font-weight: bold; "
        st_btn_motor += "font-family: Georgia; "
        st_btn_motor += "font-size: " + str(self.font_size2) + "pt; "
        st_btn_motor += f"padding: {self.pad}px; "
        st_btn_motor += "}"
        
        st_btn_motor += "QPushButton:enabled { "
        st_btn_motor += "background-color: rgb(41, 128, 185); "
        st_btn_motor += "border-color: rgb(26, 82, 118); "
        st_btn_motor += "}"
        
        st_btn_motor += "QPushButton:hover { "
        st_btn_motor += "background-color: rgb(155, 89, 182); "
        st_btn_motor += "border-color: rgb(187, 143, 206); "
        st_btn_motor += "border-style: groove; "
        st_btn_motor += "}"
        
        st_btn_motor += "QPushButton:pressed { "
        st_btn_motor += "background-color: rgb(192, 57, 43); "
        st_btn_motor += "border-color: rgb(231, 76, 60); "
        st_btn_motor += "border-style: inset; "
        st_btn_motor += "}"

        # Style XYZ Button
        st_btn_xyz = "QPushButton { "
        st_btn_xyz += "border-style: outset; "
        st_btn_xyz += "border-width: 5px; "
        st_btn_xyz += "border-radius: 20px; "
        st_btn_xyz += "font-weight: bold; "
        st_btn_xyz += "font-family: Georgia; "
        st_btn_xyz += "font-size: " + str(self.font_size2) + "pt; "
        st_btn_xyz += "padding: " + str(self.pad) + "px; "
        st_btn_xyz += "}"
        
        st_btn_xyz += "QPushButton:enabled { "
        st_btn_xyz += "background-color: rgb(41, 128, 185); "
        st_btn_xyz += "border-color: rgb(26, 82, 118); "
        st_btn_xyz += "}"
        
        st_btn_xyz += "QPushButton:hover { "
        st_btn_xyz += "background-color: rgb(155, 89, 182); "
        st_btn_xyz += "border-color: rgb(187, 143, 206); "
        st_btn_xyz += "border-style: groove; "
        st_btn_xyz += "}"
        
        st_btn_xyz += "QPushButton:pressed { "
        st_btn_xyz += "background-color: rgb(192, 57, 43); "
        st_btn_xyz += "border-color: rgb(231, 76, 60); "
        st_btn_xyz += "border-style: inset; "
        st_btn_xyz += "}"

        # Style Label Coordenadas
        st_lbl_coord = "QLabel { "
        st_lbl_coord += "font-family: Georgia; "
        st_lbl_coord += "font-size: 11pt; "
        st_lbl_coord += "padding: 0px; "
        st_lbl_coord += "border-width: 0px; "
        st_lbl_coord += "}"

        # Style Button Widgets
        st_btn = "QPushButton { "
        st_btn += "background-color: lightgreen; "
        st_btn += "border-style: outset; "
        st_btn += f"border-width: {self.border_width}px; "
        st_btn += f"border-radius: {self.border_radius}px; "
        st_btn += "border-color: green; "
        st_btn += "font-weight: bold; "
        st_btn += "font-family: Georgia; "
        st_btn += f"font-size: {self.font_size6}pt; "
        st_btn += "padding: 3px; "
        st_btn += "}"

        st_btn += "QPushButton:hover { "
        st_btn += f"background-color: {verde_oscuro}; "
        st_btn += "border-color: green; "
        st_btn += "border-style: inset; "
        st_btn += "}"

        st_btn += "QPushButton:pressed { "
        st_btn += f"background-color: {azul_claro}; "
        st_btn += f"border-color: {azul_oscuro}; "
        st_btn += "border-style: inset; "
        st_btn += "}"

        # Style Button Widgets (ALT)
        st_alt = "QPushButton { "
        st_alt += "background-color: rgb(41, 128, 185); "
        st_alt += "border-style: outset; "
        st_alt += "border-width: 5px; "
        st_alt += "border-radius: 20px; "
        st_alt += "border-color: rgb(26, 82, 118); "
        st_alt += "font-weight: bold; "
        st_alt += "font-family: Georgia; "
        st_alt += "font-size: 25pt; "
        st_alt += "padding: 10px; "
        st_alt += "}"
        
        st_alt += "QPushButton:hover { "
        st_alt += "background-color: rgb(155, 89, 182); "
        st_alt += "border-color: rgb(187, 143, 206); "
        st_alt += "border-style: groove; "
        st_alt += "}"
        
        st_alt += "QPushButton:pressed { "
        st_alt += "background-color: rgb(192, 57, 43); "
        st_alt += "border-color: rgb(231, 76, 60); "
        st_alt += "border-style: inset; "
        st_alt += "}"

        # Style TOOL WIDGET
        st_tool = "{ "
        st_tool += "color: black; "
        st_tool += "background-color: rgb(200, 200, 200); "
        st_tool += "border-style: solid; "
        st_tool += "border-width: 1px; "
        st_tool += "border-radius: 0px; "
        st_tool += "border-color: black; "
        st_tool += "font-weight: normal; "
        st_tool += "font-family: Georgia; "
        st_tool += "font-size: 12pt; "
        st_tool += "margin: 0px; "
        st_tool += "padding: 0px; "
        st_tool += "}"

        # Style BOTTOM WIDGET
        st_bottom = "QWidget { "
        st_bottom += "color: black; "
        st_bottom += "background-color: rgb(220, 220, 220); "
        st_bottom += "border-style: solid; "
        st_bottom += "border-width: 0px; "
        #st_bottom += "border-bottom-width: 0px; "
        st_bottom += "border-radius: 0px; "
        st_bottom += "border-color: black; "
        st_bottom += "font-weight: normal; "
        st_bottom += "font-family: Georgia; "
        st_bottom += "font-size: 12pt; "
        st_bottom += "margin: 0px; "
        st_bottom += "padding: 0px; "
        st_bottom += "}"

        # Style Label Aux
        st_lbl_aux = "QLabel {"
        st_lbl_aux += "font-family: Georgia; "
        st_lbl_aux += f"font-size: {self.font_size4}pt; "
        st_lbl_aux += "font-style: italic; "
        st_lbl_aux += "font-weight: bold; "
        st_lbl_aux += "padding: 0px; "
        st_lbl_aux += "margin: 0px; "
        st_lbl_aux += "border: 0px dotted; "
        st_lbl_aux += "}"

# ----- PRINCIPAL WIDGET -----------------------------------------------------

        # Label 01: Títutlo de WIDGET - CONTROL MANUAL
        lbl_cmanual = QLabel("CONTROL MANUAL")  # Generar Label Ventana CONTROL MANUAL
        lbl_cmanual.setAlignment(Qt.AlignCenter)    # Alinear texto en el centro
        lbl_cmanual.setStyleSheet(st_label) # Fijar estilo de widget
        w = lbl_cmanual.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_cmanual.sizeHint().height() # Guardar valor de alto para widget
        lbl_cmanual.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        main_layout.addStretch(1)   # Anexar espaciado entre widget
        main_layout.addWidget(lbl_cmanual, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT PRINCIPAL
        main_layout.addStretch(1)   # Anexar espaciado entre widget

# ------- TOP LAYOUT (ACCESO DATOS RAPIDO) ------------------------------------------------------
        
        # Label 02: Etiqueta Coordenadas TOP LAYOUT
        top_coord = QLabel("COORD:")    # Generar Label Etiqueta COORDENADAS
        top_coord.setStyleSheet("border-width: 0px;")   # Fijar estilo de widget
        top_layout.addStretch(1)    # Anexar espaciado entre widget
        top_layout.addWidget(top_coord) # Agregar widget a LAYOUT TOP
        
        # Label 03: Valor Coordenadas TOP LAYOUT
        self.top_typecrd = QLabel("R/M")    # Generar Label Valor COORDENADAS
        self.top_typecrd.setStyleSheet("border-width: 0px;")    # Fijar estilo de widget
        top_layout.addWidget(self.top_typecrd)  # Agregar widget a LAYOUT TOP
        top_layout.addStretch(3)    # Anexar espaciado entre widget
        
        # Label 04: Etiqueta Herramienta TOP LAYOUT
        top_herr = QLabel("TOOL:")  # Generar Label Etiqueta HERRAMIENTA
        top_herr.setStyleSheet("border-width: 0px;")    # Fijar estilo de widget
        top_layout.addWidget(top_herr)  # Agregar widget a LAYOUT TOP
        
        # Label 05: Valor Herramienta TOP LAYOUT
        self.top_typeh = QLabel("D/I/R/C/S/P")    # Generar Label Valor HERRAMIENTA
        self.top_typeh.setStyleSheet("border-width: 0px;")  # Fijar estilo de widget
        top_layout.addWidget(self.top_typeh)    # Agregar widget a LAYOUT TOP
        top_layout.addStretch(3)    # Anexar espaciado entre widget
        
        # Label 06: Etiqueta Velocidad TOP LAYOUT
        top_vel = QLabel("VEL:")    # Generar Label Etiqueta VELOCIDAD
        top_vel.setStyleSheet("border-width: 0px;") # Fijar estilo de widget
        top_layout.addWidget(top_vel)   # Agregar widget a LAYOUT TOP
        
        # Label 07: Valor Velocidad TOP LAYOUT
        self.top_typev = QLabel("1/2/3/4")  # Generar Label Valor VELOCIDAD
        self.top_typev.setStyleSheet("border-width: 0px;")  # Fijar estilo de widget
        top_layout.addWidget(self.top_typev)    # Agregar widget a LAYOUT TOP
        top_layout.addStretch(1)    # Anexar espaciado entre widget
        
        # Configuración TOP WIDGET
        top_widget.setStyleSheet(st_top)    # Fijar estilo de TOP WIDGET
        top_widget.setFixedWidth(self.w * 0.95)  # Ajustar tamaño TOP WIDGET
        main_layout.addWidget(top_widget, alignment = Qt.AlignCenter)   # Agregar TOP WIDGET a LAYOUT PRINCIPAL
        main_layout.addStretch(0)   # Quitar espaciado con siguiente widget
        
# ------- MIDDLE LAYOUT -------------------------------------------------------
    
    # ----- LAYOUT HERRAMIENTA (VERTICAL 1) ---------------------------------------------
    
        # Checkbox 01: Activar/Desactivar HERRAMIENTA LAYOUT
        self.chb_tool = QCheckBox("Herramienta:")   # Generar CheckBox para cambio de HERRAMIENTA
        self.chb_tool.setEnabled(False) # Desactivado al INICIO
        self.chb_tool.stateChanged.connect(self.click_tool) # Conectar a función para cambio de estado
        self.chb_tool.setStyleSheet(st_chb) # Fijar estilo de widget
        w = self.chb_tool.sizeHint().width()    # Guardar valor de ancho para widget
        h = self.chb_tool.sizeHint().height()   # Guardar valor de alto para widget
        self.chb_tool.setFixedSize(w, h)    # Ajustar valores de ancho (w) y alto (h) para widget
        ml_tool_layout.addWidget(self.chb_tool, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT HERRAMIENTA
        
        # ComboBox 01: Selección de HERRAMIENTA LAYOUT
        self.cb_tool = QComboBox()  # Generar ComboBox para selección de HERRAMIENTA
        items = ["DESACTIVADO", "INVENTARIO", "RIEL Y POLEA", "CÁMARA", "SOLDADURA", "PICK & PLACE"]   # Lista de Valores para ComboBox
        self.cb_tool.addItems(items)    # Agregar lista de valores
        self.cb_tool.activated.connect(self.change_tool)    # Conectar a función para selección de HERRAMIENTA
        self.cb_tool.view().setRowHidden(0, True)   # Fijar y ocultar primer valor de lista
        self.cb_tool.setEnabled(False)  # Desactivado al INICIO
        self.cb_tool.setStyleSheet(st_cb)   # Fijar estilo de widget
        self.cb_tool.adjustSize()   # Ajustar tamaño a texto
        w = self.cb_tool.sizeHint().width() * 1.05    # Guardar valor de ancho para widget
        h = self.cb_tool.sizeHint().height()    # Guardar valor de alto para widget
        self.cb_tool.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        ml_tool_layout.addWidget(self.cb_tool, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT HERRAMIENTA
        
        # Configuración TOOL WIDGET
        ml_tool_widget.setStyleSheet(st_mmlw) # Fijar estilo de widget
        w = self.w * 0.22   # Guardar valor de ancho para widget
        ml_tool_widget.setFixedWidth(w)   # Ajustar valores de ancho (w) para widget
        
    # ----- LAYOUT VELOCIDAD (VERTICAL 2) ---------------------------------------------
        
        # Checkbox 02: Activar/Desactivar cambio de VELOCIDAD LAYOUT
        self.chb_vel = QCheckBox("Velocidad:")  # Generar CheckBox para cambio de VELOCIDAD
        self.chb_vel.setEnabled(False)  # Desactivado al INICIO
        self.chb_vel.stateChanged.connect(self.click_vel)   # Conectar a función para cambio de estado
        self.chb_vel.setStyleSheet(st_chb)  # Fijar estilo de widget
        w = self.chb_vel.sizeHint().width() # Guardar valor de ancho para widget
        h = self.chb_vel.sizeHint().height()    # Guardar valor de alto para widget
        self.chb_vel.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        ml_vel_layout.addWidget(self.chb_vel, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT VELOCIDAD
        
        # Slider 01: Ajustar valor de VELOCIDAD
        self.sld_vel = QSlider(Qt.Horizontal)   # Generar SLIDER para control de velocidad
        self.sld_vel.setEnabled(False)  # Desactivado al INICIO
        self.sld_vel.setRange(1,4)  # Fijar rango de slider (4 posiciones)
        self.sld_vel.setStyleSheet(st_sld)
        self.sld_vel.setTickPosition(QSlider.TicksBelow)    # Agregar ticks para cada valor de slider
        self.sld_vel.setTickInterval(1) # Fijar intervalo entre cada tick
        self.sld_vel.valueChanged.connect(self.change_vel)  # Conectar a función para cambio de estado
        w = self.w * 0.15
        h = self.sld_vel.sizeHint().height()
        self.sld_vel.setFixedSize(w, h)
        ml_vel_layout.addWidget(self.sld_vel, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT VELOCIDAD
        
        # Label 08: Ticks para Slider 01
        self.lbl_sld = QLabel("  |         |          |         |  ")    # Generar Label de VELOCIDAD seleccionada
        self.lbl_sld.setAlignment(Qt.AlignCenter)   # Alinear texto al centro
        self.lbl_sld.setStyleSheet("border: 0px dotted; font-size: 10pt;")  # Fijar estilo de widget
        self.lbl_sld.adjustSize()
        w = self.lbl_sld.sizeHint().width() # Guardar valor de ancho para widget
        h = self.lbl_sld.sizeHint().height()    # Guardar valor de alto para widget
        self.lbl_sld.setFixedSize(w + 30, h)    # Ajustar valores de ancho (w) y alto (h) para widget
        ml_vel_layout.addWidget(self.lbl_sld, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT VELOCIDAD

        # Label 09: Valor de VELOCIDAD seleccionada
        self.vels = ["1 : Precisión", "2 : Lenta", "3 : Media", "4 : Alta"] # Lista de posibles valores de velocidad
        self.lbl_vel = QLabel("DESACTIVADO")    # Generar Label de VELOCIDAD seleccionada
        self.lbl_vel.setAlignment(Qt.AlignCenter)   # Alinear texto al centro
        self.lbl_vel.setStyleSheet(st_lbl_alt)  # Fijar estilo de widget
        w = self.lbl_vel.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = self.lbl_vel.sizeHint().height()    # Guardar valor de alto para widget
        self.lbl_vel.setFixedSize(w, h)    # Ajustar valores de ancho (w) y alto (h) para widget
        ml_vel_layout.addWidget(self.lbl_vel, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT VELOCIDAD

        # Configuración VELOCIDAD WIDGET        
        ml_vel_widget.setStyleSheet(st_mmlw)  # Fijar estilo de widget
        w = self.w * 0.18    # Guardar valor de ancho para widget
        ml_vel_widget.setFixedWidth(w)    # Ajustar valores de ancho (w) para widget
    
    # ----- LAYOUT COORDENADAS (VERTICAL 3) ---------------------------------------------
    
        # Generar LAYOUTS de apoyo
        measure_layout = QHBoxLayout()
        x_layout = QHBoxLayout()
        y_layout = QHBoxLayout()
        z_layout = QHBoxLayout()
        # Generar WIDGETS de APOYO
        measure_widget = QWidget()
        x_widget = QWidget()
        y_widget = QWidget()
        z_widget = QWidget()
        # Fijar LAYOUTS a WIDGETS de apoyo
        measure_widget.setLayout(measure_layout)
        x_widget.setLayout(x_layout)
        y_widget.setLayout(y_layout)
        z_widget.setLayout(z_layout)
        # Quitar margins adicionales a widgets
        measure_layout.setContentsMargins(0, 0, 0, 0)
        x_layout.setContentsMargins(0, 0, 0, 0)
        y_layout.setContentsMargins(0, 0, 0, 0)
        z_layout.setContentsMargins(0, 0, 0, 0)
        
    # ***** MEASURE LAYOUT ****************************

        # Label 10: Etiqueta de titulo para coordenadas actuales COORD LAYOUT
        act_coord = QLabel("ACTUALES")  # Generar Label de Etiqueta titulo
        act_coord.setAlignment(Qt.AlignCenter)    # Alinear texto en el centro
        act_coord.setStyleSheet(st_lbl_alt) # Fijar estilo de widget
        act_coord.adjustSize()    # Fijar tamaño a texto
        measure_layout.addWidget(act_coord, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT MEASURE
        measure_layout.addSpacing(30)

        # Switch 01: TOOGLE BUTTON para cambio de medida angulo en COORD LAYOUT
        self.sw_measure = ToggleButton(35)    # Generar ToogleButton para cambio de angulo
        self.sw_measure.setEnabled(False)   # Desactivado al INICIO
        self.sw_measure.clicked.connect(self.change_measure)    # Conectar a función para cambio de estado     
        self.sw_measure.setStyleSheet("")    # Fijar estilo de widget
        measure_layout.addWidget(self.sw_measure, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT MEASURE
    
        # Configuración MESAURE LAYOUT
        ml_coord_layout.addWidget(measure_widget, alignment = Qt.AlignCenter)   # Agregar MEASURE WIDGET a LAYOUT COORD
    
    # ***** X LAYOUT ****************************
        
        # Label 11: Etiqueta coordenadas X/M1 COORD LAYOUT
        self.lbl_x = QLabel("X1:")   # Generar Label de Etiqueta COORD X/M1
        self.lbl_x.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.lbl_x.setStyleSheet(st_lbl_alt) # Fijar estilo de widget
        w = self.lbl_x.sizeHint().width() * 1.5 # Guardar valor de ancho para widget
        self.lbl_x.setFixedWidth(w) # Ajustar valor de ancho (w) para widget
        x_layout.addWidget(self.lbl_x, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD X
        
        # LineEdit 01: Valor FIJO coordenadas X/M1 COORD LAYOUT
        self.x_coord = QLineEdit(f"{self.x_sp:.2f}")    # Generar Label de Valor FIJO COORD X/M1
        self.x_coord.setAlignment(Qt.AlignRight)    # Alinear texto a la derecha
        self.x_coord.setValidator(validator)    # Fijar validador numérico
        self.x_coord.setReadOnly(True)  # Establecer como LineEdit de solo lectura
        self.x_coord.setFixedWidth(100) # Ajustar valor de ancho (w) para widget
        self.x_coord.setStyleSheet("border: 1px solid;")
        x_layout.addWidget(self.x_coord, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT COORD X

        # LineEdit 02: Valor MEDIDO coordenadas X/M1 COORD LAYOUT
        self.x_measure = QLineEdit(f"{self.x_val:.2f}") # Generar Label de Valor MEDIDO COORD X/M1
        self.x_measure.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.x_measure.setValidator(validator)  # Fijar validador numérico
        self.x_measure.setReadOnly(True)    # Establecer como LineEdit de solo lectura
        self.x_measure.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        self.x_measure.setStyleSheet("border: 1px solid;")
        x_layout.addWidget(self.x_measure, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD X

        # Label 12: Dimension coordenadas X/M1 COORD LAYOUT
        self.x_dim = QLabel("rad")  # Generar Label de Dimension COORD X/M1
        self.x_dim.setStyleSheet("border: 0px dotted;")
        self.x_dim.adjustSize() # Ajustar tamaño a texto
        w = self.x_dim.sizeHint().width() * 2.5 # Guardar valor de ancho para widget
        self.x_dim.setFixedWidth(w) # Ajustar valor de ancho (w) para widget
        x_layout.addWidget(self.x_dim, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD X
        
        # Configuración X LAYOUT
        ml_coord_layout.addWidget(x_widget, alignment = Qt.AlignCenter)

    # ***** Y LAYOUT ****************************
        
        # Label 13: Etiqueta coordenadas Y/M2 COORD LAYOUT
        self.lbl_y = QLabel("Y2:")   # Generar Label de Etiqueta COORD Y/M2
        self.lbl_y.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.lbl_y.setStyleSheet(st_lbl_alt) # Fijar estilo de widget
        w = self.lbl_y.sizeHint().width() * 1.5 # Guardar valor de ancho para widget
        self.lbl_y.setFixedWidth(w) # Ajustar valor de ancho (w) para widget
        y_layout.addWidget(self.lbl_y, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD Y
        
        # LineEdit 03: Valor FIJO coordenadas Y/M2 COORD LAYOUT
        self.y_coord = QLineEdit(f"{self.y_sp:.2f}")    # Generar Label de Valor FIJO COORD Y/M2
        self.y_coord.setAlignment(Qt.AlignRight)     # Alinear texto a la derecha
        self.y_coord.setValidator(validator)    # Fijar validador numérico
        self.y_coord.setReadOnly(True)  # Establecer como LineEdit de solo lectura
        self.y_coord.setFixedWidth(100) # Ajustar valor de ancho (w) para widget
        self.y_coord.setStyleSheet("border: 1px solid;")
        y_layout.addWidget(self.y_coord, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT COORD Y

        # LineEdit 04: Valor MEDIDO coordenadas Y/M2 COORD LAYOUT
        self.y_measure = QLineEdit(f"{self.y_val:.2f}") # Generar Label de Valor MEDIDO COORD Y/M2
        self.y_measure.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.y_measure.setValidator(validator)  # Fijar validador numérico
        self.y_measure.setReadOnly(True)    # Establecer como LineEdit de solo lectura
        self.y_measure.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        self.y_measure.setStyleSheet("border: 1px solid;")
        y_layout.addWidget(self.y_measure, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD X

        # Label 14: Dimension coordenadas Y/M2 COORD LAYOUT
        self.y_dim = QLabel("rad")   # Generar Label de Dimension COORD Y/M2
        self.y_dim.setStyleSheet("border: 0px dotted;")
        self.y_dim.adjustSize() # Ajustar tamaño a texto
        w = self.y_dim.sizeHint().width() * 2.5 # Guardar valor de ancho para widget
        self.y_dim.setFixedWidth(w) # Ajustar valor de ancho (w) para widget
        y_layout.addWidget(self.y_dim, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD Y
        
        # Configuración Y LAYOUT
        ml_coord_layout.addWidget(y_widget, alignment = Qt.AlignCenter)

    # ***** Z LAYOUT ****************************
        
        # Label 15: Etiqueta coordenadas Z/M3 COORD LAYOUT
        self.lbl_z = QLabel("Z3:")    # Generar Label de Etiqueta COORD Z/M3
        self.lbl_z.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.lbl_z.setStyleSheet(st_lbl_alt) # Fijar estilo de widget
        w = self.lbl_z.sizeHint().width() * 1.5 # Guardar valor de ancho para widget
        self.lbl_z.setFixedWidth(w)    # Ajustar valor de ancho (w) para widget
        z_layout.addWidget(self.lbl_z, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD Z
        
        # LineEdit 05: Valor FIJO coordenadas Y/M2 COORD LAYOUT
        self.z_coord = QLineEdit(f"{self.z_sp:.2f}")    # Generar Label de Valor FIJO COORD Z/M3
        self.z_coord.setAlignment(Qt.AlignRight)    # Alinear texto a la derecha
        self.z_coord.setValidator(validator)    # Fijar validador numérico
        self.z_coord.setReadOnly(True)  # Establecer como LineEdit de solo lectura
        self.z_coord.setFixedWidth(100) # Ajustar valor de ancho (w) para widget
        self.z_coord.setStyleSheet("border: 1px solid;")
        z_layout.addWidget(self.z_coord, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT COORD Z

        # LineEdit 06: Valor MEDIDO coordenadas Z/M3 COORD LAYOUT
        self.z_measure = QLineEdit(f"{self.z_val:.2f}") # Generar Label de Valor MEDIDO COORD Z/M3
        self.z_measure.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.z_measure.setValidator(validator)  # Fijar validador numérico
        self.z_measure.setReadOnly(True)    # Establecer como LineEdit de solo lectura
        self.z_measure.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        self.z_measure.setStyleSheet("border: 1px solid;")
        z_layout.addWidget(self.z_measure, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD Z

        # Label 16: Dimension coordenadas Z/M3 COORD LAYOUT
        self.z_dim = QLabel("rad")   # Generar Label de Dimension COORD Z/M3
        self.z_dim.setStyleSheet("border: 0px dotted;")
        self.z_dim.adjustSize() # Ajustar tamaño a texto
        w = self.z_dim.sizeHint().width() * 2.5 # Guardar valor de ancho para widget
        self.z_dim.setFixedWidth(w) # Ajustar valor de ancho (w) para widget
        z_layout.addWidget(self.z_dim, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT COORD Z

        # Configuración Z LAYOUT
        ml_coord_layout.addWidget(z_widget, alignment = Qt.AlignCenter)

        # Configuración de COORD LAYOUT
        ml_coord_layout.setSpacing(0)   # Quitar espaciado
        ml_coord_layout.setContentsMargins(0, 0, 0, 0)  # Quitar margins
        ml_coord_widget.setStyleSheet(st_cml)   # Fijar estilo de widget COORD
        w = x_widget.sizeHint().width() # Guardar valor de ancho para widget
        h = x_widget.sizeHint().height()    # Guardar valor de alto para widget
        x_widget.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget X
        y_widget.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget Y
        z_widget.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget Z
        w = self.w * 0.33  # Guardar valor de ancho para widget
        ml_coord_widget.setFixedWidth(w)  # Ajustar valores de ancho (w) para widget COORD
        
    # ----- LAYOUT ACTIONS BUTTONS (VERTICAL 4) ---------------------------------------------

        # Button 01: Flecha de acción -> fijar nuevas coordenadas ACTION LAYOUT
        icon = qta.icon("fa5s.arrow-alt-circle-left")   # Icon FLECHA (QTAWESOME)
        self.btn_arrow = QPushButton(icon, "")  # Generar Button Flecha
        self.btn_arrow.setEnabled(False)    # Desactivado al INICIO
        self.btn_arrow.setIconSize(QSize(40, 40))   # Ajustar tamaño de ícono
        self.btn_arrow.setStyleSheet(st_act_btn) # Fijar estilo de widget
        w = self.btn_arrow.sizeHint().width() * 1.05   # Guardar valor de ancho para widget
        h = self.btn_arrow.sizeHint().height() *1.05  # Guardar valor de alto para widget
        self.btn_arrow.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_arrow.clicked.connect(self.set_coords) # Conectar a función para actualizar coordenadas
        ml_action_layout.addStretch()
        ml_action_layout.addWidget(self.btn_arrow, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT ACCION
        ml_action_layout.addStretch()

        # Button 02: Flecha de acción -> enviar comando a PORT ACTION LAYOUT
        icon = qta.icon("fa.commenting")    # Icon MENSAJE (QTAWESOME)
        self.btn_msg = QPushButton(icon, "")    # Generar Button Mensaje
        self.btn_msg.setEnabled(False)  # Fijar estilo de widget
        self.btn_msg.setIconSize(QSize(30, 30)) # Ajustar tamaño de ícono
        self.btn_msg.setStyleSheet(st_act_btn)   # Fijar estilo de widget
        w = self.btn_msg.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = self.btn_msg.sizeHint().height() * 1.05    # Guardar valor de alto para widget
        self.btn_msg.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_msg.clicked.connect(self.send_msg) # Conectar a función para enviar mensaje a PORT
        ml_action_layout.addWidget(self.btn_msg, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT ACCION
        ml_action_layout.addStretch()
    
        # Configuración de ACTION LAYOUT
        ml_action_layout.setContentsMargins(0, 0, 0, 0)    # Quitar margins
        #ml_action_layout.setSpacing(0) # Quitar espaciado
        ml_action_widget.setStyleSheet(st_amlw)  # Fijar estilo de widget COORD
        w = self.w * 0.1    # Guardar valor de ancho para widget
        ml_action_widget.setFixedWidth(w)    # Ajustar valores de ancho (w) para widget NEW

    # ----- LAYOUT NUEVAS COORD (VERTICAL 5) ---------------------------------------------
    
        # Label 17: Etiqueta de titulo para coordenadas nuevas NEW LAYOUT
        lbl_new = QLabel("Nueva:") # Generar Label de Etiqueta titulo
        lbl_new.setStyleSheet("border: 0px solid;")
        lbl_new.setAlignment(Qt.AlignCenter)    # Alinear texto en el centro
        lbl_new.setStyleSheet(st_lbl_alt) # Fijar estilo de widget
        lbl_new.adjustSize()    # Fijar tamaño a texto
        ml_new_layout.addWidget(lbl_new, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT NEW
        
        # LineEdit 07: Valor NUEVO coordenadas X/M1 NEW LAYOUT
        self.x_new = QLineEdit()    # Generar LineEdit de Valor NUEVO COORD X/M1
        self.x_new.setStyleSheet("border: 1px solid;")
        self.x_new.setEnabled(False)    # Desactivado al INICIO
        self.x_new.setMaxLength(7)  # Tamaño máximo de texto
        self.x_new.setPlaceholderText("000.00") # Texto de inicio (ayuda en el fondo)
        self.x_new.setValidator(validator)  # Fijar validador numérico
        self.x_new.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.x_new.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        ml_new_layout.addWidget(self.x_new, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT NEW
        
        # LineEdit 08: Valor NUEVO coordenadas Y/M2 NEW LAYOUT
        self.y_new = QLineEdit()    # Generar LineEdit de Valor NUEVO COORD Y/M2
        self.y_new.setStyleSheet("border: 1px solid;")
        self.y_new.setEnabled(False)    # Desactivado al INICIO
        self.y_new.setMaxLength(7)  # Tamaño máximo de texto
        self.y_new.setPlaceholderText("000.00") # Texto de inicio (ayuda en el fondo)
        self.y_new.setValidator(validator)  # Fijar validador numérico
        self.y_new.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.y_new.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        ml_new_layout.addWidget(self.y_new, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT NEW
        
        # LineEdit 09: Valor NUEVO coordenadas Z/M3 NEW LAYOUT
        self.z_new = QLineEdit()    # Generar LineEdit de Valor NUEVO COORD Y/M2
        self.z_new.setStyleSheet("border: 1px solid;")
        self.z_new.setEnabled(False)    # Desactivado al INICIO
        self.z_new.setMaxLength(7)  # Tamaño máximo de texto
        self.z_new.setPlaceholderText("000.00") # Texto de inicio (ayuda en el fondo)
        self.z_new.setValidator(validator)  # Fijar validador numérico
        self.z_new.setAlignment(Qt.AlignRight)  # Alinear texto a la derecha
        self.z_new.setFixedWidth(100)   # Ajustar valor de ancho (w) para widget
        ml_new_layout.addWidget(self.z_new, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT NEW
    
        # Configuración de NEW LAYOUT
        ml_new_layout.setSpacing(0) # Quitar espaciado
        ml_new_layout.setContentsMargins(0, 0, 0, 0)    # Quitar margins
        ml_new_widget.setStyleSheet(st_nmlw)  # Fijar estilo de widget COORD
        w = self.w * 0.12    # Guardar valor de ancho para widget
        ml_new_widget.setFixedWidth(w)    # Ajustar valores de ancho (w) para widget NEW
    
    # ----- CONFIG LAYOUT -------------------------------------------------
    
        # Ordenamiento de widgets con su respectivo espaciado
        middle_layout.addWidget(ml_tool_widget)
        middle_layout.addWidget(ml_vel_widget)
        middle_layout.addWidget(ml_coord_widget)
        middle_layout.addWidget(ml_action_widget)
        middle_layout.addWidget(ml_new_widget)
        middle_layout.addStretch()
        
        # Configuración MIDDLE WIDGET
        middle_layout.setContentsMargins(1, 1, 1, 1)
        middle_layout.setSpacing(0)
        middle_widget.setStyleSheet(st_middle)
        middle_widget.setFixedWidth(self.w * 0.95)
        main_layout.addWidget(middle_widget, alignment = Qt.AlignCenter)
        main_layout.addStretch(0)
    
# ------- BOTTOM LAYOUT -------------------------------------------------------
    
    # ----- LAYOUT CONTROL POSICION (VERTICAL 6) ---------------------------------------------
    
        # Generar LAYOUTS de apoyo
        self.x_btn_layout = QHBoxLayout()
        self.y_btn_layout = QHBoxLayout()
        self.z_btn_layout = QHBoxLayout()
        self.m1_btn_layout = QHBoxLayout()
        self.m2_btn_layout = QHBoxLayout()
        self.m3_btn_layout = QHBoxLayout()
        sw_coord_layout = QHBoxLayout()
        sw_coord_layout.setContentsMargins(0, 0, 0, 0)  # Quitar margins
        sw_coord_layout.setSpacing(0)   # Quitar espaciado
        # Generar WIDGETS de APOYO
        self.x_btn_widget = QWidget()
        self.y_btn_widget = QWidget()
        self.z_btn_widget = QWidget()
        self.m1_btn_widget = QWidget()
        self.m2_btn_widget = QWidget()
        self.m3_btn_widget = QWidget()
        sw_coord_widget = QWidget()
        # Fijar LAYOUTS a WIDGETS de apoyo
        self.x_btn_widget.setLayout(self.x_btn_layout)      
        self.y_btn_widget.setLayout(self.y_btn_layout)      
        self.z_btn_widget.setLayout(self.z_btn_layout)   
        self.m1_btn_widget.setLayout(self.m1_btn_layout)      
        self.m2_btn_widget.setLayout(self.m2_btn_layout)      
        self.m3_btn_widget.setLayout(self.m3_btn_layout)   
        sw_coord_widget.setLayout(sw_coord_layout)
        # Generar LAYOUTS intercambiables
        self.xm_layout = QStackedLayout()
        self.ym_layout = QStackedLayout()
        self.zm_layout = QStackedLayout()
        # Quitar margins
        self.xm_layout.setContentsMargins(0, 0, 0, 0)
        self.ym_layout.setContentsMargins(0, 0, 0, 0)
        self.zm_layout.setContentsMargins(0, 0, 0, 0)
        # Agregar widgets a XM LAYOUT
        self.xm_layout.addWidget(self.x_btn_widget)
        self.xm_layout.addWidget(self.m1_btn_widget)
        # Agregar widgets a YM LAYOUT
        self.ym_layout.addWidget(self.y_btn_widget)
        self.ym_layout.addWidget(self.m2_btn_widget)
        # Agregar widgets a ZM LAYOUT
        self.zm_layout.addWidget(self.z_btn_widget)
        self.zm_layout.addWidget(self.m3_btn_widget)
        # Generar WIDGETS para LAYOUT intecambiables
        self.xm_widget = QWidget()
        self.ym_widget = QWidget()
        self.zm_widget = QWidget()
        # Fijar LAYOUTS intercambiables a WIDGETS de apoyo
        self.xm_widget.setLayout(self.xm_layout)
        self.ym_widget.setLayout(self.ym_layout)
        self.zm_widget.setLayout(self.zm_layout)
        # Widgets desactivados de INICIO
        self.xm_widget.setEnabled(False)
        self.ym_widget.setEnabled(False)
        self.zm_widget.setEnabled(False)
        
        # Button 03 [M1-]: Desplazamiento negativo en Motor 1
        self.btn_m1n = QPushButton("M1-")   # Generar PushButton Motor 1 NEGATIVO
        self.btn_m1n.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        w = self.btn_m1n.sizeHint().width() # Guardar valor de ancho para widget
        s = int(w * 1.1)    # Guardar valor de ancho modificado para widgets de control
        self.btn_m1n.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m1n.clicked.connect(self.m1_neg)   # Conectar a función para movimiento
        self.m1_btn_layout.addWidget(self.btn_m1n, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 04 [M1+]: Desplazamiento positivo en Motor 1
        self.btn_m1p = QPushButton("M1+")   # Generar PushButton Motor 1 POSITIVO
        self.btn_m1p.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        self.btn_m1p.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m1p.clicked.connect(self.m1_pos)   # Conectar a función para movimiento
        self.m1_btn_layout.addWidget(self.btn_m1p, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 05 [M2-]: Desplazamiento negativo en Motor 2
        self.btn_m2n = QPushButton("M2-")   # Generar PushButton Motor 2 NEGATIVO
        self.btn_m2n.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        self.btn_m2n.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m2n.clicked.connect(self.m2_neg)   # Conectar a función para movimiento
        self.m2_btn_layout.addWidget(self.btn_m2n, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 06 [M2+]: Desplazamiento positivo en Motor 2
        self.btn_m2p = QPushButton("M2+")   # Generar PushButton Motor 2 POSITIVO
        self.btn_m2p.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        self.btn_m2p.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m2p.clicked.connect(self.m2_pos)   # Conectar a función para movimiento
        self.m2_btn_layout.addWidget(self.btn_m2p, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 07 [M3-]: Desplazamiento negativo en Motor 3
        self.btn_m3n = QPushButton("M3-")   # Generar PushButton Motor 3 NEGATIVO
        self.btn_m3n.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        self.btn_m3n.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m3n.clicked.connect(self.m3_neg)   # Conectar a función para movimiento
        self.m3_btn_layout.addWidget(self.btn_m3n, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 08 [M3+]: Desplazamiento positivo en Motor 3
        self.btn_m3p = QPushButton("M3+")   # Generar PushButton Motor 3 POSITIVO
        self.btn_m3p.setStyleSheet(st_btn_motor)    # Fijar estilo de widget
        self.btn_m3p.setFixedSize(s, w) # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_m3p.clicked.connect(self.m3_pos)   # Conectar a función para movimiento
        self.m3_btn_layout.addWidget(self.btn_m3p, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT CONTROL POS
        
        # Button 09 [X-]: Desplazamiento en X negativo coordenadas rectangulares
        self.btn_xn = QPushButton("X-") # Generar PushButton X NEGATIVO
        self.btn_xn.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_xn.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_xn.clicked.connect(self.x_neg) # Conectar a función para movimiento
        self.x_btn_layout.addWidget(self.btn_xn, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Button 10 [X+]: Desplazamiento en X positivo coordenadas rectangulares
        self.btn_xp = QPushButton("X+") # Generar PushButton X POSITIVO
        self.btn_xp.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_xp.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_xp.clicked.connect(self.x_pos) # Conectar a función para movimiento
        self.x_btn_layout.addWidget(self.btn_xp, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Button 11 [Y-]: Desplazamiento en Y negativo coordenadas rectangulares
        self.btn_yn = QPushButton("Y-") # Generar PushButton Y NEGATIVO
        self.btn_yn.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_yn.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_yn.clicked.connect(self.y_neg) # Conectar a función para movimiento
        self.y_btn_layout.addWidget(self.btn_yn, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Button 12 [Y+]: Desplazamiento en Y positivo coordenadas rectangulares
        self.btn_yp = QPushButton("Y+") # Generar PushButton Y POSITIVO
        self.btn_yp.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_yp.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_yp.clicked.connect(self.y_pos) # Conectar a función para movimiento
        self.y_btn_layout.addWidget(self.btn_yp, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Button 13 [Z-]: Desplazamiento en Z negativo coordenadas rectangulares
        self.btn_zn = QPushButton("Z-") # Generar PushButton Z NEGATIVO
        self.btn_zn.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_zn.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_zn.clicked.connect(self.z_neg) # Conectar a función para movimiento
        self.z_btn_layout.addWidget(self.btn_zn, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Button 14 [Z+]: Desplazamiento en Z positivo coordenadas rectangulares
        self.btn_zp = QPushButton("Z+") # Generar PushButton Y POSITIVO
        self.btn_zp.setStyleSheet(st_btn_xyz)   # Fijar estilo de widget
        self.btn_zp.setFixedSize(s, w)  # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_zp.clicked.connect(self.z_pos) # Conectar a función para movimiento
        self.z_btn_layout.addWidget(self.btn_zp, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Switch 02: TOOGLE BUTTON para cambio de coordenadas CONTROL POS LAYOUT
        self.sw_coord = ToggleButton()  # Generar ToogleButton para cambio de coordenada
        self.sw_coord.setEnabled(False) # Desactivado al INICIO
        self.sw_coord.setStyleSheet("border-top-width: 0px;")   # Fijar estilo de widget
        self.sw_coord.clicked.connect(self.change_coord)    # Conectar a función para cambio de estado
        sw_coord_layout.addWidget(self.sw_coord, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT CONTROL POS
        
        # Label 18: Etiqueta de tipo de COORDENADAS actual
        self.lbl_typecrd = QLabel("RECTANGULARES")  # Generar Label de Etiqueta coordenadas
        self.lbl_typecrd.setAlignment(Qt.AlignCenter)   # Alinear texto en el centro
        self.lbl_typecrd.setStyleSheet(st_lbl_coord)   # Fijar estilo de widget
        w = self.lbl_typecrd.sizeHint().width() * 1.1    # Guardar valor de ancho para widget
        h = self.lbl_typecrd.sizeHint().height() * 1.05   # Guardar valor de alto para widget
        self.lbl_typecrd.setFixedSize(w, h) # Ajustar valores de ancho (w) y alto (h) para widget
        sw_coord_layout.addWidget(self.lbl_typecrd, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT CONTROL POS
        
        # Fijar estilo de Widgets
        self.xm_widget.setStyleSheet("border-width: 0px;")
        self.ym_widget.setStyleSheet("border-width: 0px;")
        self.zm_widget.setStyleSheet("border-width: 0px;")
        sw_coord_widget.setStyleSheet("border-width: 0px; border-top-width: 1px;")
        # Ordenamiento de widgets CONTROL POS LAYOUT
        self.cpos_layout.addWidget(self.xm_widget, alignment = Qt.AlignCenter)
        self.cpos_layout.addWidget(self.ym_widget, alignment = Qt.AlignCenter)
        self.cpos_layout.addWidget(self.zm_widget, alignment = Qt.AlignCenter)
        self.cpos_layout.addWidget(sw_coord_widget, alignment = Qt.AlignCenter)
        # Configurar CONTROL POS LAYOUT
        self.cpos_layout.setContentsMargins(1, 1, 1, 1) # Quitar margins
        self.cpos_layout.setSpacing(0)  # Quitar espaciado
        w = sw_coord_widget.sizeHint().width()  # Guardar valor de ancho para widget
        bh = self.xm_widget.sizeHint().height() # Guardar valor de alto para widget
        h = sw_coord_widget.sizeHint().height() # Guardar valor de alto para widget
        w_v5 = cpos_widget.sizeHint().width()   # Guardar valor de ancho para widget
        h_v5 = (bh * 3) + h    # Guardar valor de alto para widget
        # print(f"h_v5: {h_v5}")
        h_min = int(self.h * 0.55)  # Guardar valor mínimo de altura
        # print(f"h_min: {h_min}")
        if (h_min > h_v5):
            bh = (h_min//15) * 4
            h = h_min - (bh * 3) - 5
        h_v5 = (bh * 3) + h    # Guardar valor de alto para widget
        self.xm_widget.setFixedSize(w, bh)  # Ajustar valores de ancho (w) y alto (h) para widget X/M1
        self.ym_widget.setFixedSize(w, bh)  # Ajustar valores de ancho (w) y alto (h) para widget Y/M2
        self.zm_widget.setFixedSize(w, bh)  # Ajustar valores de ancho (w) y alto (h) para widget Z/M3
        sw_coord_widget.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget SW
        # Configuración CONTROL POS WIDGET
        cpos_widget.setFixedSize(w_v5, h_v5)    # Ajustar valores de ancho (w) y alto (h) para widget
        cpos_widget.setStyleSheet("border-width: 1px; border-right-width: 0px; border-top-width: 0px; ")
    
    # ----- LAYOUT TOOL OPERATION (VERTICAL 6) ---------------------------------------------
    
        # Generar LAYOUTS de apoyo
        begin_layout = QVBoxLayout()
        disable_layout = QVBoxLayout()
        inventory_layout = QVBoxLayout()
        polea_layout = QVBoxLayout()
        camera_layout = QVBoxLayout()
        solder_layout = QVBoxLayout()
        pp_layout = QVBoxLayout()
        # Generar WIDGETS de APOYO
        begin_widget = QWidget()
        disable_widget = QWidget()
        inventory_widget = QWidget()
        polea_widget = QWidget()
        camera_widget = QWidget()
        solder_widget = QWidget()
        pp_widget = QWidget()
        # Fijar LAYOUTS a WIDGETS de apoyo
        begin_widget.setLayout(begin_layout)
        disable_widget.setLayout(disable_layout)
        inventory_widget.setLayout(inventory_layout)
        polea_widget.setLayout(polea_layout)
        camera_widget.setLayout(camera_layout)
        solder_widget.setLayout(solder_layout)
        pp_widget.setLayout(pp_layout)
        # Fijar estilos de widgtes
        begin_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        disable_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        inventory_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        polea_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        camera_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        solder_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        pp_widget.setStyleSheet("border-width: 1px; border-top-width: 0px; ")
        
    # ***** BEGIN LAYOUT ***************************
        
        # Label 19: Etiqueta panel de herramientas TOOL LAYOUT
        lbl_begin = QLabel("Panel de Herramientas") # Generar Label Titulo Panel Herramientas
        lbl_begin.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_begin.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        begin_layout.addStretch(3)  # Agregar espaciado
        begin_layout.addWidget(lbl_begin, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT TOOL
        begin_layout.addStretch(1)  # Agregar espaciado
        
        # Button 15: Iniciar uso de CONTROL MANUAL
        self.btn_begin = QPushButton("INICIAR") # Generar PushButton INICIAR CMANUAL
        self.btn_begin.setStyleSheet(st_alt)    # Fijar estilo de widget
        self.btn_begin.clicked.connect(self.begin_operation)    # Conectar a función para iniciar operación
        begin_layout.addWidget(self.btn_begin, alignment = Qt.AlignCenter)  # Agregar widget a LAYOUT TOOL
        begin_layout.addStretch(4)  # Agregar espaciado
        
    # ***** DISABLE LAYOUT ***************************

        # Label 20: Etiqueta herramienta desactivada TOOL LAYOUT
        lbl_disable = QLabel("DESACTIVADO")  # Generar Label Titulo Herramienta Desactivada
        lbl_disable.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_disable.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_disable.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_disable.sizeHint().height() # Guardar valor de alto para widget
        lbl_disable.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        disable_layout.addWidget(lbl_disable, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT TOOL
        
        # Widget 01: DISABLE TOOL WIDGET
        tool_disable_widget = QWidget()    # Generar WIDGET auxiliar
        tool_disable_widget.setStyleSheet("border: 0px dotted; ")
        base = (self.w * 0.95) - w_v5
        altura = h_v5
        self.layout_disable = desactivado.DESACTIVADO(self.ser, base, altura) # Generar LAYOUT INVENTARIO
        tool_disable_widget.setLayout(self.layout_disable)   # Fijar LAYOUT INVENTARIO a WIDGET auxiliar
        tool_disable_widget.setFixedSize(base - 2, altura - h - 2) # Ajustar tamaño de DISABLE WIDGET
        disable_layout.addWidget(tool_disable_widget, alignment = Qt.AlignCenter)  # Agregar Widget a LAYOUT DISABLE
        disable_layout.addStretch()

    # ***** INVENTORY LAYOUT ***************************

        # Label 21: Etiqueta herramienta inventario TOOL LAYOUT
        lbl_inventory = QLabel("INVENTARIO")  # Generar Label Titulo Herramienta Desactivada
        lbl_inventory.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_inventory.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_inventory.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_inventory.sizeHint().height() # Guardar valor de alto para widget
        lbl_inventory.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        inventory_layout.addWidget(lbl_inventory, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT TOOL
        
        # Widget 02: INVENTORY TOOL WIDGET
        tool_inventory_widget = QWidget()    # Generar WIDGET auxiliar
        tool_inventory_widget.setStyleSheet("border: 0px dotted; ")
        base = (self.w * 0.95) - w_v5
        altura = h_v5
        self.layout_inventory = inventario.INVENTORY(self.ser, base, altura) # Generar LAYOUT INVENTARIO
        tool_inventory_widget.setLayout(self.layout_inventory)   # Fijar LAYOUT INVENTARIO a WIDGET auxiliar
        tool_inventory_widget.setFixedSize(base - 2, altura - h - 2) # Ajustar tamaño de DISABLE WIDGET
        inventory_layout.addWidget(tool_inventory_widget, alignment = Qt.AlignCenter)  # Agregar Widget a LAYOUT DISABLE
        inventory_layout.addStretch()

    # ***** POLEA LAYOUT ***************************

        # Label 22: Etiqueta herramiental riel y polea TOOL LAYOUT
        lbl_polea = QLabel("RIEL Y POLEA")    # Generar Label Titulo Herramienta Ninguna
        lbl_polea.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_polea.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_polea.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_polea.sizeHint().height() # Guardar valor de alto para widget
        lbl_polea.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        polea_layout.addWidget(lbl_polea, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT TOOL
        
        # Widget 03: POLEA TOOL WIDGET
        tool_polea_widget = QWidget()    # Generar WIDGET auxiliar
        tool_polea_widget.setStyleSheet("border: 0px dotted; ")
        self.layout_polea = tool_polea.TOOL_N(self.ser, base, altura)   # Generar LAYOUT NINGUNA
        tool_polea_widget.setLayout(self.layout_polea)    # Fijar LAYOUT NINGUNA a WIDGET auxiliar
        tool_polea_widget.setFixedSize(base - 2, altura - h - 2) # Ajustar tamaño de NONE WIDGET
        polea_layout.addWidget(tool_polea_widget, alignment = Qt.AlignCenter) # Agregar Widget a LAYOUT NONE
        polea_layout.addStretch()
        
    # ***** CAMERA LAYOUT ***************************

        # Label 23: Etiqueta herramienta cámara TOOL LAYOUT
        lbl_camera = QLabel("CÁMARA")   # Generar Label Titulo Herramienta Cámara
        lbl_camera.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_camera.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_camera.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_camera.sizeHint().height() # Guardar valor de alto para widget
        lbl_camera.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        camera_layout.addWidget(lbl_camera, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT TOOL

        # Widget 04: CAMERA TOOL WIDGET
        tool_camera_widget = QWidget()  # Generar WIDGET auxiliar
        tool_camera_widget.setStyleSheet("border: 0px dotted; ")
        self.layout_camera = tool_camera.TOOL_C(self.ser, base, altura)   # Generar LAYOUT CAMERA
        tool_camera_widget.setLayout(self.layout_camera)    # Fijar LAYOUT CAMERA a WIDGET auxiliar
        tool_camera_widget.setFixedSize(base - 2, altura - h - 2)   # Ajustar tamaño de CAMERA WIDGET
        camera_layout.addWidget(tool_camera_widget, alignment = Qt.AlignCenter) # Agregar Widget a LAYOUT CAMERA
        camera_layout.addStretch()
        
    # ***** SOLDERING LAYOUT ***************************

        # Label 24: Etiqueta herramienta soldadura TOOL LAYOUT
        lbl_solder = QLabel("SOLDADURA")    # Generar Label Titulo Herramienta Soldadura
        lbl_solder.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_solder.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_solder.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_solder.sizeHint().height() # Guardar valor de alto para widget
        lbl_solder.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        solder_layout.addWidget(lbl_solder, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT TOOL
        
        # Widget 05: SOLDADURA TOOL WIDGET
        tool_solder_widget = QWidget()  # Generar WIDGET auxiliar
        tool_solder_widget.setStyleSheet("border: 0px dotted; ")
        layout_solder = tool_solder.TOOL_S(self.ser, base, altura)   # Generar LAYOUT SOLDERING
        tool_solder_widget.setLayout(layout_solder) # Fijar LAYOUT SOLDERING a WIDGET auxiliar
        tool_solder_widget.setFixedSize(base - 2, altura - h - 2)  # Ajustar tamaño de CAMERA WIDGET
        solder_layout.addWidget(tool_solder_widget, alignment = Qt.AlignCenter) # Agregar Widget a LAYOUT CAMERA
        solder_layout.addStretch()
        
    # ***** PICK & PLACE LAYOUT ***************************

        # Label 25: Etiqueta herramienta p&p TOOL LAYOUT
        lbl_pp = QLabel("PICK & PLACE") # Generar Label Titulo Herramienta PnP
        lbl_pp.setStyleSheet(st_lbl_aux) # Fijar estilo de widget
        lbl_pp.setAlignment(Qt.AlignCenter)  # Alinear texto al centro
        w = lbl_pp.sizeHint().width() * 1.05 # Guardar valor de ancho para widget
        h = lbl_pp.sizeHint().height() # Guardar valor de alto para widget
        lbl_pp.setFixedSize(w, h)  # Ajustar valores de ancho (w) y alto (h) para widget
        pp_layout.addWidget(lbl_pp, alignment = Qt.AlignCenter) # Agregar widget a LAYOUT TOOL
        
        # Widget 06: PICK & PLACE TOOL WIDGET
        tool_pp_widget = QWidget()  # Generar WIDGET auxiliar
        tool_pp_widget.setStyleSheet("border: 0px dotted; ")
        self.layout_pp = tool_pp.TOOL_P(self.ser, base, altura)  # Generar LAYOUT PnP
        tool_pp_widget.setLayout(self.layout_pp)    # Fijar LAYOUT PnP a WIDGET auxiliar
        tool_pp_widget.setFixedSize(base - 2, altura - h - 2)  # Ajustar tamaño de PnP WIDGET
        pp_layout.addWidget(tool_pp_widget, alignment = Qt.AlignCenter) # Agregar Widget a LAYOUT PnP
        pp_layout.addStretch()

    # ***** CONFIGURATION TOOL WIDGETS *************************** 

        # Fijar tamaño de WIDGETS
        begin_widget.setFixedSize(base, altura)
        disable_widget.setFixedSize(base, altura)
        inventory_widget.setFixedSize(base, altura)
        polea_widget.setFixedSize(base, altura)
        camera_widget.setFixedSize(base, altura)
        solder_widget.setFixedSize(base, altura)
        pp_widget.setFixedSize(base, altura)
        # Quitar espaciados
        begin_layout.setSpacing(0)
        disable_layout.setSpacing(0)
        inventory_layout.setSpacing(0)
        polea_layout.setSpacing(0)
        camera_layout.setSpacing(0)
        solder_layout.setSpacing(0)
        pp_layout.setSpacing(0)
        # Quitar margins
        begin_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        disable_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        inventory_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        polea_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        camera_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        solder_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        pp_layout.setContentsMargins(0, 0, 0, 0)   #Quitar margins
        # Agregar WIDGETS a TOOL LAYOUT
        self.tool_layout.addWidget(begin_widget)
        self.tool_layout.addWidget(disable_widget)
        self.tool_layout.addWidget(inventory_widget)
        self.tool_layout.addWidget(polea_widget)
        self.tool_layout.addWidget(camera_widget)
        self.tool_layout.addWidget(solder_widget)
        self.tool_layout.addWidget(pp_widget)
    
        # Configurar TOOL LAYOUT
        self.tool_layout.setAlignment(Qt.AlignCenter)
        self.tool_layout.setContentsMargins(1, 1, 1, 1)   #Quitar margins
        self.tool_layout.setSpacing(0)    # Quitar espaciado
        tool_widget.setStyleSheet(st_tool)
        tool_widget.setFixedSize(base, altura)
        
    # ----- CONFIG BOTTOM LAYOUT -------------------------------------------------
        
        # Agregar widgets
        bottom_layout.addWidget(cpos_widget)
        bottom_layout.addWidget(tool_widget)
        
        # Configuración BOTTOM WIDGET
        bottom_layout.setContentsMargins(0, 0, 0, 0)    # Quitar margins
        bottom_layout.setSpacing(0) # Quitar espaciado
        bottom_widget.setStyleSheet(st_bottom)  # Fijar estilo de widget
        bottom_widget.setFixedWidth(self.w * 0.95)   # Ajustar ancho de widget
        main_layout.addWidget(bottom_widget, alignment = Qt.AlignCenter)    # Agregar widget a LAYOUT PRINCIPAL
        main_layout.addStretch(1)   # Agregar espaciado
    
# ------- SALIDA ----------------------------------------------------------
        
        # Button 16: Volver a MENU
        self.btn_start = QPushButton("Volver")  # Generar PushBUtton VOLVER A MENU  
        self.btn_start.setStyleSheet(st_btn)    # Fijar estilo de widget
        w = self.btn_start.sizeHint().width() * 1.3 # Guardar valor de ancho para widget
        h = self.btn_start.sizeHint().height() * 1.05  # Guardar valor de alto para widget
        self.btn_start.setFixedSize(w, h)   # Ajustar valores de ancho (w) y alto (h) para widget
        self.btn_start.clicked.connect(self.stop_cam)   # Conectar a función para detener cámara
        main_layout.addWidget(self.btn_start, alignment = Qt.AlignCenter)   # Agregar widget a LAYOUT PRINCIPAL
        main_layout.addStretch(1)   # Agregar espacio
        
# ------- MAIN LAYOUT -----------------------------------------------------

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.m1_btn_widget.hide()
        self.m2_btn_widget.hide()
        self.m3_btn_widget.hide()
        self.setLayout(main_layout)
    
############## FUNCIONES ADICIONALES ##############################################
    
    # FUNCIÓN 01 (Switch 01): Cambiar dimensión de coordenadas MOTORES/RECT
    def change_measure(self, on_off):
        if (on_off == True):
            x_text = f"{self.m1_deg_sp:.2f}"
            y_text = f"{self.m2_deg_sp:.2f}"
            z_text = f"{self.m3_deg_sp:.2f}"
            self.x_dim.setText("°")
            self.y_dim.setText("°")
            self.z_dim.setText("°")
        else:
            x_text = f"{self.m1_rad_sp:.4f}"
            y_text = f"{self.m2_rad_sp:.4f}"
            z_text = f"{self.m3_rad_sp:.4f}"
            self.x_dim.setText("rad")
            self.y_dim.setText("rad")
            self.z_dim.setText("rad")
        self.x_coord.setText(x_text)
        self.y_coord.setText(y_text)
        self.z_coord.setText(z_text)

    # FUNCIÓN 02 (Switch 02): Cambiar coordenadas MOTORES/RECT
    def change_coord(self, on_off):
        if on_off == False:
            self.sw_measure.hide()
            self.xm_layout.setCurrentIndex(0)
            self.ym_layout.setCurrentIndex(0)
            self.zm_layout.setCurrentIndex(0)
            self.top_typecrd.setText('R')
            self.lbl_x.setText("X:")
            self.lbl_y.setText("Y:")
            self.lbl_z.setText("Z:")
            x_text = f"{self.x_sp:.2f}"
            y_text = f"{self.y_sp:.2f}"
            z_text = f"{self.z_sp:.2f}"
            self.lbl_typecrd.setText('RECTANGULARES')
            self.x_dim.setText('mm')
            self.y_dim.setText('mm')
            self.z_dim.setText('mm')
        else:
            self.sw_measure.show()
            self.xm_layout.setCurrentIndex(1)
            self.ym_layout.setCurrentIndex(1)
            self.zm_layout.setCurrentIndex(1)
            self.top_typecrd.setText('M')
            self.lbl_x.setText("M1:")
            self.lbl_y.setText("M2:")
            self.lbl_z.setText("M3:")
            self.lbl_typecrd.setText('MOTORES')
            if (self.sw_measure.toggle_on == False):
                x_text = f"{self.m1_rad_sp:.4f}"
                y_text = f"{self.m2_rad_sp:.4f}"
                z_text = f"{self.m3_rad_sp:.4f}"
                self.x_dim.setText('rad')
                self.y_dim.setText('rad')
                self.z_dim.setText('rad')
            else:
                x_text = f"{self.m1_deg_sp:.2f}"
                y_text = f"{self.m2_deg_sp:.2f}"
                z_text = f"{self.m3_deg_sp:.2f}"
                self.x_dim.setText('°')
                self.y_dim.setText('°')
                self.z_dim.setText('°')
        self.x_coord.setText(x_text)
        self.y_coord.setText(y_text)
        self.z_coord.setText(z_text)
    
    # FUNCIÓN 03 (ComboBox 01): Cambiar layout de herramienta
    def change_tool(self, x):
        if x != 0:
            self.last_tool = x
        if x == 0:
            self.top_typeh.setText("D")
            self.tool_layout.setCurrentIndex(1)
        elif x == 1:
            self.top_typeh.setText("I")
            self.tool_layout.setCurrentIndex(2)
        elif x == 2:
            self.top_typeh.setText("R")
            self.tool_layout.setCurrentIndex(3)
        elif x == 3:
            self.top_typeh.setText("C")
            self.tool_layout.setCurrentIndex(4)
            # Herramienta seleccionada
            self.tool = 0
            esp.cambio_herramienta(self.ser, self.tool)
            # T : Seleccion de herramienta
            # 0 - mover motor M5 a pos de Camara
            # 1 - mover motor M5 a pos de Dispensador
            # 2 - mover motor M5 a pos de Manipulador PnP
        elif x == 4:
            self.top_typeh.setText("S")
            self.tool_layout.setCurrentIndex(5)
            # Herramienta seleccionada
            self.tool = 1
            esp.cambio_herramienta(self.ser, self.tool)
            # T : Seleccion de herramienta
            # 0 - mover motor M5 a pos de Camara
            # 1 - mover motor M5 a pos de Dispensador
            # 2 - mover motor M5 a pos de Manipulador PnP
        elif x == 5:
            self.top_typeh.setText("P")
            self.tool_layout.setCurrentIndex(6)
            # Herramienta seleccionada
            self.tool = 2
            esp.cambio_herramienta(self.ser, self.tool)
            temp = esp.read_ESP32(self.ser)
            # T : Seleccion de herramienta
            # 0 - mover motor M5 a pos de Camara
            # 1 - mover motor M5 a pos de Dispensador
            # 2 - mover motor M5 a pos de Manipulador PnP
            
    # FUNCIÓN 04 (Slider 01): Cambiar velocidad de movimiento
    def change_vel(self, value):
        # print(value)
        if value == 1:
            self.top_typev.setText("1")
            self.lbl_vel.setText(self.vels[0])
            self.inc = 0.5
        elif value == 2:
            self.top_typev.setText("2")
            self.lbl_vel.setText(self.vels[1])
            self.inc = 1
        elif value == 3:
            self.top_typev.setText("3")
            self.lbl_vel.setText(self.vels[2])
            self.inc = 2
        elif value == 4:
            self.top_typev.setText("4")
            self.lbl_vel.setText(self.vels[3])
            self.inc = 5
        #self.chb_vel.setChecked(False)
        #self.sld_vel.setEnabled(False)
        
    # FUNCIÓN 05 (Button 15): Condiciones para inicio de operación
    def begin_operation(self):
        self.chb_tool.setEnabled(True)
        self.chb_vel.setEnabled(True)
        self.btn_arrow.setEnabled(True)
        self.btn_msg.setEnabled(True)
        self.x_new.setEnabled(True)
        self.y_new.setEnabled(True)
        self.z_new.setEnabled(True)
        self.xm_widget.setEnabled(True)
        self.ym_widget.setEnabled(True)
        self.zm_widget.setEnabled(True)
        self.sw_measure.setEnabled(True)
        self.sw_coord.setEnabled(True)
        self.sw_coord.pushToggle()
        self.tool_layout.setCurrentIndex(1)
        self.top_typecrd.setText("M")
        self.top_typeh.setText("D")
        self.top_typev.setText("1")
        self.chb_tool.setChecked(False)
        self.chb_vel.setChecked(False)
        self.lbl_vel.setText(self.vels[0])
        self.inc = 0.5
        #Inicialización Timer
        esp.HOME_herramienta(self.ser)
        temp = esp.read_ESP32(self.ser)
        print(f"H-> {temp}")
        while(temp[0:5] != "ready"):
            temp = esp.read_ESP32(self.ser)
        print(f"H-> {temp}")
        sleep(0.01)
        esp.cambio_herramienta(self.ser, 0)
        temp = esp.read_ESP32(self.ser)
        print(f"T-> {temp}")
        while(temp[0:5] != "ready"):
            temp = esp.read_ESP32(self.ser)
        print(f"T-> {temp}")
        self.read_encoders()
        self.m1_rad_sp = self.x_val
        self.m2_rad_sp = self.y_val
        self.m3_rad_sp = self.z_val
        self.actualizar_datos_sp(1)
        x_text = f"{self.m1_rad_sp:.4f}"
        y_text = f"{self.m2_rad_sp:.4f}"
        z_text = f"{self.m3_rad_sp:.4f}"
        self.x_coord.setText(x_text)
        self.y_coord.setText(y_text)
        self.z_coord.setText(z_text)
        self.timer.start()

    # FUNCIÓN 06 (Checkbox 01): Activar/Desactivar herramienta
    def click_tool(self):
        if self.chb_tool.isChecked():
            self.cb_tool.setEnabled(True)
            self.cb_tool.setCurrentIndex(self.last_tool)
            self.change_tool(self.last_tool)
        else:
            self.cb_tool.setEnabled(False)
            self.cb_tool.setCurrentIndex(0)
            self.change_tool(0)
            
    # FUNCIÓN 07 (Checkbox 02): Activar/Desactivar cambio de velocidad
    def click_vel(self):
        if self.chb_vel.isChecked():
            self.sld_vel.setEnabled(True)
        else:
            self.sld_vel.setEnabled(False)
            
    # FUNCIÓN 08 (Button 01): Fijar coordenadas
    def set_coords(self):
        x = self.x_new.text()
        y = self.y_new.text()
        z = self.z_new.text()
        if x != "":
            self.x_sp = float(x)
            self.m1_rad_sp = float(x)
            self.m1_deg_sp = float(x)
        if y != "":
            self.y_sp = float(y)
            self.m2_rad_sp = float(y)
            self.m2_deg_sp = float(y)
        if z != "":
            self.z_sp = float(z)
            self.m3_rad_sp = float(z)
            self.m3_deg_sp = float(z)
        if self.sw_coord.toggle_on == False:
            self.actualizar_datos_sp(0)
            x_text = f"{self.x_sp:.2f}"
            y_text = f"{self.y_sp:.2f}"
            z_text = f"{self.z_sp:.2f}"
        elif self.sw_measure.toggle_on == False:
            self.actualizar_datos_sp(1)
            x_text = f"{self.m1_rad_sp:.4f}"
            y_text = f"{self.m2_rad_sp:.4f}"
            z_text = f"{self.m3_rad_sp:.4f}"
        else:
            self.actualizar_datos_sp(2)
            x_text = f"{self.m1_deg_sp:.2f}"
            y_text = f"{self.m2_deg_sp:.2f}"
            z_text = f"{self.m3_deg_sp:.2f}"
        self.x_coord.setText(x_text)
        self.y_coord.setText(y_text)
        self.z_coord.setText(z_text)
        self.x_new.clear()
        self.y_new.clear()
        self.z_new.clear()
        # Enviar coordenadas a ESP
        esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        sleep(0.01)
        esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        sleep(0.01)
        esp.mover_motor(self.ser, 3, self.m3_rad_sp)

    # FUNCIÓN 09: Actualizar datos SET POINT
    def actualizar_datos_sp(self, x = 3):
        # Valor actualizado de SET POINT en COORD RECTANGULARES
        if x == 0:
            print(f"x: {self.x_sp}")
            print(f"y: {self.y_sp}")
            print(f"z: {self.z_sp}")
            q1, q2, q3, err = eq.DeltaIK(px = self.x_sp, py = self.y_sp, pz = self.z_sp)
            self.m1_rad_sp = q1
            self.m2_rad_sp = q2
            self.m3_rad_sp = q3
            self.m1_deg_sp = np.rad2deg(self.m1_rad_sp)
            self.m2_deg_sp = np.rad2deg(self.m2_rad_sp)
            self.m3_deg_sp = np.rad2deg(self.m3_rad_sp)
            print(f"Error XYZ: {err}")
        # Valor actualizado de SET POINT en MOTORES RAD
        elif x == 1:
            self.m1_rad_sp = self.validate_sp(self.m1_rad_sp)
            self.m2_rad_sp = self.validate_sp(self.m2_rad_sp)
            self.m3_rad_sp = self.validate_sp(self.m3_rad_sp)
            self.m1_deg_sp = np.rad2deg(self.m1_rad_sp)
            self.m2_deg_sp = np.rad2deg(self.m2_rad_sp)
            self.m3_deg_sp = np.rad2deg(self.m3_rad_sp)
            px, py, pz, err = eq.DeltaFK(q1 = self.m1_rad_sp, q2 = self.m2_rad_sp, q3 = self.m3_rad_sp)
            self.x_sp = px
            self.y_sp = py
            self.z_sp = pz
            print(f"Error RAD: {err}")
        # Valor actualizado de SET POINT en MOTORES DEG
        elif x == 2:
            self.m1_rad_sp = np.deg2rad(self.m1_deg_sp)
            self.m2_rad_sp = np.deg2rad(self.m2_deg_sp)
            self.m3_rad_sp = np.deg2rad(self.m3_deg_sp)
            self.m1_rad_sp = self.validate_sp(self.m1_rad_sp)
            self.m2_rad_sp = self.validate_sp(self.m2_rad_sp)
            self.m3_rad_sp = self.validate_sp(self.m3_rad_sp)
            self.m1_deg_sp = np.rad2deg(self.m1_rad_sp)
            self.m2_deg_sp = np.rad2deg(self.m2_rad_sp)
            self.m3_deg_sp = np.rad2deg(self.m3_rad_sp)
            px, py, pz, err = eq.DeltaFK(q1 = self.m1_rad_sp, q2 = self.m2_rad_sp, q3 = self.m3_rad_sp)
            self.x_sp = px
            self.y_sp = py
            self.z_sp = pz
            print(f"Error DEG: {err}")
        # Error: NO definido
        else:
            print("ERROR")

    # FUNCIÓN 10 (Button 03): Desplazamiento NEGATIVO MOTOR 1
    def m1_neg(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m1_rad_sp -= np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.x_coord.setText(f"{self.m1_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m1_deg_sp -= self.inc
            self.actualizar_datos_sp(2)
            self.x_coord.setText(f"{self.m1_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        sleep(0.01)
        # esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        # sleep(0.01)
        # esp.mover_motor(self.ser, 3, self.m3_rad_sp)

    # FUNCIÓN 11 (Button 04): Desplazamiento POSITIVO MOTOR 1
    def m1_pos(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m1_rad_sp += np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.x_coord.setText(f"{self.m1_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m1_deg_sp += self.inc
            self.actualizar_datos_sp(2)
            self.x_coord.setText(f"{self.m1_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        sleep(0.01)
        # esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        # sleep(0.01)
        # esp.mover_motor(self.ser, 3, self.m3_rad_sp)
        
    # FUNCIÓN 12 (Button 05): Desplazamiento NEGATIVO MOTOR 2
    def m2_neg(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m2_rad_sp -= np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.y_coord.setText(f"{self.m2_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m2_deg_sp -= self.inc
            self.actualizar_datos_sp(2)
            self.y_coord.setText(f"{self.m2_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        # esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        # sleep(0.01)
        esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        sleep(0.01)
        # esp.mover_motor(self.ser, 3, self.m3_rad_sp)

    # FUNCIÓN 13 (Button 06): Desplazamiento POSITIVO MOTOR 2
    def m2_pos(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m2_rad_sp += np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.y_coord.setText(f"{self.m2_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m2_deg_sp += self.inc
            self.actualizar_datos_sp(2)
            self.y_coord.setText(f"{self.m2_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        # esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        # sleep(0.01)
        esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        sleep(0.01)
        # esp.mover_motor(self.ser, 3, self.m3_rad_sp)

    # FUNCIÓN 14 (Button 07): Desplazamiento NEGATIVO MOTOR 3
    def m3_neg(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m3_rad_sp -= np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.z_coord.setText(f"{self.m3_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m3_deg_sp -= self.inc
            self.actualizar_datos_sp(2)
            self.z_coord.setText(f"{self.m3_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        # esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        # sleep(0.01)
        # esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        # sleep(0.01)
        esp.mover_motor(self.ser, 3, self.m3_rad_sp)
        sleep(0.01)

    # FUNCIÓN 15 (Button 08): Desplazamiento POSITIVO MOTOR 3
    def m3_pos(self):
        # Valor en radianes
        if self.sw_measure.toggle_on == False:
            self.m3_rad_sp += np.deg2rad(self.inc)
            self.actualizar_datos_sp(1)
            self.z_coord.setText(f"{self.m3_rad_sp:.4f}")
        # Valor en grados
        else:
            self.m3_deg_sp += self.inc
            self.actualizar_datos_sp(2)
            self.z_coord.setText(f"{self.m3_deg_sp:.2f}")
        # Enviar coordenadas a ESP
        # esp.mover_motor(self.ser, 1, self.m1_rad_sp)
        # sleep(0.01)
        # esp.mover_motor(self.ser, 2, self.m2_rad_sp)
        # sleep(0.01)
        esp.mover_motor(self.ser, 3, self.m3_rad_sp)
        sleep(0.01)

    # FUNCIÓN 16 (Button 09): Desplazamiento NEGATIVO COORD X
    def x_neg(self):
        # Valor en coordenadas rectangulares
        self.x_sp -= self.inc
        self.actualizar_datos_sp(0)
        self.x_coord.setText(f"{self.x_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 17 (Button 10): Desplazamiento POSITIVO COORD X
    def x_pos(self):
        # Valor en coordenadas rectangulares
        self.x_sp += self.inc
        self.actualizar_datos_sp(0)
        self.x_coord.setText(f"{self.x_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 18 (Button 11): Desplazamiento NEGATIVO COORD Y
    def y_neg(self):
        # Valor en coordenadas rectangulares
        self.y_sp -= self.inc
        self.actualizar_datos_sp(0)
        self.y_coord.setText(f"{self.y_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 19 (Button 12): Desplazamiento POSITIVO COORD Y
    def y_pos(self):
        # Valor en coordenadas rectangulares
        self.y_sp += self.inc
        self.actualizar_datos_sp(0)
        self.y_coord.setText(f"{self.y_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 20 (Button 13): Desplazamiento NEGATIVO COORD Z
    def z_neg(self):
        # Valor en coordenadas rectangulares
        self.z_sp -= self.inc
        self.actualizar_datos_sp(0)
        self.z_coord.setText(f"{self.z_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 21 (Button 14): Desplazamiento POSITIVO COORD Z
    def z_pos(self):
        # Valor en coordenadas rectangulares
        self.z_sp += self.inc
        self.actualizar_datos_sp(0)
        self.z_coord.setText(f"{self.z_sp:.2f}")
        # Enviar coordenadas a ESP
        esp.mover_brazos(self.ser, self.m1_rad_sp, self.m2_rad_sp, self.m3_rad_sp)

    # FUNCIÓN 22 (Button 16): Salir de control manual
    def stop_cam(self):
        self.timer.stop()
        esp.desactivar_motores(self.ser)
        esp.reset_ESP(self.ser)
        sleep(0.01)
        temp = esp.read_ESP32(self.ser)
        while(temp != ""):
            print(f"S-> {temp}")
            temp = esp.read_ESP32(self.ser)
        esp.stop_serial(self.ser)
        try:
            self.layout_camera.picam2.stop()
            self.layout_camera.picam2.close()
        except:
            print("NO CAMERA")

    # FUNCIÓN 23 (Button 16): Lectura de encoders y demás instrucciones con el Timer
    def read_encoders(self):
        value = []
        try:
            temp = esp.read_ESP32(self.ser)
            #print(temp[0:4])
            while(temp != ""):
                print(f"R-> {temp}")
                if (temp[0:6] == "echo:S" or temp[0:6] == "echo:T"):
                    self.encoders = False
                    # print(f"Flag OFF: {self.encoders}")
                if ((self.encoders == False) and (temp[0:5] == "ready")):
                    self.encoders = True
                    # print(f"Flag ON: {self.encoders}")
                temp = esp.read_ESP32(self.ser)
            #esp.reset(self.ser)
            if self.encoders == True:
                print("ENCODERS")
                val = ""
                temp = esp.leer_encoders(self.ser)
                while(temp != ""):
                    print(f"E-> {temp}")
                    val = temp
                    temp = esp.read_ESP32(self.ser)
                #esp.reset(self.ser)
                print(f"val: {val}")
                x = ""
                for i in val:
                    if (i == " "):
                        value.append(float(x))
                        x = ""
                    else:
                        x += i
                value.append(float(x))
                #print(value)
                self.x_val = value[0]
                self.y_val = value[1]
                self.z_val = value[2]
                self.layout_pp.pnp_val = value[3]
                self.chtool_val = value[4]
                self.layout_inventory.invent_val = value[5]
                self.act_mediciones()
        except Exception as E:
            print("Bad reading !!!")
            print(f"Exception: {E}")

    # FUNCIÓN 24: Actualizar valor de mediciones
    def act_mediciones(self):
        if (self.sw_coord.toggle_on == False):
            px, py, pz, err = eq.DeltaFK(q1 = self.x_val, q2 = self.y_val, q3 = self.z_val)
            self.x_val = px
            self.y_val = py
            self.z_val = pz
            text_x = f"{self.x_val:.2f}"
            text_y = f"{self.y_val:.2f}"
            text_z = f"{self.z_val:.2f}"
            # print(err)
        elif (self.sw_measure.toggle_on == True):
            self.x_val = np.rad2deg(self.x_val)
            self.y_val = np.rad2deg(self.y_val)
            self.z_val = np.rad2deg(self.z_val)
            text_x = f"{self.x_val:.2f}"
            text_y = f"{self.y_val:.2f}"
            text_z = f"{self.z_val:.2f}"
        else:
            text_x = f"{self.x_val:.4f}"
            text_y = f"{self.y_val:.4f}"
            text_z = f"{self.z_val:.4f}"
        self.x_measure.setText(text_x)
        self.y_measure.setText(text_y)
        self.z_measure.setText(text_z)

        self.layout_pp.sw_angle()
        self.layout_polea.edit_sensor.setText(f"{self.chtool_val:.4f}")
        self.layout_inventory.sw_angle()

    # FUNCIÓN 25 (Button 02): Generar ventana para enviar mensaje a ESP
    def send_msg(self):
        msg_dialog = QDialog()
        msg_dialog.setWindowTitle("MENSAJE")
        layout = QHBoxLayout()
        self.message = QLineEdit()
        self.message.setFixedWidth(self.w * 0.3)
        layout.addWidget(self.message)
        self.btn_send = QPushButton("Enviar")
        self.btn_send.clicked.connect(self.get_message)
        layout.addWidget(self.btn_send)
        msg_dialog.setLayout(layout)
        msg_dialog.exec()

    # FUNCIÓN 26 (Button 'Enviar'): Escribir mensaje a ESP
    def get_message(self):
        text = bytes(self.message.text(), 'ascii')
        print(f"MESSAGE to ESP: {text}")
        esp.write_ESP32(self.ser, text)
        self.message.clear()

    # FUNCIÓN 27: Validar valores máximos de SET POINT para ángulos motores
    def validate_sp(self, a):
        if a >= 1.4:
            a = 1.4
        elif a <= -0.9:
            a = -0.9
        return a
