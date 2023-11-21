import numpy as np
from ..fun.DeltaEcuaciones import *
import matplotlib.pyplot as plt
step = 0.010

# operaciones 
movimiento = 1
soldadura = 2
valvula_on = 3
valvula_off = 4
herramienta = 5

# herramientas
camara = 0
dispensador = 1
pnp = 2

home_pos = np.array([0.0, 0.0, 200.0])

# offset herramientas
offset_cam = np.array([0.0, 0.0, 0.0])
offset_dispensador = np.array([0.0, 0.0, 0.0])
offset_pnp = np.array([0.0, 0.0, 0.0])

def getStep():
    return step

def getOffsetCam():
    return offset_cam

def getOffsetDispensador():
    return offset_dispensador

def getOffsetPnP():
    return offset_pnp

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
    if t2 < step:
        t2 = step
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

def bezier_no_t(t2 : float, q1 : float, q2 : float):
    interps = 10
    t1 = 0.0
    if t2 < step*interps:
        t2 = step*interps
    gamma_1 = 126; gamma_2 = 420; gamma_3 = 540; gamma_4 = 315; gamma_5 = 70
    t = np.linspace(start=t1, stop=t2, num=interps)
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
        tiempos[i] = math.sqrt( (Ps[i+1,0]-Ps[i,0])**2 + (Ps[i+1,1]-Ps[i,1])**2 + (Ps[i+1,2]-Ps[i,2])**2 )/(vel_deseada[i]/1.5)
    
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
    
    pds = np.resize(pds, ts.shape)
    dpds = np.resize(dpds, ts.shape)
    d2pds = np.resize(d2pds, ts.shape)
    return ts, qds, dqds, d2qds, pds, dpds, d2pds, err

