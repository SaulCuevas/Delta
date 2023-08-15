import math
import numpy as np
from numpy.linalg import inv

def DeltaIK(r=100.0, h=65.0, a=280, b=350, phi1=0, phi2=2*math.pi/3, phi3=-2*math.pi/3, px=0, py=0, pz=100):
    err = 0

    cx1 = math.cos(phi1)*px + math.sin(phi1)*py + h - r
    cy1 = -math.sin(phi1)*px + math.cos(phi1)*py
    cz1 = pz

    cx2 = math.cos(phi2)*px + math.sin(phi2)*py + h - r
    cy2 = -math.sin(phi2)*px + math.cos(phi2)*py
    cz2 = pz

    cx3 = math.cos(phi3)*px + math.sin(phi3)*py + h - r
    cy3 = -math.sin(phi3)*px + math.cos(phi3)*py
    cz3 = pz

    th31 = math.acos(cy1/b)
    th32 = math.acos(cy2/b)
    th33 = math.acos(cy3/b)

    k1 = ( pow(cx1,2) + pow(cy1,2) + pow(cz1,2) - pow(a,2) - pow(b,2) ) / (2*a*b*math.sin(th31))
    k2 = ( pow(cx2,2) + pow(cy2,2) + pow(cz2,2) - pow(a,2) - pow(b,2) ) / (2*a*b*math.sin(th32))
    k3 = ( pow(cx3,2) + pow(cy3,2) + pow(cz3,2) - pow(a,2) - pow(b,2) ) / (2*a*b*math.sin(th33))

    th21 = math.acos(k1)
    th22 = math.acos(k2)
    th23 = math.acos(k3)

    L1 = ( a*cx1 + b*math.sin(th31)*( cz1*math.sin(th21) + cx1*math.cos(th21) ) ) / ( pow(a,2) + 2*a*b*math.sin(th31)*math.cos(th21) + pow(b,2)*pow(math.sin(th31),2) )
    L2 = ( a*cx2 + b*math.sin(th32)*( cz2*math.sin(th22) + cx2*math.cos(th22) ) ) / ( pow(a,2) + 2*a*b*math.sin(th32)*math.cos(th22) + pow(b,2)*pow(math.sin(th32),2) )
    L3 = ( a*cx3 + b*math.sin(th33)*( cz3*math.sin(th23) + cx3*math.cos(th23) ) ) / ( pow(a,2) + 2*a*b*math.sin(th33)*math.cos(th23) + pow(b,2)*pow(math.sin(th33),2) )

    q1 = math.acos(L1)
    q2 = math.acos(L2)
    q3 = math.acos(L3)

    a1x = r + a*math.cos(q1); a1y = 0; a1z = a*math.sin(q1)
    a2x = (r + a*math.cos(q2))*math.cos(phi2); a2y = (r + a*math.cos(q2))*math.sin(phi2); a2z = a*math.sin(q2)
    a3x = (r + a*math.cos(q3))*math.cos(phi3); a3y = (r + a*math.cos(q3))*math.sin(phi3); a3z = a*math.sin(q3)

    b1x = px+h; b1y = py; b1z = pz
    b2x = px+h*math.cos(phi2); b2y = py+h*math.sin(phi2); b2z = pz
    b3x = px+h*math.cos(phi3); b3y = py+h*math.sin(phi3); b3z = pz

    A1_B1 = math.sqrt(pow((a1x-b1x),2) + pow((a1y-b1y),2) + pow((a1z-b1z),2))
    A2_B2 = math.sqrt(pow((a2x-b2x),2) + pow((a2y-b2y),2) + pow((a2z-b2z),2))
    A3_B3 = math.sqrt(pow((a3x-b3x),2) + pow((a3y-b3y),2) + pow((a3z-b3z),2))

    if(A1_B1 > (b+1) or A1_B1 < (b-1)):
        q1 = -q1

    if(A2_B2 > (b+1) or A2_B2 < (b-1)):
        q2 = -q2

    if(A3_B3 > (b+1) or A3_B3 < (b-1)):
        q3 = -q3

    a1x = r + a*math.cos(q1); a1y = 0; a1z = a*math.sin(q1)
    a2x = (r + a*math.cos(q2))*math.cos(phi2); a2y = (r + a*math.cos(q2))*math.sin(phi2); a2z = a*math.sin(q2)
    a3x = (r + a*math.cos(q3))*math.cos(phi3); a3y = (r + a*math.cos(q3))*math.sin(phi3); a3z = a*math.sin(q3)

    A1_B1 = math.sqrt(pow((a1x-b1x),2) + pow((a1y-b1y),2) + pow((a1z-b1z),2))
    A2_B2 = math.sqrt(pow((a2x-b2x),2) + pow((a2y-b2y),2) + pow((a2z-b2z),2))
    A3_B3 = math.sqrt(pow((a3x-b3x),2) + pow((a3y-b3y),2) + pow((a3z-b3z),2))

    if(A1_B1 < b-1 or A1_B1 > b+1 or isinstance(A1_B1,complex)):
        err = 2
    if(A2_B2 < b-1 or A2_B2 > b+1 or isinstance(A2_B2,complex)):
        err = 2
    if(A3_B3 < b-1 or A3_B3 > b+1 or isinstance(A3_B3,complex)):
        err = 2
    
    if(abs(cy1)>b or abs(cy2)>b or abs(cy3)>b):
        #print('A1B1 no intersecta')
        err = 1
    
    return q1, q2, q3, err

