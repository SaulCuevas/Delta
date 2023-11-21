%% Cálculo de la cinemática del robot delta
clear
clc
r = 80; % Longitud en mm
h = 25; 
a = 110;
b = 225.5;

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

% Cinemática directa

q1Deg = 60; q2Deg =	42; q3Deg =	78;

q1 = deg2rad(q1Deg); q2 = deg2rad(q2Deg); q3 = deg2rad(q3Deg);
err = 0;

% Cuando los tres angulos son exactamente iguales ocurre una singularidad
if(q1 == q2 && q1 == q3)
    px = 0;
    py = 0;
    pz = a*sin(q1) + sqrt( b^2 - (r-h+a*cos(q1))^2 );
    return
end

% Cuando dos angulos son exactamente iguales y la suma de un igual con el
% diferente es pi, se puede generar una singularidad
if( q1 == q2  && (abs(q1+q3-pi)<0.001) ) % q1 = q2, q1+q3 = pi
    q1 = q1 + 0.001;
elseif( q1 == q3 &&  (abs(q1+q2-pi)<0.001) ) % q1 = q3, q1+q2 = pi
    q1 = q1 + 0.001;
elseif( q2 == q3 &&  (abs(q1+q2-pi)<0.001) ) % q2 = q3, q1+q2 = pi
    q2 = q2 + 0.001;
end

% Si un angulo es cero y la suma de los otros es cero, se puede generar una
% singularidad
if(q1 == 0 || q2 == 0 || q3 ==0)
    if(q2 ~= 0 && (abs(q2+q3)<0.001)) % q1 = 0, q2 = q3
        q2 = q2 + 0.001;
    elseif(q1 ~= 0 && (abs(q1+q3)<0.001)) % q2 = 0, q1 = q3
        q1 = q1 + 0.001;
    elseif(q1 ~= 0 && (abs(q1+q2)<0.001)) % q3 = 0, q1 = q2
        q1 = q1 + 0.001;
    end
end

% Cuando la suma de magnitudes de los tres angulos da pi o 2pi/3 puede
% ocurrir una singularidad
if(abs(abs(q1)+abs(q2)+abs(q3)-pi)>0.001 || abs(abs(q1)+abs(q2)+abs(q3)-2*pi/3)>0.001)
    q1 = q1 + 0.001;
end

alpha1 = r-h+a*cos(q1); alpha2 = r-h+a*cos(q2); alpha3 = r-h+a*cos(q3);
beta1 = a*sin(q1); beta2 = a*sin(q2); beta3 = a*sin(q3);

e12 = -2*alpha1 + 2*alpha2*cos(phi2);
e22 = 2*alpha2*sin(phi2);
e32 = -2*beta1 + 2*beta2;
e42 = alpha1^2 - alpha2^2 + beta1^2 - beta2^2;

e13 = -2*alpha1 + 2*alpha3*cos(phi3);
e23 = 2*alpha3*sin(phi3);
e33 = -2*beta1 + 2*beta3;
e43 = alpha1^2 - alpha3^2 + beta1^2 - beta3^2;

l0 = e32*e43 - e42*e33;
l1 = e32*e13 - e12*e33;
l2 = e22*e33 - e32*e23;
l3 = e23*e42 - e43*e22;
l4 = e23*e12 - e13*e22;

k0 = 1 + ( l1^2 + l4^2 )/( l2^2 );
k1 = ( 2*l0*l1 + 2*l3*l4 )/( l2^2 ) - 2*alpha1 - 2*beta1*l4/l2;
k2 = ( l0^2 + l3^2 )/( l2^2 ) - 2*beta1*l3/l2 + alpha1^2 + beta1^2 - b^2;

if((k1^2-4*k0*k2)<0)
    %fprintf('No hay soluciones reales')
    px = 0;
    py = 0;
    pz = 0;
    err = 1;
    return
elseif((k1^2-4*k0*k2)>0)
    fprintf('Dos soluciones posibles')
    %px = ( -k1 + sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    px = ( -k1 - sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    py = ( l0 + l1*px )/l2;
    pz = ( l3 + l4*px )/l2;
    if(pz<0)
        px = ( -k1 + sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
        py = ( l0 + l1*px )/l2;
        pz = ( l3 + l4*px )/l2;
    end
elseif((k1^2-4*k0*k2)==0)
    %fprintf('Solo una solucion real')
    %px = ( -k1 + sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    px = ( -k1 - sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    py = ( l0 + l1*px )/l2;
    pz = ( l3 + l4*px )/l2;
else
    %fprintf('Si los centros coinciden, hay infinitas soluciones; si no, no hay soluciones')
    px = 0;
    py = 0;
    pz = a*sin(q1) + sqrt( b^2 - (r-h+a*cos(q1))^2 );
end

a1x = r + a*cos(q1); a1y = 0; a1z = a*sin(q1);
b1x = px+h; b1y = py; b1z = pz;
a2x = (r + a*cos(q2))*cos(phi2); a2y = (r + a*cos(q2))*sin(phi2); a2z = a*sin(q2);
b2x = px+h*cos(phi2); b2y = py+h*sin(phi2); b2z = pz;
a3x = (r + a*cos(q3))*cos(phi3); a3y = (r + a*cos(q3))*sin(phi3); a3z = a*sin(q3);
b3x = px+h*cos(phi3); b3y = py+h*sin(phi3); b3z = pz;

bb1 = sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2); bb2 = sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2); bb3 = sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2);
if(bb1 < b-1 || bb1 > b+1)
    err = 2;
    return
end
if(bb2 < b-1 || bb2 > b+1)
    err = 2;
    return
end
if(bb3 < b-1 || bb3 > b+1)
    err = 2;
    return
end

if(pz < 0)
    err = 1;
end

DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)

a1x = r + a*cos(q1); a1y = 0; a1z = a*sin(q1);
a2x = (r + a*cos(q2))*cos(phi2); a2y = (r + a*cos(q2))*sin(phi2); a2z = a*sin(q2);
a3x = (r + a*cos(q3))*cos(phi3); a3y = (r + a*cos(q3))*sin(phi3); a3z = a*sin(q3);

B1_x = a1x - h*cos(phi1); B1_y = a1y - h*sin(phi1);
B2_x = a2x - h*cos(phi2); B2_y = a2y - h*sin(phi2);
B3_x = a3x - h*cos(phi3); B3_y = a3y - h*sin(phi3);

esfera(b,B1_x,B1_y,a1z,'red')
esfera(b,B2_x,B2_y,a2z,'green')
esfera(b,B3_x,B3_y,a3z,'blue')
