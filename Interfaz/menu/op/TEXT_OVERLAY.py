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

import sys
import os

from PyQt5.QtCore import Qt, pyqtSignal, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenuBar,
    QStatusBar,
    QMainWindow,
    QApplication
)

class LabelSpecial(QLabel):

    def __init__(self, parent, text, pL, pT):
        super().__init__(parent)
        self.paddingLeft = pL
        self.paddingTop = pT
        self.setText(text)

    def update_position(self):
        if hasattr(self.parent(), 'viewport'):
            parent_rect = self.parent().viewport().rect()
        else:
            parent_rect = self.parent().rect()
        if not parent_rect:
            return

        x = parent_rect.width() - self.width() - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_position()


class IMG_Special(QLabel):
    floatingButtonClicked = pyqtSignal()

    def __init__(self, parent = None, h = 100, img = None, txt = "", x1 = 10, x2 = 10):
        super().__init__(parent)
        self.h = h
        self.txt = txt
        self.x1 = x1
        self.x2 = x2
        # path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # img_delta = os.path.join(path, 'Interfaz-20240115T145144Z-001\Interfaz\imagenes\delta.jpg')
        img_delta = img
        # print(img_delta)
        # Label 01: Imagen Bienvenida
        im = QPixmap(img_delta) # Generar PIXMAP para imagen/video inicio
        im = im.scaled(self.h, self.h, Qt.KeepAspectRatio)  # Escalar imagen al tamaño deseado conforme relación de pantalla
        self.setPixmap(im) # Fijar imagen de pixmap a Label
        self.adjustSize()   # AJustar tamaño label automático
        # self.floating_label = LabelSpecial(parent = self, self.txt, self.x1, self.x2)
        self.lbl = LabelSpecial(self, self.txt, self.x1, self.x2)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lbl.update_position()


class DISK_IMG(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if os.name == 'nt':
            disk = os.path.join(path, 'imagenes\disco.png')
        else:
            disk = os.path.join(path, 'imagenes/disco.png')
        image_special = IMG_Special(self, 500, disk, "1", 100, 100)
        self.layout.addWidget(image_special)

