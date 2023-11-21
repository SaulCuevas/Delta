from VisionArtificial.PCB import SVA_PCB
from Control.fun import Trayectorias
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

map_path = askopenfilename(title='Selecciona la imagen a comparar', filetypes=[("Imágenes", ".jpg .png")])

start_time = time.time()

puntos = SVA_PCB.inicioSVA(path, map_path, _top_bottom)

ts, qds, dqds, d2qds, pds, dpds, d2pds, err = Trayectorias.calc_trayectorias_ps_no_t(func=Trayectorias.bezier_no_t, operaciones=puntos[:,0], Ps=puntos[:,1:4], vel_deseada=puntos[:,4])

if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ts: ", ts.shape, "qds: ", qds.shape, "dqds: ", dqds.shape, "d2qds: ", d2qds.shape, "pds: ", pds.shape, "dpds: ", dpds.shape, "d2pds: ", d2pds.shape)
    Trayectorias.plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds)
