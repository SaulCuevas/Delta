%% Cálculo de la cinemática directa del robot delta
clear
clc
clf
r = 100; % Longitud en mm
h = 45; 
a = 250;
b = 500;

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

%px = -200; py = 200; pz = 400;
px = 3.800237030585067; py = 1.818707784884528e+02; pz = 3.552488180405616e+02;

%q1 = 0.900512494025016; q2 = -0.387349286236903; q3 = 0.617712099211789;
q1 = 0;	q2 = -0.506145483078356;	q3 = 0.506145483078356;

subplot(2,2,1);

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

view([0 0]);
title('(a) Vista frontal');

subplot(2,2,2);
DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)
esfera(b,B1_x,B1_y,a1z,'red')
esfera(b,B2_x,B2_y,a2z,'green')
esfera(b,B3_x,B3_y,a3z,'blue')
view([90 0]);
title('(b) Vista derecha');

subplot(2,2,3);
DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)
esfera(b,B1_x,B1_y,a1z,'red')
esfera(b,B2_x,B2_y,a2z,'green')
esfera(b,B3_x,B3_y,a3z,'blue')
view([180 0]);
title('(c) Vista posterior');

subplot(2,2,4);
DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)
esfera(b,B1_x,B1_y,a1z,'red')
esfera(b,B2_x,B2_y,a2z,'green')
esfera(b,B3_x,B3_y,a3z,'blue')
view([145 30]);
title('(d) Vista general');

%%%%%%%%%%%%%%
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
    fprintf('No hay soluciones reales')
elseif((k1^2-4*k0*k2)>0)
    %fprintf('Dos soluciones posibles')
    %px = ( -k1 + sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    px = ( -k1 - sqrt(k1^2 - 4*k0*k2) )/( 2*k0 );
    py = ( l0 + l1*px )/l2;
    pz = ( l3 + l4*px )/l2;
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

% figure
% DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)