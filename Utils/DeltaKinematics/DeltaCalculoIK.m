%% Cálculo de la cinemática inversa del robot delta
clear
clc
clf
r = 100; % Longitud en mm
h = 45; 
a = 280;
b = 350;

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

px = -134.779; py = 57.623; pz = 374.436;

q1 = deg2rad(62); q2 = deg2rad(21); q3 = deg2rad(40);

DeltaPlot(r,h,a,b,phi2,phi3,q1,q2,q3,px,py,pz)

A1x = r*cos(phi1); A1y = r*sin(phi1); A1z = 0;
A2x = r*cos(phi2); A2y = r*sin(phi2); A2z = 0;
A3x = r*cos(phi3); A3y = r*sin(phi3); A3z = 0;

C1x = px+h*cos(phi1); C1y = py+h*sin(phi1); C1z = pz;
C2x = px+h*cos(phi2); C2y = py+h*sin(phi2); C2z = pz;
C3x = px+h*cos(phi3); C3y = py+h*sin(phi3); C3z = pz;

esfera(a,A1x,A1y,A1z,'red')
drawCircle(b,[C1x,C1y,C1z],[sin(phi1) cos(phi1) 0]','red')
% esfera(a,A2x,A2y,A2z,'green')
% esfera(a,A3x,A3y,A3z,'blue')

%A circle in 3D is parameterized by six numbers: two for the orientation of its unit normal vector, one for the radius, and three for the circle center.
function drawCircle(rad,pos,n,color)
    %https://demonstrations.wolfram.com/ParametricEquationOfACircleIn3D/
    %draws a 3D circle at position pos with radius rad, normal to the
    %circle n, and color color.
    phi = atan2(n(2),n(1)); %azimuth angle, in [-pi, pi]
    theta = atan2(sqrt(n(1)^2 + n(2)^2) ,n(3));% zenith angle, in [0,pi]    
    t = 0:pi/32:2*pi;
    x = pos(1)- rad*( cos(t)*sin(phi) + sin(t)*cos(theta)*cos(phi) );
    y = pos(2)+ rad*( cos(t)*cos(phi) - sin(t)*cos(theta)*sin(phi) );
    z = pos(3)+ rad*sin(t)*sin(theta);
    plot3(x,y,z,color,'LineStyle','--')
end
