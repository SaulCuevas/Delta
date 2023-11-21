%% Cálculo de la cinemática del robot delta
clear
clc
r = 100; % Longitud en mm
h = 45; 
a = 250;
b = 500;

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

%% Cinemática directa

q1Deg = 60; q2Deg =	42; q3Deg =	78;

q1 = deg2rad(q1Deg); q2 = deg2rad(q2Deg); q3 = deg2rad(q3Deg);
%q1 = 1.37881010907552;	q2 = 1.76278254451427;	q3 = 1.76278254451427;
%q1 = 0;	q2 = -0.507145483078356;	q3 = 0.506145483078356;

%[px, py, pz, err] = DeltaFK(r,h,a,b,phi1,phi2,phi3,q1,q2,q3);
[px, py, pz, err] = DeltaFK(r, h, a, b, phi1, phi2, phi3, q1, q2, q3);

DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)

%% Cinemática inversa

px = 0; py = 0; pz = 400;

[q1, q2, q3, err] = DeltaIK(r,h,a,b,phi1,phi2,phi3,px,py,pz);
q1Deg = rad2deg(q1); q2Deg = rad2deg(q2); q3Deg = rad2deg(q3);

DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)

%% Espacio de trabajo
clear
clc
r = 80; % Longitud en mm
h = 25; 
a = 110;
b = 225.5;

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

tic
[Ps, Zmin, Zmax, ERR] = DeltaWorkSpace(r, h, a, b, phi1, phi2, phi3);
toc

if(ERR == 1)
    fprintf('Singularidad no contemplada\n');
end
DeltaPlotWS(Ps)
[sum, middleZ, X, Y, Z, Q1, Q2, Q3] = Cuboid(r, h, a, b, phi1, phi2, phi3);
plotcube([2*sum 2*sum 2*sum], [-sum  -sum  middleZ-sum], .3, [0 1 0])