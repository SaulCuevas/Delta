from VisionArtificial.PCB import interprete_gerber
from Control.fun import Trayectorias, DeltaEcuaciones
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory
import time
import numpy as np
import math

# # operaciones 
# movimiento = 1
# soldadura = 2
# valvula = 3
# herramienta = 4

# # herramientas
# camara = 0
# dispensador = 1
# pnp = 2

path = askdirectory(title='Abrir carpeta con archivo de soldadura')

top_bottom = input('¿Es top layer? (Y/N) ')

start_time = time.time()

if top_bottom == 'Y' or top_bottom == 'y':
     _top_bottom = True
elif top_bottom == 'N' or top_bottom == 'n':
     _top_bottom = False
else: print('...'); exit()

soldadura_lista = interprete_gerber.obtener_soldadura(path, _top_bottom)

puntos = Trayectorias.soldaduraclass_to_puntos(soldadura_lista, 500)

ts_, ts, qds_, dqds_, d2qds_, qds, dqds, d2qds, pds, dpds, d2pds, err = Trayectorias.calc_trayectorias_ps_no_t2(func=Trayectorias.bezier_no_t, Ps=puntos[:,0:3], vel_deseada=puntos[:,3])

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
