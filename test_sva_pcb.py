from VisionArtificial.PCB import interprete_gerber
from Control.fun import Trayectorias
import numpy as np
import cv2
import math
import time
from matplotlib import pyplot as plt

from tkinter.filedialog import askdirectory, askopenfilename

path = askdirectory(title='Selecciona la carpeta CAM')
top_bottom = input('¿Es top layer? (Y/N) ')

if top_bottom == 'Y' or top_bottom == 'y':
    _top_bottom = True
elif top_bottom == 'N' or top_bottom == 'n':
    _top_bottom = False
else:
    print('...')
    exit()

if _top_bottom:
    interprete_gerber.genImage(path, top=True)
else:
    interprete_gerber.genImage(path, top=False)

im1 = cv2.imread('VisionArtificial/PCB/board-top.png')
im2 = cv2.imread('VisionArtificial/PCB/board-bottom.png')

map_path = askopenfilename(title='Selecciona la imagen a comparar', filetypes=[("Imágenes", ".jpg .png")])
# read images
temp_img_gray = cv2.imread('VisionArtificial/PCB/board-mask.png', 0)
map_img = cv2.imread(map_path)
cv2.imwrite('VisionArtificial/PCB/from.jpg', map_img)

# image segmentation
# """
hsv = cv2.cvtColor(map_img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 180])
upper = np.array([255, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

# equalize histograms
temp_img_eq = cv2.equalizeHist(temp_img_gray)
map_img_eq = cv2.equalizeHist(mask)

# calculate matched coordinates
offset, grados_rot = interprete_gerber.get_matched_coordinates(temp_img_eq, map_img_eq)

print(offset)
print(grados_rot)

# convertir de pixeles a mm
pixeles_por_mm = 10.0
offset_x = offset[0]/pixeles_por_mm
offset_y = offset[1]/pixeles_por_mm

soldadura_lista = interprete_gerber.obtener_soldadura(path, _top_bottom)
for x in soldadura_lista:
    nuevo_x = x.x*math.cos(grados_rot) - x.y*math.sin(grados_rot)
    nuevo_y = x.x*math.sin(grados_rot) + x.y*math.cos(grados_rot)
    x.x = nuevo_x + offset_x
    x.y = nuevo_y + offset_y

puntos_soldadura = Trayectorias.soldaduraclass_to_puntos2(soldadura_lista, 500)

componentes_lista = interprete_gerber.obtener_pnp(path, _top_bottom)
for x in componentes_lista:
    nuevo_x = x.x*math.cos(grados_rot) - x.y*math.sin(grados_rot)
    nuevo_y = x.x*math.sin(grados_rot) + x.y*math.cos(grados_rot)
    x.x = nuevo_x + offset_x
    x.y = nuevo_y + offset_y
    x.angulo += grados_rot
    if(x.angulo) < 0.0: x.angulo += 360.0
    if(x.angulo) > 360.0: x.angulo -= 360.0 

puntos_pnp = Trayectorias.componentesclass_to_puntos2(componentes_lista, 400, 420)

start_time = time.time()
ts_, ts, qds_, dqds_, d2qds_, qds, dqds, d2qds, pds, dpds, d2pds, err = Trayectorias.calc_trayectorias_ps_no_t2(func=Trayectorias.bezier_no_t, operaciones=puntos_soldadura[:,0], Ps=puntos_soldadura[:,1:4], vel_deseada=puntos_soldadura[:,4])

if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ts: ", ts.shape, "qds: ", qds.shape, "dqds: ", dqds.shape, "d2qds: ", d2qds.shape, "pds: ", pds.shape, "dpds: ", dpds.shape, "d2pds: ", d2pds.shape)
    Trayectorias.plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds)
    print(ts_.shape, qds_.shape)
    plt.subplot(3,2,1)
    plt.plot(ts_, qds_[0], color='black')
    plt.subplot(3,2,3)
    plt.plot(ts_, qds_[1], color='black')
    plt.subplot(3,2,5)
    plt.plot(ts_, qds_[2], color='black')
    plt.subplot(3,2,2)
    plt.plot(ts[0], qds[0], color='red')
    plt.subplot(3,2,4)
    plt.plot(ts[0], qds[1], color='red')
    plt.subplot(3,2,6)
    plt.plot(ts[0], qds[2], color='red')
    plt.show()