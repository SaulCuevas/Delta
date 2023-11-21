from VisionArtificial.PCB import interprete_gerber
from Control.fun.Trayectorias import *
import matplotlib.pyplot as plt
import time

from tkinter.filedialog import askdirectory

path = askdirectory(title='Abrir carpeta con archivo de soldadura')

top_bottom = input('¿Es top layer? (Y/N) ')

start_time = time.time()

if top_bottom == 'Y' or top_bottom == 'y':
     _top_bottom = True
elif top_bottom == 'N' or top_bottom == 'n':
     _top_bottom = False
else: print('...'); exit()

soldadura_lista = interprete_gerber.obtener_soldadura(path, _top_bottom)
altura_pcb = 500
puntos = soldaduraclass_to_puntos(soldadura_lista, altura_pcb)

ts, qds, dqds, d2qds, pds, dpds, d2pds, err = calc_trayectorias_ps(func=bezier, Ps=puntos[:,0:3], vel_deseada=puntos[:,3])
if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ts: ", ts.shape, "qds: ", qds.shape, "dqds: ", dqds.shape, "d2qds: ", d2qds.shape, "pds: ", pds.shape, "dpds: ", dpds.shape, "d2pds: ", d2pds.shape)

    plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds)
