import math

import gerber
import numpy as np
import cv2
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
import os
from glob import glob

class soldadura_class:
    def __init__(self, x, y, cantidad) -> None:
        self.x = x
        self.y = y
        self.cantidad = cantidad

path = askdirectory(title='Abrir carpeta con archivo de soldadura')

top_bottom = input('¿Es top layer? (Y/N) ')

if top_bottom == 'Y' or top_bottom == 'y':
     path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GTP'), recursive=True)[0])
elif top_bottom == 'N' or top_bottom == 'n':
     path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GBP'), recursive=True)[0])
else: print('...')

soldadura_lista = []

copper = gerber.read(path_solder)
for prim in copper.primitives:
    # print(prim.position, prim.width)
    # if isinstance(prim, gerber.primitives.Region):
    #     print(prim.bounding_box)
    # if isinstance(prim, gerber.primitives.Line):
    #     print(prim)
    pos = (prim.bounding_box[0][0] + (prim.bounding_box[0][1] - prim.bounding_box[0][0]) / 2,
           prim.bounding_box[1][0] + (prim.bounding_box[1][1] - prim.bounding_box[1][0]) / 2)
    area_sqr = math.sqrt(prim.bounding_box[0][1] - prim.bounding_box[0][0]) * (prim.bounding_box[1][1] - prim.bounding_box[1][0])
    soldadura_lista.append(soldadura_class(round(pos[0], 4), round(pos[1], 4), area_sqr))

for x in soldadura_lista:
    print(x.x, x.y, x.cantidad)