def DeltaFK(r=100.0, h=65.0, a=280, b=350, phi1=0, phi2=2*math.pi/3, phi3=-2*math.pi/3, q1=0, q2=0, q3=0):
    err = 0

    # Cuando los tres angulos son exactamente iguales ocurre una singularidad
    if(q1 == q2 and q1 == q3):
        px = 0
        py = 0
        pz = a*math.sin(q1) + math.sqrt( b**2 - (r-h+a*math.cos(q1))**2 )
        return px, py, pz, err
    

    # Cuando dos angulos son exactamente iguales y la suma de un igual con el
    # diferente es pi, se puede generar una singularidad
    if( q1 == q2  and (abs(q1+q3-math.pi)<0.001) ): # q1 = q2, q1+q3 = pi
        q1 = q1 + 0.001
    elif( q1 == q3 and  (abs(q1+q2-math.pi)<0.001) ): # q1 = q3, q1+q2 = pi
        q1 = q1 + 0.001
    elif( q2 == q3 and  (abs(q1+q2-math.pi)<0.001) ): # q2 = q3, q1+q2 = pi
        q2 = q2 + 0.001
    

    # Si un angulo es cero y la suma de los otros es cero, se puede generar una
    # singularidad
    if(q1 == 0 or q2 == 0 or q3 == 0):
        if(q2 != 0 and (abs(q2+q3)<0.001)): # q1 = 0, q2 = q3
            q2 = q2 + 0.001
        elif(q1 != 0 and (abs(q1+q3)<0.001)): # q2 = 0, q1 = q3
            q1 = q1 + 0.001
        elif(q1 != 0 and (abs(q1+q2)<0.001)): # q3 = 0, q1 = q2
            q1 = q1 + 0.001
        
    

    # Cuando la suma de magnitudes de los tres angulos da pi o 2pi/3 puede
    # ocurrir una singularidad
    #if(abs(abs(q1)+abs(q2)+abs(q3)-math.pi)>0.001 or abs(abs(q1)+abs(q2)+abs(q3)-2*math.pi/3)>0.001):
    #    q1 = q1 + 0.001
    

    alpha1 = r-h+a*math.cos(q1); alpha2 = r-h+a*math.cos(q2); alpha3 = r-h+a*math.cos(q3)
    beta1 = a*math.sin(q1); beta2 = a*math.sin(q2); beta3 = a*math.sin(q3)

    e12 = -2*alpha1 + 2*alpha2*math.cos(phi2)
    e22 = 2*alpha2*math.sin(phi2)
    e32 = -2*beta1 + 2*beta2
    e42 = alpha1**2 - alpha2**2 + beta1**2 - beta2**2

    e13 = -2*alpha1 + 2*alpha3*math.cos(phi3)
    e23 = 2*alpha3*math.sin(phi3)
    e33 = -2*beta1 + 2*beta3
    e43 = alpha1**2 - alpha3**2 + beta1**2 - beta3**2

    l0 = e32*e43 - e42*e33
    l1 = e32*e13 - e12*e33
    l2 = e22*e33 - e32*e23
    l3 = e23*e42 - e43*e22
    l4 = e23*e12 - e13*e22

    k0 = 1 + ( l1**2 + l4**2 )/( l2**2 )
    k1 = ( 2*l0*l1 + 2*l3*l4 )/( l2**2 ) - 2*alpha1 - 2*beta1*l4/l2
    k2 = ( l0**2 + l3**2 )/( l2**2 ) - 2*beta1*l3/l2 + alpha1**2 + beta1**2 - b**2

    if((k1**2-4*k0*k2)<0):
        #print('No hay soluciones reales')
        px = 0
        py = 0
        pz = 0
        err = 1
        return px, py, pz, err
    elif((k1**2-4*k0*k2)>0):
        #print('Dos soluciones posibles')
        #px = ( -k1 + math.sqrt(k1**2 - 4*k0*k2) )/( 2*k0 )
        px = ( -k1 - math.sqrt(k1**2 - 4*k0*k2) )/( 2*k0 )
        py = ( l0 + l1*px )/l2
        pz = ( l3 + l4*px )/l2
        if(pz<0):
            px = ( -k1 + math.sqrt(k1**2 - 4*k0*k2) )/( 2*k0 )
            py = ( l0 + l1*px )/l2
            pz = ( l3 + l4*px )/l2
        
    elif((k1**2-4*k0*k2)==0):
        #print('Solo una solucion real')
        #px = ( -k1 + math.sqrt(k1**2 - 4*k0*k2) )/( 2*k0 )
        px = ( -k1 - math.sqrt(k1**2 - 4*k0*k2) )/( 2*k0 )
        py = ( l0 + l1*px )/l2
        pz = ( l3 + l4*px )/l2
    else:
        #print('Si los centros coinciden, hay infinitas soluciones; si no, no hay soluciones')
        px = 0
        py = 0
        pz = a*math.sin(q1) + math.sqrt( b**2 - (r-h+a*math.cos(q1))**2 )
    

    a1x = r + a*math.cos(q1); a1y = 0; a1z = a*math.sin(q1)
    b1x = px+h; b1y = py; b1z = pz
    a2x = (r + a*math.cos(q2))*math.cos(phi2); a2y = (r + a*math.cos(q2))*math.sin(phi2); a2z = a*math.sin(q2)
    b2x = px+h*math.cos(phi2); b2y = py+h*math.sin(phi2); b2z = pz
    a3x = (r + a*math.cos(q3))*math.cos(phi3); a3y = (r + a*math.cos(q3))*math.sin(phi3); a3z = a*math.sin(q3)
    b3x = px+h*math.cos(phi3); b3y = py+h*math.sin(phi3); b3z = pz

    bb1 = math.sqrt((a1x-b1x)**2 + (a1y-b1y)**2 + (a1z-b1z)**2); bb2 = math.sqrt((a2x-b2x)**2 + (a2y-b2y)**2 + (a2z-b2z)**2); bb3 = math.sqrt((a3x-b3x)**2 + (a3y-b3y)**2 + (a3z-b3z)**2)
    if(bb1 < b-1 or bb1 > b+1):
        err = 2
        return px, py, pz, err
    
    if(bb2 < b-1 or bb2 > b+1):
        err = 2
        return px, py, pz, err
    
    if(bb3 < b-1 or bb3 > b+1):
        err = 2
        return px, py, pz, err
    

    if(pz < 0):
        err = 1
        return px, py, pz, err
    
    return px, py, pz, err

