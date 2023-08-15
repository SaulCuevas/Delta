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

path = askopenfilename(title='Abrir gerber')

copper = gerber.read(path)
for prim in copper.primitives:
    # print(prim.position, prim.width)
    # if isinstance(prim, gerber.primitives.Region):
    #     print(prim.bounding_box)
    # if isinstance(prim, gerber.primitives.Line):
    #     print(prim)
    pos = (prim.bounding_box[0][0] + (prim.bounding_box[0][1] - prim.bounding_box[0][0]) / 2,
           prim.bounding_box[1][0] + (prim.bounding_box[1][1] - prim.bounding_box[1][0]) / 2)
    area = (prim.bounding_box[0][1] - prim.bounding_box[0][0]) * (prim.bounding_box[1][1] - prim.bounding_box[1][0])
    print(pos, area)