def calc_trayectorias_ps_no_t(func, operaciones : np.single, Ps : np.single, vel_deseada : np.single):
    with open('test_trayectorias.txt', 'w') as f: # se abre el archivo a mandar por comunicacion serial
        tiempos = np.zeros(Ps.shape[0]-1) # arreglo de tiempos para interpolacion
        for i in range(Ps.shape[0]-1):
            if (operaciones[i] == movimiento) & (operaciones[i+1] == movimiento): # se calcula el tiempo de interpolacion 
                tiempos[i] = math.sqrt( (Ps[i+1,0]-Ps[i,0])**2 + (Ps[i+1,1]-Ps[i,1])**2 + (Ps[i+1,2]-Ps[i,2])**2 )/(vel_deseada[i]/1.5)
            elif (operaciones[i] != movimiento) & (operaciones[i+1] == movimiento) & (i>0): # se calcula el tiempo de interpolacion 
                tiempos[i-1] = math.sqrt( (Ps[i+1,0]-Ps[i-1,0])**2 + (Ps[i+1,1]-Ps[i-1,1])**2 + (Ps[i+1,2]-Ps[i-1,2])**2 )/(vel_deseada[i-1]/1.5) 
            elif operaciones[i] != movimiento: # no se usa en interpolacion
                tiempos[i] = Ps[i,0]  
        t0 = np.zeros(1) # se inicializan los arreglos tipo numpy
        t1 = np.zeros(1)
        t2 = np.zeros(1)
        pd0 = np.array([home_pos[0]]) # el robot va a iniciar en home
        pd1 = np.array([home_pos[1]])
        pd2 = np.array([home_pos[2]])
        dpd0 = np.zeros(1)
        dpd1 = np.zeros(1)
        dpd2 = np.zeros(1)
        d2pd0 = np.zeros(1)
        d2pd1 = np.zeros(1)
        d2pd2 = np.zeros(1)
        index_soldaduras = np.zeros(1) # arreglo con indice en el arreglo de tiempos en donde ocurre una operacion de soldadura
        pulsos_soldaduras = np.zeros(1) # arreglo con las cantidades de soldadura a dispensar
        index_valvula_on = np.zeros(1) # arreglo con indice en el arreglo de tiempos en donde ocurre una operacion de encendido de valvula
        index_valvula_off = np.zeros(1) # arreglo con indice en el arreglo de tiempos en donde ocurre una operacion de apagado de valvula
        index_herramienta = np.zeros(1) # arreglo con indice en el arreglo de tiempos en donde ocurre una operacion de cambio de herramienta
        herramientas = np.zeros(1) # arreglo con las herramientas a cambiar
        cont_sold = 0 # contador para operaciones de soldadura
        cont_valv_on = 0 # contador para operaciones de encendido de valvula
        cont_valv_off = 0 # contador para operaciones de apagado de valvula
        cont_herr = 0 # contador para operaciones de cambio de herramienta
        # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- #
        #               Generacion de trayectorias               #
        for y in range(Ps.shape[0]-1): 
            if operaciones[y] == soldadura:
                index_soldaduras = np.append(index_soldaduras, t0.shape[0]) # guardo el indice tiempo en donde debe ocurrir la operacion
                pulsos_soldaduras = np.append(pulsos_soldaduras, Ps[y][0]) # guardo la cantidad de soldadura que debe dispensar en ese momento
                t0 = np.append(t0,Ps[y][0]*2+0.1+t0[-1]) # le agrego al vector de tiempo el doble de la cantidad de soldadura (tiempo de pulso) y 0.1 (tiempo de asentamiento arbitrario)
                t1 = np.append(t1,Ps[y][0]*2+0.1+t1[-1])
                t2 = np.append(t2,Ps[y][0]*2+0.1+t2[-1])
                pd0 = np.append(pd0,pd0[-1])    # manteniendo la misma posicion
                dpd0 = np.append(dpd0,0.0)       # vel = 0.0
                d2pd0 = np.append(d2pd0,0.0)      # acel = 0.0
                pd1 = np.append(pd1,pd1[-1])    # manteniendo la misma posicion
                dpd1 = np.append(dpd1,0.0)       # vel = 0.0
                d2pd1 = np.append(d2pd1,0.0)      # acel = 0.0
                pd2 = np.append(pd2,pd2[-1])    # manteniendo la misma posicion
                dpd2 = np.append(dpd2,0.0)       # vel = 0.0
                d2pd2 = np.append(d2pd2,0.0)      # acel = 0.0
                

            if operaciones[y] == valvula_on:
                index_valvula_on = np.append(index_valvula_on, t0.shape[0]) # guardo el indice tiempo en donde debe ocurrir la operacion
                t0 = np.append(t0,0.5+t0[-1]) # le agrego al vector de tiempo 500ms
                t1 = np.append(t1,0.5+t1[-1])
                t2 = np.append(t2,0.5+t2[-1])
                pd0 = np.append(pd0,pd0[-1])    # manteniendo la misma posicion
                dpd0 = np.append(dpd0,0.0)       # vel = 0.0
                d2pd0 = np.append(d2pd0,0.0)      # acel = 0.0
                pd1 = np.append(pd1,pd1[-1])    # manteniendo la misma posicion
                dpd1 = np.append(dpd1,0.0)       # vel = 0.0
                d2pd1 = np.append(d2pd1,0.0)      # acel = 0.0
                pd2 = np.append(pd2,pd2[-1])    # manteniendo la misma posicion
                dpd2 = np.append(dpd2,0.0)       # vel = 0.0
                d2pd2 = np.append(d2pd2,0.0)      # acel = 0.0

            if operaciones[y] == valvula_off:
                index_valvula_off = np.append(index_valvula_off, t0.shape[0]) # guardo el indice tiempo en donde debe ocurrir la operacion
                t0 = np.append(t0,0.5+t0[-1]) # le agrego al vector de tiempo 500ms
                t1 = np.append(t1,0.5+t1[-1])
                t2 = np.append(t2,0.5+t2[-1])
                pd0 = np.append(pd0,pd0[-1])    # manteniendo la posicion HOME X
                dpd0 = np.append(dpd0,0.0)       # vel = 0.0
                d2pd0 = np.append(d2pd0,0.0)      # acel = 0.0
                pd1 = np.append(pd1,pd1[-1])    # manteniendo la posicion HOME Y
                dpd1 = np.append(dpd1,0.0)       # vel = 0.0
                d2pd1 = np.append(d2pd1,0.0)      # acel = 0.0
                pd2 = np.append(pd2,pd2[-1])    # manteniendo la posicion HOME Z
                dpd2 = np.append(dpd2,0.0)       # vel = 0.0
                d2pd2 = np.append(d2pd2,0.0)      # acel = 0.0

            if operaciones[y] == herramienta:
                index_herramienta = np.append(index_herramienta, t0.shape[0]) # guardo el indice tiempo en donde debe ocurrir la operacion
                herramientas = np.append(herramientas, Ps[y][0]) # guardo la herramienta a la que debe cambiar en ese momento
                t0 = np.append(t0,10.0+t0[-1]) # le agrego al vector de tiempo 10s
                t1 = np.append(t1,10.0+t1[-1])
                t2 = np.append(t2,10.0+t2[-1])
                pd0 = np.append(pd0,home_pos[0])    # manteniendo la posicion HOME X
                dpd0 = np.append(dpd0,0.0)       # vel = 0.0
                d2pd0 = np.append(d2pd0,0.0)      # acel = 0.0
                pd1 = np.append(pd1,home_pos[1])    # manteniendo la posicion HOME Y
                dpd1 = np.append(dpd1,0.0)       # vel = 0.0
                d2pd1 = np.append(d2pd1,0.0)      # acel = 0.0
                pd2 = np.append(pd2,home_pos[2])    # manteniendo la posicion HOME Z
                dpd2 = np.append(dpd2,0.0)       # vel = 0.0
                d2pd2 = np.append(d2pd2,0.0)      # acel = 0.0
            
            if (operaciones[y] == movimiento) & (operaciones[y+1] == movimiento):
                # Para interpolar entre dos puntos de trayectoria contiguos
                t, pd, dpd, d2pd = func(tiempos[y], Ps[y,0], Ps[y+1,0]) # se calcula la interpolacion entre puntos en X
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:] # dado que la interpolacion pd inicia en t[0] = 0.0, se elimina ese punto para unirlo a la interpolacion anterior
                t0 = np.append(t0,np.add(t,t0[-1])) # se agrega t al vector de tiempos, sumandole el ultimo tiempo
                pd0 = np.append(pd0,pd) # se agrega pd al vector de pds en X
                dpd0 = np.append(dpd0,dpd) # se agrega dpd al vector de dpds en X
                d2pd0 = np.append(d2pd0,d2pd) # se agrega d2pd al vector de d2pds en X

                # Se repite para Y
                t, pd, dpd, d2pd = func(tiempos[y], Ps[y,1], Ps[y+1,1])
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:]
                t1 = np.append(t1,np.add(t,t1[-1]))
                pd1 = np.append(pd1,pd)
                dpd1 = np.append(dpd1,dpd)
                d2pd1 = np.append(d2pd1,d2pd)

                # Se repite para Z
                t, pd, dpd, d2pd = func(tiempos[y], Ps[y,2], Ps[y+1,2])
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:]
                t2 = np.append(t2,np.add(t,t2[-1]))
                pd2 = np.append(pd2,pd)
                dpd2 = np.append(dpd2,dpd)
                d2pd2 = np.append(d2pd2,d2pd)

            elif (operaciones[y] != movimiento) & (operaciones[y+1] == movimiento) & (y>0):
                # Para interpolar entre dos puntos de trayectoria con una operacion intermedia
                t, pd, dpd, d2pd = func(tiempos[y-1], Ps[y-1,0], Ps[y+1,0]) # <- es diferente 
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:]
                t0 = np.append(t0,np.add(t,t0[-1]))
                pd0 = np.append(pd0,pd)
                dpd0 = np.append(dpd0,dpd)
                d2pd0 = np.append(d2pd0,d2pd)

                t, pd, dpd, d2pd = func(tiempos[y-1], Ps[y-1,1], Ps[y+1,1]) #<-
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:]
                t1 = np.append(t1,np.add(t,t1[-1]))
                pd1 = np.append(pd1,pd)
                dpd1 = np.append(dpd1,dpd)
                d2pd1 = np.append(d2pd1,d2pd)

                t, pd, dpd, d2pd = func(tiempos[y-1], Ps[y-1,2], Ps[y+1,2]) #<-
                t = t[1:]; pd = pd[1:]; dpd = dpd[1:]; d2pd = d2pd[1:]
                t2 = np.append(t2,np.add(t,t2[-1]))
                pd2 = np.append(pd2,pd)
                dpd2 = np.append(dpd2,dpd)
                d2pd2 = np.append(d2pd2,d2pd)

        # el punto final de Ps describe el cambio de herramienta a la camara, se pone fuera del ciclo FOR
        index_herramienta = np.append(index_herramienta, t0.shape[0]) # guardo el indice tiempo en donde debe ocurrir la operacion
        herramientas = np.append(herramientas, Ps[-1][0]) # guardo la herramienta a la que debe cambiar en ese momento
        t0 = np.append(t0,10.0+t0[-1]) # le agrego al vector de tiempo 10s
        t1 = np.append(t1,10.0+t1[-1])
        t2 = np.append(t2,10.0+t2[-1])
        pd0 = np.append(pd0,home_pos[0])    # manteniendo la posicion HOME X
        dpd0 = np.append(dpd0,0.0)       # vel = 0.0
        d2pd0 = np.append(d2pd0,0.0)      # acel = 0.0
        pd1 = np.append(pd1,home_pos[1])    # manteniendo la posicion HOME Y
        dpd1 = np.append(dpd1,0.0)       # vel = 0.0
        d2pd1 = np.append(d2pd1,0.0)      # acel = 0.0
        pd2 = np.append(pd2,home_pos[2])    # manteniendo la posicion HOME Z
        dpd2 = np.append(dpd2,0.0)       # vel = 0.0
        d2pd2 = np.append(d2pd2,0.0)      # acel = 0.0

        index_soldaduras = index_soldaduras[1:] # inicializados en un arreglo con cero inicial, se elimina el primer valor
        pulsos_soldaduras = pulsos_soldaduras[1:]
        index_valvula_on = index_valvula_on[1:]
        index_valvula_off = index_valvula_off[1:]
        index_herramienta = index_herramienta[1:]
        herramientas = herramientas[1:]
        
        ts = np.array([t0, t1, t2]) # concatenacion de arreglos [X Y Z] <-> [0 1 2]
        pds = np.array([pd0, pd1, pd2])
        dpds = np.array([dpd0, dpd1, dpd2])
        d2pds = np.array([d2pd0, d2pd1, d2pd2])
        # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- #

        qds = np.zeros(ts.shape) # inicializacion de arreglo vacio para pos de los motores [M1 M2 M3] <-> [0 1 2]
        dqds = np.zeros(ts.shape)
        d2qds = np.zeros(ts.shape)

        # cinematica inversa pds -> qds / [X Y Z] -> [M1 M2 M3]
        for x in range(pds.shape[1]):
            q1, q2, q3, err = DeltaIK(px=pds[0,x], py=pds[1,x], pz=pds[2,x])
            if(err != 0):
                print("error")
                return ts, qds, pds, err
            qds[:,x] = [q1, q2, q3]

        # se obtienen la primera y segunda derivada de qds
        for x in range(ts.shape[0]):
            dqds[x] = np.gradient(qds[x], ts[x])
            d2qds[x] = np.gradient(dqds[x], ts[x])
        
        # Escritura de archivo para comunicacion serial con ESP32
        #     Tiempo Comando Valores
        # Ej: 0.0000 M123 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000
        # Ej: 0.0000 S 0.00000
        for x in range(ts.shape[1]):
            if(x==index_soldaduras[cont_sold]):
                if(cont_sold<len(index_soldaduras)-1): cont_sold += 1
                f.writelines("%.4f" % (ts[0][x-1]+0.1) + ' ' + 'S ' + "%.5f" % pulsos_soldaduras[cont_sold] + '\n')
            elif(x==index_valvula_on[cont_valv_on]):
                if(cont_valv_on<len(index_valvula_on)-1): cont_valv_on += 1
                f.writelines("%.4f" % (ts[0][x-1]+0.1) + ' ' + 'V1\n')
            elif(x==index_valvula_off[cont_valv_off]):
                if(cont_valv_off<len(index_valvula_off)-1):cont_valv_off += 1
                f.writelines("%.4f" % (ts[0][x-1]+0.1) + ' ' + 'V0\n')
            elif(x==index_herramienta[cont_herr]):
                if(cont_herr<len(index_herramienta)-1):cont_herr += 1
                f.writelines("%.4f" % (ts[0][x-1]+0.1) + ' ' + 'T' + "%.0f" % herramientas[cont_herr] + '\n')
            else:
                f.writelines("%.4f" % ts[0][x] + ' ' + 
                             'M123 ' + "%.5f" % qds[0][x] + ' ' + "%.5f" % dqds[0][x] + ' ' + "%.5f" % d2qds[0][x]
                               + ' ' + "%.5f" % qds[1][x] + ' ' + "%.5f" % dqds[1][x] + ' ' + "%.5f" % d2qds[1][x]
                               + ' ' + "%.5f" % qds[2][x] + ' ' + "%.5f" % dqds[2][x] + ' ' + "%.5f" % d2qds[2][x]
                               + '\n')
        f.writelines('%.4f' % (ts[0][-1]) + ' ' + '-') # al final de la operacion se desea que se desactiven todos los motores
    
    return ts, qds, dqds, d2qds, pds, dpds, d2pds, err

