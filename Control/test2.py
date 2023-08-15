import numpy as np
import matplotlib.pyplot as plt
from fun.DeltaEcuaciones import *
step = 0.05
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

def trapezoide(tf : float, q0 : float, qf : float):
    t = np.arange(0, tf+step, step)
    qd = np.zeros(t.size)
    dqd = np.zeros(t.size)
    d2qd = np.zeros(t.size)
    
    v=1.5*(qf-q0)/tf

    if(v==0):
        qd = np.full(t.size, q0)
        return t, qd, dqd, d2qd

    a0=q0
    a1=0
    tb=(q0-qf+v*tf)/v
    a2=v/(2*tb)
    b0=(q0+qf-v*tf)/2
    b1=v
    c2=-a2
    c1=v*tf/tb
    c0=qf-0.5*v*(pow(tf,2))/tb

    for i in range(t.size):
        if(t[i]>=0 and t[i]<tb):
            qd[i] = a0 + a1*t[i] + a2*pow(t[i],2)
            dqd[i] = a1 + 2*a2*t[i]
            d2qd[i] = 2*a2
        elif(t[i]>=tb and t[i]<=(tf-tb)):
            qd[i] = b0 + b1*t[i]
            dqd[i] = b1
            d2qd[i] = 0
        elif(t[i]>(tf-tb) and t[i]<=tf):
            qd[i] = c0 + c1*t[i] + c2*pow(t[i],2)
            dqd[i] = c1 + 2*c2*t[i]
            d2qd[i] = 2*c2
        else:
            qd[i] = qf
            dqd[i] = dqd[i-1]
            d2qd[i] = d2qd[i-1]

    return t, qd, dqd, d2qd

def calc_trayectorias_ps(func, Ps : np.single, vel_deseada):
    tiempos = np.zeros(Ps.shape[0]-1)
    for i in range(Ps.shape[0]-1):
        tiempos[i] = math.sqrt( (Ps[i+1,0]-Ps[i,0])**2 + (Ps[i+1,1]-Ps[i,1])**2 + (Ps[i+1,2]-Ps[i,2])**2 )/(vel_deseada/1.5)
    
    t0 = np.zeros(1)
    t1 = np.zeros(1)
    t2 = np.zeros(1)
    pd0 = np.zeros(1)
    pd1 = np.zeros(1)
    pd2 = np.zeros(1)
    dpd0 = np.zeros(1)
    dpd1 = np.zeros(1)
    dpd2 = np.zeros(1)
    d2pd0 = np.zeros(1)
    d2pd1 = np.zeros(1)
    d2pd2 = np.zeros(1)

    for y in range(Ps.shape[0]-1):
        t, pd, dpd, d2pd = trapezoide(tf=tiempos[y], q0=Ps[y,0], qf=Ps[y+1,0])
        t0 = np.append(t0[:-1],np.add(t,t0[-1]))
        t0 = np.round(t0,2)
        pd0 = np.append(pd0[:-1],pd)
        dpd0 = np.append(dpd0[:-1],dpd)
        d2pd0 = np.append(d2pd0[:-1],d2pd)

        t, pd, dpd, d2pd = trapezoide(tf=tiempos[y], q0=Ps[y,1], qf=Ps[y+1,1])
        t1 = np.append(t1[:-1],np.add(t,t1[-1]))
        t1 = np.round(t1,2)
        pd1 = np.append(pd1[:-1],pd)
        dpd1 = np.append(dpd1[:-1],dpd)
        d2pd1 = np.append(d2pd1[:-1],d2pd)

        t, pd, dpd, d2pd = trapezoide(tf=tiempos[y], q0=Ps[y,2], qf=Ps[y+1,2])
        t2 = np.append(t2[:-1],np.add(t,t2[-1]))
        t2 = np.round(t2,2)
        pd2 = np.append(pd2[:-1],pd)
        dpd2 = np.append(dpd2[:-1],dpd)
        d2pd2 = np.append(d2pd2[:-1],d2pd)

    ts = np.array([t0, t1, t2])
    pds = np.array([pd0, pd1, pd2])
    dpds = np.array([dpd0, dpd1, dpd2])
    d2pds = np.array([d2pd0, d2pd1, d2pd2])
    return ts, pds, dpds, d2pds

ts, pds, dpds, d2pds = calc_trayectorias_ps(func=trapezoide, Ps=puntos, vel_deseada=100)
plt.subplot(1,3,1)
plt.plot(ts[0],pds[0])
plt.subplot(1,3,2)
plt.plot(ts[1],pds[1])
plt.subplot(1,3,3)
plt.plot(ts[2],pds[2])
plt.show()
print(pds[0,-1])
print(pds)