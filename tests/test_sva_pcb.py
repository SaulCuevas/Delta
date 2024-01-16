import sys

sys.path.append("../Delta")

from VisionArtificial import SVA_PCB, interprete_gerber
from Control import Trayectorias
import time
from matplotlib import pyplot as plt

# from tkinter.filedialog import askdirectory, askopenfilename

# path = askdirectory(title='Selecciona la carpeta CAM')
# map_path = askopenfilename(title='Selecciona la imagen a comparar', filetypes=[("Imágenes", ".jpg .png")])

path = "tests/Triple oscilador a LEDs v10"
map_path = "tests/Imagenes/FOTO_20240112_130010.png"

# top_bottom = input('¿Es top layer? (Y/N) ')

# if top_bottom == 'Y' or top_bottom == 'y':
#     _top_bottom = True
# elif top_bottom == 'N' or top_bottom == 'n':
#     _top_bottom = False
# else:
#     print('...')
#     exit()

_top_bottom = True

start_time = time.time()

path_r1 = "tests/Imagenes/test.png"
path_r2 = path_r1
path_r3 = path_r1
path_r4 = path_r1

componentes_lista = interprete_gerber.obtener_pnp(path, _top_bottom)
puntos = SVA_PCB.inicioSVA(path, map_path, _top_bottom, componentes_lista, path_r1, path_r2, path_r3, path_r4)

ts, qds, dqds, d2qds, pds, dpds, d2pds, err = Trayectorias.calc_trayectorias_ps_no_t(func=Trayectorias.bezier_no_t, operaciones=puntos[:,0], Ps=puntos[:,1:4], vel_deseada=puntos[:,4])

if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ts: ", ts.shape, "qds: ", qds.shape, "dqds: ", dqds.shape, "d2qds: ", d2qds.shape, "pds: ", pds.shape, "dpds: ", dpds.shape, "d2pds: ", d2pds.shape)
    Trayectorias.plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds)
