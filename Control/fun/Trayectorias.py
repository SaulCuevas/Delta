import numpy as np
from fun.DeltaEcuaciones import *
step = 0.01

def getStep():
    return step

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

def bezier(t2 : float, q1 : float, q2 : float):
    t1 = 0.0
    gamma_1 = 126; gamma_2 = 420; gamma_3 = 540; gamma_4 = 315; gamma_5 = 70
    t = np.arange(0, t2+step, step)
    qd = np.zeros(t.size)
    dqd = np.zeros(t.size)
    d2qd = np.zeros(t.size)

    for i in range(t.size):
        delta = (t[i] - t1) / (t2 - t1)
        mu = delta**5*gamma_1 - delta**6*gamma_2 + delta**7*gamma_3 - delta**8*gamma_4 + delta**9*gamma_5
        dmu = 5*delta**4*gamma_1 - 6*delta**5*gamma_2 + 7*delta**6*gamma_3 - 8*delta**7*gamma_4 + 9*delta**8*gamma_5
        d2mu = 20*delta**3*gamma_1 - 30*delta**4*gamma_2 + 42*delta**5*gamma_3 - 56*delta**6*gamma_4 + 72*delta**7*gamma_5
        if( t[i]<t1 ):
            qd[i] = q1
            dqd[i] = 0
            d2qd[i] = 0
        elif( t[i]>=t1 and t[i]<=t2):
            qd[i] = mu*(q2-q1) + q1
            dqd[i] = dmu*(q2-q1)
            d2qd[i] = d2mu*(q2-q1)
        elif( t[i]>t2 ):
            qd[i] = q2
            dqd[i] = 0
            d2qd[i] = 0
    
    return t, qd, dqd, d2qd