def plot_trayectorias_IK(ts, qds, dqds, d2qds, pds, dpds, d2pds):
    plt.subplot(3, 3, 1)
    plt.plot(ts[0],pds[0],color='red')
    plt.title('Trayectoria deseada px')
    plt.ylabel('mm')
    plt.subplot(3, 3, 2)
    plt.plot(ts[0],dpds[0],color='red')
    plt.title('Velocidad deseada vx')
    plt.ylabel('mm/s')
    plt.subplot(3, 3, 3)
    plt.plot(ts[0],d2pds[0],color='red')
    plt.title('Aceleración deseada ax')
    plt.ylabel('mm/s^2')

    plt.subplot(3, 3, 4)
    plt.plot(ts[1],pds[1],color='green')
    plt.title('Trayectoria deseada py')
    plt.ylabel('mm')
    plt.subplot(3, 3, 5)
    plt.plot(ts[1],dpds[1],color='green')
    plt.title('Velocidad deseada vy')
    plt.ylabel('mm/s')
    plt.subplot(3, 3, 6)
    plt.plot(ts[1],d2pds[1],color='green')
    plt.title('Aceleración deseada ay')
    plt.ylabel('m/s^2')

    plt.subplot(3, 3, 7)
    plt.plot(ts[2],pds[2],color='blue')
    plt.title('Trayectoria deseada pz')
    plt.ylabel('mm')
    plt.subplot(3, 3, 8)
    plt.plot(ts[2],dpds[2],color='blue')
    plt.title('Velocidad deseada vz')
    plt.ylabel('mm/s')
    plt.subplot(3, 3, 9)
    plt.plot(ts[2],d2pds[2],color='blue')
    plt.title('Aceleración deseada az')
    plt.ylabel('mm/s^2')

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

