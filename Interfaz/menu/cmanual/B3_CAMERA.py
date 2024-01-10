# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:19 2023

TT - Robot Manipulador para la colocación y soldadura de componentes electrónicos de montaje superficial

IPN - UPIITA

Alumnos:
    - Saúl Asís Cuevas Morales
    - Luis Fernando Morales Flores

TOOL: CAMERA
"""


import os
from PyQt5.QtCore import Qt, QSize
# import PyQt5.QtGui as pyGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QLabel,
    QWidget,
    QSpinBox,
    QPushButton,
    QMessageBox,
    QDialog)
import qtawesome as qta

if os.name != 'nt':
    from picamera2 import Picamera2
    from picamera2.previews.qt import QGlPicamera2
from datetime import datetime

import ESP32_serial as esp

import chess

# Dirección de imagen
#path = os.getcwd()
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.name == 'nt':
    img_tool = os.path.join(path, 'imagenes\\tool_pp.png')
else:
    img_tool = os.path.join(path, 'imagenes/tool_pp.png')

class TOOL_C(QHBoxLayout):
    # Constructor
    def __init__(self, ser, base, altura):
        super().__init__()
        # Variables externas
        self.ser = ser
        self.w = base
        self.h = altura
        # Inicialización de variables auxiliares
        self.font_size1 = int(self.h/10) # Valor de fuente 1 ajustado a tamaño pantalla
        self.font_size2 = int(self.h/15) # Valor de fuente 2 ajustado a tamaño pantalla
        self.font_size3 = int(self.h/22) # Valor de fuente 3 ajustado a tamaño pantalla
        self.icon_size = int(self.h/10) # Valor de icon size (button) ajustado a tamaño pantalla
        self.sw_size = int(self.h/5) # Valor de sw (button) ajustado a tamaño pantalla
        # Configuración Inicial de LAYOUT
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Número de fotos
        self.num = 0
        self.fotos = [img_tool]
        self.index = 0

        # Herramienta seleccionada
        self.tool = 0
        esp.cambio_herramienta(self.ser, self.tool)
        # T : Seleccion de herramienta
        # 0 - mover motor M5 a pos de Camara
        # 1 - mover motor M5 a pos de Dispensador
        # 2 - mover motor M5 a pos de Manipulador PnP
        
        image_layout = QVBoxLayout()
        image_widget = QWidget()
        image_widget.setLayout(image_layout)
        action_layout = QVBoxLayout()
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        
    # ---- STYLES --------------------------
    
        # Style Title Label
        st_lbl = "QLabel {"
        st_lbl += "background-color: white; "
        st_lbl += "border: 1px solid; "
        st_lbl += "font-family: Georgia; "
        st_lbl += f"font-size: {self.font_size1}pt; "
        st_lbl += "padding: 0px "
        st_lbl += "}"

        # Style Normal Label
        st_normal = "QLabel {"
        st_normal += "border: 0px solid; "
        st_normal += "font-weight: bold; "
        st_normal += "font-family: Georgia; "
        st_normal += f"font-size: {self.font_size2}pt; "
        st_normal += "padding: 3px "
        st_normal += "}"

        # Style SpinBox
        st_spb = "QSpinBox {"
        st_spb += "border: 1px solid; "
        st_spb += "font-family: Georgia; "
        st_spb += f"font-size: {self.font_size2}pt; "
        st_spb += "padding: 3px "
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
        st_le += f"font-size: {self.font_size1}pt; "
        st_le += "padding: 0px "
        st_le += "}"

        # Style Button
        st_btn = "QPushButton { "
        st_btn += "background-color: lightblue; "
        st_btn += "border-style: outset; "
        st_btn += "border-width: 2px; "
        st_btn += "border-radius: 5px; "
        st_btn += f"font-size: {self.font_size3}pt; "
        st_btn += "border-color: blue; "
        st_btn += "padding: 3px }"
        
        st_btn += "QPushButton:hover { "
        st_btn += "background-color: rgb(0, 224, 224); "
        st_btn += "border-style: inset } "
        
        st_btn += "QPushButton:pressed { "
        st_btn += "background-color: rgb(0, 0, 224); "
        st_btn += "border-style: inset } "

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
        st_calib += "padding: 3px }"
        
        st_calib += "QPushButton:hover { "
        st_calib += "background-color: rgb(10, 150, 150); "
        st_calib += "border-color: rgb(30, 255, 255); "
        st_calib += "border-style: groove } "
        
        st_calib += "QPushButton:pressed { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset } "
        
        st_calib += "QPushButton:checked { "
        st_calib += "background-color: rgb(100, 30, 150); "
        st_calib += "border-color: rgb(150, 0, 255); "
        st_calib += "border-style: inset } "
        
        st_calib += "QPushButton:disabled { "
        st_calib += "background-color: rgb(150, 150, 150); "
        st_calib += "border-style: dashed; "
        st_calib += "border-color: default; "
        st_calib += "border-width: 3px; "
        st_calib += "border-radius: 0px } "

    # ---- LAYOUT PRINCIPAL ----------------

        # Widget Camera
        window = QWidget()
        self.cam_layout = QStackedLayout()
        window.setLayout(self.cam_layout)
        window.setStyleSheet("border: 0px solid;")
        image_layout.addWidget(window, alignment = Qt.AlignCenter)

        # Label 01: FOTOS
        im = QPixmap(img_tool)
        h = self.h * 0.8
        im = im.scaled(h, h, Qt.KeepAspectRatio)
        self.lbl = QLabel()
        self.lbl.setPixmap(im)
        self.cam_layout.addWidget(self.lbl)

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
        except:
            dlg_port = QMessageBox()
            dlg_port.setWindowTitle("CAM Error!")
            dlg_port.setText("Fallo al establecer conexión")
            dlg_port.exec()

        # Button 01: Activar Camara
        self.btn_camera = QPushButton("FOTOS")
        self.btn_camera.setStyleSheet(st_btn)
        w = self.btn_camera.sizeHint().width() * 1.15
        h = self.btn_camera.sizeHint().height()
        self.btn_camera.setFixedSize(w, h)
        self.btn_camera.setCheckable(True)
        self.btn_camera.clicked.connect(self.show_fotos)
        image_layout.addWidget(self.btn_camera, alignment = Qt.AlignCenter)

        # Label 02: TEXTO CONTROL
        self.lbl_control = QLabel("OFF")
        self.lbl_control.setStyleSheet(st_lbl)
        self.lbl_control.adjustSize()
        action_layout.addWidget(self.lbl_control, alignment = Qt.AlignCenter)

        # Button 01: Activar Camara
        icon = qta.icon("mdi.camera-outline")
        self.btn_camera = QPushButton(icon, "")
        self.btn_camera.setStyleSheet(st_btn)
        self.btn_camera.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_camera.sizeHint().width() * 1.05
        h = self.btn_camera.sizeHint().height() * 1.05
        self.btn_camera.setFixedSize(w, h)
        self.btn_camera.setCheckable(True)
        self.btn_camera.clicked.connect(self.sel_active)
        action_layout.addWidget(self.btn_camera, alignment = Qt.AlignCenter)
        
        # Button 02: Captura de Imagen
        icon = qta.icon("mdi.camera-iris")
        self.btn_capture = QPushButton(icon, "")
        self.btn_capture.setStyleSheet(st_btn)
        self.btn_capture.setIconSize(QSize(self.sw_size, self.sw_size))
        w = self.btn_capture.sizeHint().width() * 1.05
        h = self.btn_capture.sizeHint().height() * 1.05
        self.btn_capture.setFixedSize(w, h)
        self.btn_capture.setDisabled(True)
        self.btn_capture.clicked.connect(self.sel_capture)
        action_layout.addWidget(self.btn_capture, alignment = Qt.AlignCenter)

# ----- CALIBRAR IMAGEN -------------------------

        # Label: Captura de imágenes
        self.lbl_capture = QLabel("Calibración")
        self.lbl_capture.setStyleSheet(st_normal)
        action_layout.addWidget(self.lbl_capture)
        self.lbl_capture.hide()

        # SpinBox 01: Número de capturas
        self.spb_capture = QSpinBox()
        self.spb_capture.setMinimum(0)
        self.spb_capture.setMaximum(100)
        self.spb_capture.setSingleStep(1)
        self.spb_capture.setStyleSheet(st_spb)
        w = self.spb_capture.sizeHint().width() * 1.10
        h = int(0.4 * w)
        self.spb_capture.setFixedSize(w, h)
        self.spb_capture.setValue(50)
        self.spb_capture.hide()
        self.spb_capture.valueChanged.connect(self.spb_capture_changed)
        action_layout.addWidget(self.spb_capture, alignment = Qt.AlignCenter)
             

        # Button 03: Calibrar cámara
        self.btn_calibrar = QPushButton("Calibrar")
        self.btn_calibrar.setStyleSheet(st_calib)
        self.btn_calibrar.clicked.connect(self.sel_calibrar)
        w = self.btn_calibrar.sizeHint().width() * 1.5
        h = self.btn_calibrar.sizeHint().height() * 1.5
        self.btn_calibrar.setFixedSize(w, h)
        self.btn_calibrar.setDisabled(True)
        action_layout.addWidget(self.btn_calibrar, alignment = Qt.AlignCenter)

        # Button 03: Captura
        self.btn_foto = QPushButton("Captura")
        self.btn_foto.setStyleSheet(st_btn)
        self.btn_foto.clicked.connect(self.calibrate_capture)
        w = self.btn_foto.sizeHint().width() * 1.05
        h = self.btn_foto.sizeHint().height() * 1.05
        self.btn_foto.setFixedSize(w, h)
        self.btn_foto.hide()
        action_layout.addWidget(self.btn_foto, alignment = Qt.AlignCenter)

        # Button 03: Listo
        self.btn_listo = QPushButton("LISTO")
        self.btn_listo.setStyleSheet(st_btn)
        self.btn_listo.clicked.connect(self.listo)
        w = self.btn_listo.sizeHint().width() * 1.05
        h = self.btn_listo.sizeHint().height() * 1.05
        self.btn_listo.setFixedSize(w, h)
        self.btn_listo.hide()
        action_layout.addWidget(self.btn_listo, alignment = Qt.AlignCenter)

        # Button 03: Volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet(st_calib)
        self.btn_volver.clicked.connect(self.volver)
        w = self.btn_volver.sizeHint().width() * 1.05
        h = self.btn_volver.sizeHint().height() * 1.05
        self.btn_volver.setFixedSize(w, h)
        self.btn_volver.hide()
        action_layout.addWidget(self.btn_volver, alignment = Qt.AlignCenter)

        self.addStretch()
        self.addWidget(image_widget, alignment = Qt.AlignCenter)
        self.addStretch()
        self.addWidget(action_widget, alignment = Qt.AlignCenter)
        self.addStretch()

        
        
    def sel_active(self):
        if self.btn_camera.isChecked():
            self.lbl_control.setText("ON")
            self.btn_capture.setDisabled(False)
            self.btn_calibrar.setDisabled(False)
            self.picam2.start()
            self.cam_layout.setCurrentIndex(1)
        else:
            self.lbl_control.setText("OFF")
            self.btn_capture.setDisabled(True)
            self.btn_calibrar.setDisabled(True)
            self.picam2.stop()
            self.cam_layout.setCurrentIndex(0)

    def sel_capture(self):
        print("BEGIN")
        self.picam2.capture_request(signal_function = self.qpicamera2.signal_done)
        print("DONE")


    def capture_done(self, job):
        if self.lbl_control.isHidden() == False:
            request = self.picam2.wait(job)
            fecha = datetime.now()
            fecha = fecha.strftime("%Y%m%d_%H%M%S")
            text= "FOTO_" + fecha + ".png"
            request.save("main", text)
            request.release()
            # print(os.getcwd())
            # img_foto = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FOTO.png")
            img_foto = os.path.join(os.getcwd(), text)
            new = chess.generate_undistort(img_foto, 1)
            self.fotos.append(new)
            print(self.fotos)
            foto = QPixmap(new)
            #print(foto.size())
            self.lbl.setPixmap(foto)
            h = self.lbl.size().width()
            #print(h)
            foto = foto.scaled(h, h, Qt.KeepAspectRatio)
            #print(foto.size())
            self.lbl.setPixmap(foto)
        else:
            request = self.picam2.wait(job)
            name = "FOTO" + str(self.num) + ".png"
            request.save("main", name)
            request.release()
            original = os.path.join(os.getcwd(), name)
            ubi = "temp/calibrar/" + name
            nuevo = os.path.join(os.getcwd(), ubi)
            os.rename(original, nuevo)


    def sel_calibrar(self):
        self.lbl.hide()
        self.lbl_control.hide()
        self.lbl_capture.show()
        self.btn_camera.hide()
        self.btn_capture.hide()
        self.btn_calibrar.hide()
        self.spb_capture.show()
        self.btn_listo.show()

    # Función para cambio valor SpinBox
    def spb_capture_changed(self, val):
        self.val = val

    def listo(self):
        self.spb_capture.hide()
        self.btn_foto.show()
        self.btn_listo.hide()
        self.btn_volver.show()

    def volver(self):
        self.num = 0
        self.lbl.show()
        self.lbl_control.show()
        self.lbl_capture.hide()
        self.btn_camera.show()
        self.btn_capture.show()
        self.btn_calibrar.show()
        self.spb_capture.hide()
        self.btn_foto.hide()
        self.btn_volver.hide()

    def calibrate_capture(self):
        print("BEGIN")
        if self.num == self.val:
            self.calibrate_camera()
            self.volver()
            print("END")
        else:
            self.lbl_capture.setText(str(self.num))
            self.num += 1
            self.picam2.capture_request(signal_function = self.qpicamera2.signal_done)
            print("DONE")
            
    def calibrate_camera(self):
        print("Calibrate")
        images, objpoints, imgpoints = chess.find_obj()
        cameraMatrix, dist, rvecs, tvecs = chess.calibration(objpoints, imgpoints)
        ubi = chess.undistort(images, cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints)
        if ubi == None:
            ubi = "/home/deltaassysbot/Desktop/Delta-SVA/temp/calibrar/undist2/u2_20.png"
            #ubi = "/home/deltaassysbot/Desktop/Delta-SVA/temp/undistorted.png"
        pix = chess.pixel_mm(ubi, 21)                                                                                                       

        message = "Calibración Completa"
        detail = "Images: " + str(len(images)) + "\n"
        detail += "Objpoints: " + str(objpoints) + "\n"
        detail += "Imgpoints: " + str(imgpoints) + "\n"
        detail += "cameraMatrix: " + str(cameraMatrix) + "\n"
        detail += "dist: " + str(dist) + "\n"
        detail += "rvecs: " + str(rvecs) + "\n"
        detail += "tvecs: " + str(tvecs) + "\n"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setDetailedText(detail)
        msg.setWindowTitle("CAMERA DATA")
        msg.setWindowIcon(qta.icon("ei.eye-open")) 
        style = "#qt_msgbox_label{min-width: 300px;}"
        msg.setStyleSheet(style)

        msg.exec()


    def show_fotos(self):
        msg_dialog = QDialog()
        msg_dialog.setWindowTitle("FOTOS")
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_widget = QWidget()
        h_widget.setLayout(h_layout)

        # Style
        style = "QPushButton:enabled { "
        style += "background-color: rgb(40, 150, 40); "
        style += "border-style: outset; "
        style += "border-width: 2px; "
        style += "border-radius: 5px; "
        style += "border-color: green; "
        style += "padding: 3px }"
        
        style += "QPushButton:hover { "
        style += "background-color: rgb(220, 220, 0); "
        style += "border-style: inset } "
        
        style += "QPushButton:pressed { "
        style += "background-color: rgb(0, 80, 220); "
        style += "border-style: inset } "

        # Button 01: Desplazar en sentido antihorario
        icon = qta.icon("mdi.arrow-left-bold-box-outline")
        self.btn_left = QPushButton(icon, "")
        self.btn_left.setStyleSheet(style)
        self.btn_left.setIconSize(QSize(self.icon_size, self.icon_size))
        w = self.btn_left.sizeHint().width() * 1.05
        h = self.btn_left.sizeHint().height() * 1.05
        self.btn_left.setFixedSize(w, h)
        self.btn_left.clicked.connect(self.left_photo)
        h_layout.addStretch(1)
        h_layout.addWidget(self.btn_left, alignment = Qt.AlignCenter)
        h_layout.addStretch(2)
        
        # Button 02: Desplazar en sentido horario
        icon = qta.icon("mdi.arrow-right-bold-box-outline")
        self.btn_right = QPushButton(icon, "")
        self.btn_right.setStyleSheet(style)
        self.btn_right.setIconSize(QSize(self.icon_size, self.icon_size))
        w = self.btn_right.sizeHint().width() * 1.05
        h = self.btn_right.sizeHint().height() * 1.05
        self.btn_right.setFixedSize(w, h)
        self.btn_right.clicked.connect(self.right_photo)
        h_layout.addWidget(self.btn_right, alignment = Qt.AlignCenter)
        h_layout.addStretch(1)

        # LABEL: DATA
        self.index = self.fotos.index(self.fotos[-1])
        self.data = QLabel()
        self.data.setAlignment(Qt.AlignCenter)
        self.data.adjustSize()
        text = f"DATA: {self.index + 1} de {len(self.fotos)}"
        self.data.setText(text)

        # LABEL: PHOTO
        if self.index == 0:
            self.btn_left.setDisabled(True)
            self.btn_right.setDisabled(True)
        elif self.index != 0 and self.index == len(self.fotos) - 1:
            self.btn_left.setDisabled(False)
            self.btn_right.setDisabled(True)
        else:
            self.btn_left.setDisabled(False)
            self.btn_right.setDisabled(False)
        im = QPixmap(self.fotos[-1])
        w = self.w
        h = self.h * 1.2
        im = im.scaled(w, h, Qt.KeepAspectRatio)
        self.photo = QLabel()
        self.photo.setPixmap(im)

        v_layout.addWidget(self.data, alignment = Qt.AlignCenter)
        v_layout.addWidget(self.photo, alignment = Qt.AlignCenter)
        v_layout.addWidget(h_widget, alignment = Qt.AlignCenter)

        msg_dialog.setLayout(v_layout)
        w = self.photo.sizeHint().width() * 1.10
        h = self.photo.sizeHint().height() + self.data.sizeHint().height() + self.btn_left.sizeHint().height()
        msg_dialog.setFixedSize(w, h * 1.1)
        h_widget.setFixedWidth(w - 20)
        msg_dialog.exec()

    def left_photo(self):
        self.index -= 1
        if self.index == 0:
            self.btn_left.setDisabled(True)
            self.btn_right.setDisabled(False)
        else:
            self.btn_left.setDisabled(False)
            self.btn_right.setDisabled(False)
        text = f"DATA: {self.index + 1} de {len(self.fotos)}"
        self.data.setText(text)
        im = QPixmap(self.fotos[self.index])
        w = self. w
        h = self.h * 1.2
        im = im.scaled(w, h, Qt.KeepAspectRatio)
        self.photo.setPixmap(im)

    def right_photo(self):
        self.index += 1
        if self.index == len(self.fotos) - 1:
            self.btn_right.setDisabled(True)
            self.btn_left.setDisabled(False)
        else:
            self.btn_right.setDisabled(False)
            self.btn_left.setDisabled(False)
        text = f"DATA: {self.index + 1} de {len(self.fotos)}"
        self.data.setText(text)
        im = QPixmap(self.fotos[self.index])
        w = self.w
        h = self.h * 1.2
        im = im.scaled(w, h, Qt.KeepAspectRatio)
        self.photo.setPixmap(im)




    
        
        

        