def calc_trayectorias_qs(func, Ps : np.single, vel_deseada):
    tiempos = np.zeros(Ps.shape[0]-1)
    for i in range(Ps.shape[0]-1):
        tiempos[i] = math.sqrt( (Ps[i+1,0]-Ps[i,0])**2 + (Ps[i+1,1]-Ps[i,1])**2 + (Ps[i+1,2]-Ps[i,2])**2 )/vel_deseada
    
    Qs = np.zeros((1,3))
    for x in Ps:
        q1, q2, q3, err = DeltaIK(px=x[0], py=x[1], pz=x[2])
        if(err != 0):
            return ts, qds, dqds, d2qds, Qs, err
        Qs = np.vstack([Qs, [q1, q2, q3]])
    Qs = np.delete(Qs, 0, 0)
    
    Qs_trans = np.transpose(Qs)
    t0 = np.zeros(1)
    t1 = np.zeros(1)
    t2 = np.zeros(1)
    qd0 = np.zeros(1)
    qd1 = np.zeros(1)
    qd2 = np.zeros(1)
    for y in range(Qs_trans.shape[1]-1):
        t, qd, _, _ = trapezoide(tf=tiempos[y], q0=Qs_trans[0,y], qf=Qs_trans[0,y+1])
        t0 = np.append(t0[:-1],np.add(t,t0[-1]))
        qd0 = np.append(qd0[:-1],qd)

        t, qd, _, _ = trapezoide(tf=tiempos[y], q0=Qs_trans[1,y], qf=Qs_trans[1,y+1])
        t1 = np.append(t1[:-1],np.add(t,t1[-1]))
        qd1 = np.append(qd1[:-1],qd)

        t, qd, _, _ = trapezoide(tf=tiempos[y], q0=Qs_trans[2,y], qf=Qs_trans[2,y+1])
        t2 = np.append(t2[:-1],np.add(t,t2[-1]))
        qd2 = np.append(qd2[:-1],qd)
    
    ts = np.array([t0, t1, t2])
    qds = np.array([qd0, qd1, qd2])
    dqds = np.zeros(ts.shape)
    d2qds = np.zeros(ts.shape)

    for x in range(ts.shape[0]):
        dqds[x] = np.gradient(qds[x], ts[x])
        d2qds[x] = np.gradient(dqds[x], ts[x])

    if(np.sum(abs(d2qds[:,-1]))>100):
        ts = np.delete(ts, -1, 1)
        qds = np.delete(qds, -1, 1)
        dqds = np.delete(dqds, -1, 1)
        d2qds = np.delete(d2qds, -1, 1)

    return ts, qds, dqds, d2qds, Qs, err

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
        t, pd, dpd, d2pd = func(tiempos[y], Ps[y,0], Ps[y+1,0])
        t0 = np.append(t0[:-1],np.add(t,t0[-1]))
        t0 = np.round(t0,2)
        pd0 = np.append(pd0[:-1],pd)
        dpd0 = np.append(dpd0[:-1],dpd)
        d2pd0 = np.append(d2pd0[:-1],d2pd)

        t, pd, dpd, d2pd = func(tiempos[y], Ps[y,1], Ps[y+1,1])
        t1 = np.append(t1[:-1],np.add(t,t1[-1]))
        t1 = np.round(t1,2)
        pd1 = np.append(pd1[:-1],pd)
        dpd1 = np.append(dpd1[:-1],dpd)
        d2pd1 = np.append(d2pd1[:-1],d2pd)

        t, pd, dpd, d2pd = func(tiempos[y], Ps[y,2], Ps[y+1,2])
        t2 = np.append(t2[:-1],np.add(t,t2[-1]))
        t2 = np.round(t2,2)
        pd2 = np.append(pd2[:-1],pd)
        dpd2 = np.append(dpd2[:-1],dpd)
        d2pd2 = np.append(d2pd2[:-1],d2pd)
    
    ts = np.array([t0, t1, t2])
    pds = np.array([pd0, pd1, pd2])
    dpds = np.array([dpd0, dpd1, dpd2])
    d2pds = np.array([d2pd0, d2pd1, d2pd2])

    qds = np.zeros((1,3))
    dqds = np.zeros(ts.shape)
    d2qds = np.zeros(ts.shape)

    for x in np.transpose(pds):
        q1, q2, q3, err = DeltaIK(px=x[0], py=x[1], pz=x[2])
        if(err != 0):
            return ts, qds, dqds, d2qds, pds, err
        qds = np.vstack([qds, [q1, q2, q3]])
    qds = np.delete(qds, 0, 0)
    qds = np.transpose(qds)

    for x in range(ts.shape[0]):
        dqds[x] = np.gradient(qds[x], ts[x])
        d2qds[x] = np.gradient(dqds[x], ts[x])

    if(np.sum(abs(d2qds[:,-1]))>100):
        ts = np.delete(ts, -1, 1)
        qds = np.delete(qds, -1, 1)
        dqds = np.delete(dqds, -1, 1)
        d2qds = np.delete(d2qds, -1, 1)

    threshold = 5
    discontinuidades_0 = np.where(abs(np.diff(d2qds[0]))>threshold)[0]
    discontinuidades_1 = np.where(abs(np.diff(d2qds[1]))>threshold)[0]
    discontinuidades_2 = np.where(abs(np.diff(d2qds[2]))>threshold)[0]

    if(discontinuidades_0.size > 0 or discontinuidades_1.size > 0 or discontinuidades_2.size > 0):
        for x in discontinuidades_0:
            qds[0,x] = 0
        for y in discontinuidades_1:
            qds[1,y] = 0
        for z in discontinuidades_2:
            qds[2,z] = 0

        for i in range(100):
            for x in discontinuidades_0:
                slope = ((qds[0,x-1] - qds[0,x-2]) + (qds[0,x+1] - qds[0,x]))/2
                estimated_next_element = qds[0,x-1] + slope
                qds[0,x] = estimated_next_element
            for y in discontinuidades_1:
                slope = ((qds[1,y-1] - qds[1,y-2]) + (qds[1,y+1] - qds[1,y]))/2
                estimated_next_element = qds[1,y-1] + slope
                qds[1,y] = estimated_next_element
            for z in discontinuidades_2:
                slope = ((qds[2,z-1] - qds[2,z-2]) + (qds[2,z+1] - qds[2,z]))/2
                estimated_next_element = qds[2,z-1] + slope
                qds[2,z] = estimated_next_element

        for x in range(ts.shape[0]):
            dqds[x] = np.gradient(qds[x], ts[x])
            d2qds[x] = np.gradient(dqds[x], ts[x])
    
    return ts, qds, dqds, d2qds, pds, dpds, d2pds, err