def soldaduraclass_to_puntos(soldadura_lista, altura_pcb):
    i = 4
    puntos = np.zeros((len(soldadura_lista)*i+2,5), dtype=float)
    puntos[0,:] = np.array([movimiento, home_pos[0], home_pos[1], home_pos[2], 500])    # HOME
    for x in range(len(soldadura_lista)):
        puntos[x*i+1:x*i+i+1,:] = [np.array([movimiento, soldadura_lista[x].x-offset_dispensador[0], soldadura_lista[x].y-offset_dispensador[1], altura_pcb-5-offset_dispensador[2], 25]), # pos de pcb(x,y) + 5 mm de altura
                            np.array([movimiento, soldadura_lista[x].x-offset_dispensador[0], soldadura_lista[x].y-offset_dispensador[1], altura_pcb-offset_dispensador[2], 25]), # baja a pcb
                            np.array([soldadura, soldadura_lista[x].cantidad, 0, 0, 0]), # enciende el dispensador
                            np.array([movimiento, soldadura_lista[x].x-offset_dispensador[0], soldadura_lista[x].y-offset_dispensador[1], altura_pcb-5-offset_dispensador[2], 500])] # # pos de pcb (x,y) + 5 mm de altura
    puntos[-1,:] = np.array([movimiento, home_pos[0], home_pos[1], home_pos[2], 500])   # HOME
    return puntos

