import sys

sys.path.append("../Delta")

from scipy.io import loadmat
import numpy as np
from Control import Trayectorias
import time

x = loadmat('tests/trayectoria_upiita.mat')
upiita = np.array(x['upiita'])
altura = 400.0

trayectoria = Trayectorias.trayectoria_xy_to_puntos(upiita, altura)

start_time = time.time()

ts, qds, dqds, d2qds, pds, dpds, d2pds, err = Trayectorias.calc_trayectorias_ps_no_t(func=Trayectorias.bezier_no_t, operaciones=trayectoria[:,0], Ps=trayectoria[:,1:4], vel_deseada=trayectoria[:,4])

if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ts: ", ts.shape, "qds: ", qds.shape, "dqds: ", dqds.shape, "d2qds: ", d2qds.shape, "pds: ", pds.shape, "dpds: ", dpds.shape, "d2pds: ", d2pds.shape)
    Trayectorias.plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds)