def DeltaDinamica(r=0.100, h=0.065, a=0.280, phi1=0, phi2=2*math.pi/3, phi3=-2*math.pi/3, px=0, py=0, pz=100, d2px=0, d2py=0, d2pz=0, theta11=0, theta12=0, theta13=0, d2theta11=0, d2theta12=0, d2theta13=0):
    I_m = 0.057565963175172; # Momento de inercia del rotor
    m_a = 0.229997; # masa a (kg)
    m_b = 0.080931; # masa b (kg) [cada uno]
    m_p = 1.160627; # masa de la plataforma movil (kg)
    g_c = 9.80665; # valor de la gravedad

    f_px = 0 # fuerzas externas ejercidas en la plataforma movil
    f_py = 0
    f_pz = 0

    A = np.array([
        [ 2*( px+h*math.cos(phi1)-r*math.cos(phi1)-a*math.cos(phi1)*math.cos(theta11) ), 2*( px+h*math.cos(phi2)-r*math.cos(phi2)-a*math.cos(phi2)*math.cos(theta12) ), 2*( px+h*math.cos(phi3)-r*math.cos(phi3)-a*math.cos(phi3)*math.cos(theta13) ) ],
        [ 2*( py+h*math.sin(phi1)-r*math.sin(phi1)-a*math.sin(phi1)*math.cos(theta11) ), 2*( py+h*math.sin(phi2)-r*math.sin(phi2)-a*math.sin(phi2)*math.cos(theta12) ), 2*( py+h*math.sin(phi3)-r*math.sin(phi3)-a*math.sin(phi3)*math.cos(theta13) ) ],
        [ 2*( pz-a*math.sin(theta11) ), 2*( pz-a*math.sin(theta12) ), 2*( pz-a*math.sin(theta13) ) ]], dtype = float)

    B = np.array([
        [ (m_p+3*m_b)*d2px-f_px ],
        [ (m_p+3*m_b)*d2py-f_py ],
        [ (m_p+3*m_b)*(d2pz+g_c)-f_pz ]] , dtype = float)

    lambdas = np.matmul(inv(A),B)

    tau_1 = float( (I_m + (1/3)*m_a*a**2 + m_b*a**2)*d2theta11 + ( (1/2)*m_a+m_b )*g_c*a*math.cos(theta11) - 2*a*lambdas[0]*( (px*math.cos(phi1) + py*math.sin(phi1) + h - r)*math.sin(theta11) - pz*math.cos(theta11) ) )
    tau_2 = float( (I_m + (1/3)*m_a*a**2 + m_b*a**2)*d2theta12 + ( (1/2)*m_a+m_b )*g_c*a*math.cos(theta12) - 2*a*lambdas[1]*( (px*math.cos(phi2) + py*math.sin(phi2) + h - r)*math.sin(theta12) - pz*math.cos(theta12) ) )
    tau_3 = float( (I_m + (1/3)*m_a*a**2 + m_b*a**2)*d2theta13 + ( (1/2)*m_a+m_b )*g_c*a*math.cos(theta13) - 2*a*lambdas[2]*( (px*math.cos(phi3) + py*math.sin(phi3) + h - r)*math.sin(theta13) - pz*math.cos(theta13) ) )

    return tau_1, tau_2, tau_3