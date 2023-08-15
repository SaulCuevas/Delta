from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from fun.Trayectorias import *
import time
start_time = time.time()

puntos = np.array([
              (-177.5, 177.5, 170+175), 
              (-177.5, -177.5, 170+175),
              (177.5, -177.5, 170+175),
              (177.5, 177.5, 170+175),
              (-177.5, 177.5, 170+175),
              (177.5, -177.5, 170+175),
            #   (-177.5, 177.5, 520),
            #   (-177.5, -177.5, 520),
            #   (177.5, -177.5, 520),
            #   (177.5, 177.5, 520),
            #   (-177.5, 177.5, 520),
              ], dtype = float)

ts, qds, dqds, d2qds, pds, dpds, d2pds, err = calc_trayectorias_ps(func=bezier, Ps=puntos, vel_deseada=500)
if(err!=0):
    print("error calculando las trayectorias | error tipo: ", err)
else:
    print("--- %s seconds ---" % (time.time() - start_time))

    plt.subplot(3, 3, 1)
    plt.plot(ts[0],pds[0],color='red')
    plt.title('Trayectoria deseada px')
    plt.ylabel('m')
    plt.subplot(3, 3, 2)
    plt.plot(ts[0],dpds[0],color='red')
    plt.title('Velocidad deseada vx')
    plt.ylabel('m/s')
    plt.subplot(3, 3, 3)
    plt.plot(ts[0],d2pds[0],color='red')
    plt.title('Aceleración deseada ax')
    plt.ylabel('m/s^2')

    plt.subplot(3, 3, 4)
    plt.plot(ts[1],pds[1],color='green')
    plt.title('Trayectoria deseada py')
    plt.ylabel('m')
    plt.subplot(3, 3, 5)
    plt.plot(ts[1],dpds[1],color='green')
    plt.title('Velocidad deseada vy')
    plt.ylabel('m/s')
    plt.subplot(3, 3, 6)
    plt.plot(ts[1],d2pds[1],color='green')
    plt.title('Aceleración deseada ay')
    plt.ylabel('m/s^2')

    plt.subplot(3, 3, 7)
    plt.plot(ts[2],pds[2],color='blue')
    plt.title('Trayectoria deseada pz')
    plt.ylabel('m')
    plt.subplot(3, 3, 8)
    plt.plot(ts[2],dpds[2],color='blue')
    plt.title('Velocidad deseada vz')
    plt.ylabel('m/s')
    plt.subplot(3, 3, 9)
    plt.plot(ts[2],d2pds[2],color='blue')
    plt.title('Aceleración deseada az')
    plt.ylabel('m/s^2')

    plt.show()

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

    Ps_FK = np.zeros((1,3))
    for x in np.transpose(qds):
        px, py, pz, err = DeltaFK(q1=x[0],q2=x[1],q3=x[2])
        if(err!=0):
            print("error calculando la cinemática directa | error tipo: ", err)
        else:
            Ps_FK = np.vstack([Ps_FK, [px, py, pz]])
    Ps_FK = np.delete(Ps_FK, 0, 0)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot3D(Ps_FK[:,0], Ps_FK[:,1], Ps_FK[:,2], 'gray')

    ax.set_xlim(-250, 250); ax.set_ylim(-250, 250); ax.set_zlim(167.1977, 522.4509); ax.invert_zaxis()
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.set_title('Trayectoria generada (interp en ps)')
    plt.show()

    pds = pds/1000; dpds = dpds/1000; d2pds = d2pds/1000 # Conversion mm a m

    taus = np.zeros((1,3))
    for i in range(qds.shape[1]):
        tau1, tau2, tau3 = DeltaDinamica(px=pds[0,i], py=pds[1,i], pz=pds[2,i], d2px=d2pds[0,i], d2py=d2pds[1,i], d2pz=d2pds[2,i], theta11=qds[0,i], theta12=qds[1,i], theta13=qds[2,i], d2theta11=d2qds[0,i], d2theta12=d2qds[1,i], d2theta13=d2qds[2,i])
        taus = np.vstack([taus, [tau1, tau2, tau3]])
    taus = np.delete(taus, 0, 0)

    plt.subplot(1, 3, 1)
    plt.plot(ts[0],taus[:,0],color='red')
    plt.title(r'Momento par $\tau_1$')
    plt.ylabel('N-m')
    plt.subplot(1, 3, 2)
    plt.plot(ts[0],taus[:,1],color='green')
    plt.title(r'Momento par $\tau_2$')
    plt.ylabel('N-m')
    plt.subplot(1, 3, 3)
    plt.plot(ts[0],taus[:,2],color='blue')
    plt.title(r'Momento par $\tau_3$')
    plt.ylabel('N-m')
    plt.show()

    print("Máximo esfuerzo en q1 = ", abs(taus[:,0]).max(), "N-m")
    print("Máximo esfuerzo en q2 = ", abs(taus[:,1]).max(), "N-m")
    print("Máximo esfuerzo en q3 = ", abs(taus[:,2]).max(), "N-m")
    print("Máximo esfuerzo = ", abs(taus).max(), "N-m = ", abs(taus).max()*100/9.80665, "kg-cm")

    print("Máxima velocidad angular en q1 = ", abs(dqds[0,:]).max(), "rad/s")
    print("Máxima velocidad angular en q2 = ", abs(dqds[1,:]).max(), "rad/s")
    print("Máxima velocidad angular en q3 = ", abs(dqds[2,:]).max(), "rad/s")
    print("Máxima velocidad angular = ", abs(dqds).max(), "rad/s = ", abs(dqds).max()*60/(2*math.pi), "RPM")