def componentesclass_to_puntos(pnp_lista, altura_pcb, altura_pnp):
    i = 8
    puntos = np.zeros((len(pnp_lista)*i+1,5), dtype=float)
    comp_x = 0
    comp_y = 0
    puntos[0,:] = np.array([movimiento, home_pos[0], home_pos[1], home_pos[2], 500]) # HOME
    for x in range(len(pnp_lista)):
        separacion = 5.0 # Separacion entre componentes
        offset_x = 100.0
        offset_y = 100.0
        puntos[x*i+1:x*i+i+1,:] = [np.array([movimiento, offset_x+comp_x*separacion-offset_pnp[0], offset_y+comp_y*separacion-offset_pnp[1], altura_pcb-5-offset_pnp[2], 25]), # pos de componente(x,y) + 5 mm de altura
                            np.array([valvula_on, 0, 0, 0, 0]), # enciende la valvula
                            np.array([movimiento, offset_x+comp_x*separacion-offset_pnp[0], offset_y+comp_y*separacion-offset_pnp[1], altura_pnp-offset_pnp[2], 25]), # baja a componente(x,y)
                            np.array([movimiento, offset_x+comp_x*separacion-offset_pnp[0], offset_y+comp_y*separacion-offset_pnp[1], altura_pcb-5-offset_pnp[2], 500]), # sube
                            np.array([movimiento, pnp_lista[x].x-offset_pnp[0], pnp_lista[x].y-offset_pnp[1], altura_pcb-5-offset_pnp[2], 25]), # pos de componente en pcb
                            np.array([movimiento, pnp_lista[x].x-offset_pnp[0], pnp_lista[x].y-offset_pnp[1], altura_pcb-offset_pnp[2], 25]), # baja
                            np.array([valvula_off, 0, 0, 0, 0]), # apaga la valvula
                            np.array([movimiento, pnp_lista[x].x-offset_pnp[0], pnp_lista[x].y-offset_pnp[1], altura_pcb-5-offset_pnp[2], 500])] # sube
        comp_x += 1
        if(comp_x == 10):
            comp_x = 0
            comp_y += 1
    puntos[-1,:] = np.array([movimiento, home_pos[0], home_pos[1], home_pos[2], 500])   # HOME
    return puntos

def cambio_herramienta(herr : int):
    puntos_cambio = np.zeros([1,5])
    puntos_cambio[0,:] = np.array([herramienta, herr, 0, 0, 0])
    return puntos_cambio
