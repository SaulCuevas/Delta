from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from fun.Trayectorias import *
import time
start_time = time.time()

puntos = np.array([
              (-177.5, 177.5, 167.2), 
              (-177.5, -177.5, 167.2),
              (177.5, -177.5, 167.2),
              (177.5, 177.5, 167.2),
              (-177.5, 177.5, 167.2),
              (-177.5, 177.5, 522.2),
              (-177.5, -177.5, 522.2),
              (177.5, -177.5, 522.2),
              (177.5, 177.5, 522.2),
              (-177.5, 177.5, 522.2),
              ], dtype = float)

ts, qds, dqds, d2qds, Qs, err = calc_trayectorias_qs(func=trapezoide, Ps=puntos, vel_deseada=500)
if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(np.degrees(Qs))
    # print(qds.shape)

    plt.subplot(3, 3, 1)
    plt.plot(ts[0],qds[0],color='red')
    plt.title('Trayectoria deseada q1')
    plt.ylabel('Radianes')
    plt.subplot(3, 3, 2)
    plt.plot(ts[0],dqds[0],color='red')
    plt.title('Velocidad deseada q1')
    plt.ylabel('Radianes/s')
    plt.subplot(3, 3, 3)
    plt.plot(ts[0],d2qds[0],color='red')
    plt.title('Aceleración deseada q1')
    plt.ylabel('Radianes/s^2')

    plt.subplot(3, 3, 4)
    plt.plot(ts[1],qds[1],color='green')
    plt.title('Trayectoria deseada q2')
    plt.ylabel('Radianes')
    plt.subplot(3, 3, 5)
    plt.plot(ts[1],dqds[1],color='green')
    plt.title('Velocidad deseada q2')
    plt.ylabel('Radianes/s')
    plt.subplot(3, 3, 6)
    plt.plot(ts[1],d2qds[1],color='green')
    plt.title('Aceleración deseada q2')
    plt.ylabel('Radianes/s^2')

    plt.subplot(3, 3, 7)
    plt.plot(ts[2],qds[2],color='blue')
    plt.title('Trayectoria deseada q3')
    plt.ylabel('Radianes')
    plt.subplot(3, 3, 8)
    plt.plot(ts[2],dqds[2],color='blue')
    plt.title('Velocidad deseada q3')
    plt.ylabel('Radianes/s')
    plt.subplot(3, 3, 9)
    plt.plot(ts[2],d2qds[2],color='blue')
    plt.title('Aceleración deseada q3')
    plt.ylabel('Radianes/s^2')

    plt.show()

    Ps = np.zeros((1,3))
    for x in np.transpose(qds):
        px, py, pz, err = DeltaFK(q1=x[0],q2=x[1],q3=x[2])
        if(err!=0):
            print("error calculando la cinemática directa | error tipo: ", err)
            Ps = np.vstack([Ps, [px, py, pz]])
        else:
            Ps = np.vstack([Ps, [px, py, pz]])
    Ps = np.delete(Ps, 0, 0)

    #print(Ps)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot3D(Ps[:,0], Ps[:,1], Ps[:,2], 'gray')

    ax.set_xlim(-250, 250); ax.set_ylim(-250, 250); ax.set_zlim(167.1977, 522.4509); ax.invert_zaxis()
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.set_title('Trayectoria generada (interp en qs)')
    plt.show()
