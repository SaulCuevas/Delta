function DeltaPlot(r, h, a, b, phi2, phi3, q1, q2, q3, px, py, pz)

% Generación de triángulo fijo
Ox = 0; Oy = 0; Oz = 0;
TRx = [r r*cos(phi2) r*cos(phi3) r];
TRy = [0 r*sin(phi2) r*sin(phi3) 0];
TRz = [0 0 0 0];

%clf
plot3(TRx,TRy,TRz,'Color',"black",'Marker','o');
set(gca, 'ZDir','reverse')
xlabel('X') 
ylabel('Y') 
zlabel('Z')
axis equal
grid on
hold on

% Punto final
plot3(px,py,pz,'Color',"magenta",'Marker','x')

% Generación de triángulo móvil
Trx = [px+h px+h*cos(phi2) px+h*cos(phi3) px+h];
Try = [py py+h*sin(phi2) py+h*sin(phi3) py];
Trz = [pz pz pz pz];
plot3(Trx,Try,Trz,'Color',"black",'Marker','o');

% Primera cadena cinemática
M1x = r; M1y = 0; M1z = 0;
a1x = r + a*cos(q1); a1y = 0; a1z = a*sin(q1);
b1x = px+h; b1y = py; b1z = pz;
CC1x = [Ox M1x a1x b1x]; CC1y = [Oy M1y a1y b1y]; CC1z = [Oz M1z a1z b1z];

plot3(CC1x,CC1y,CC1z,'Color',"red",'Marker','o')

% Segunda cadena cinemática
M2x = r*cos(phi2); M2y = r*sin(phi2); M2z = 0;
a2x = (r + a*cos(q2))*cos(phi2); a2y = (r + a*cos(q2))*sin(phi2); a2z = a*sin(q2);
b2x = px+h*cos(phi2); b2y = py+h*sin(phi2); b2z = pz;
CC2x = [Ox M2x a2x b2x]; CC2y = [Oy M2y a2y b2y]; CC2z = [Oz M2z a2z b2z];

plot3(CC2x,CC2y,CC2z,'Color',"green",'Marker','o')

% Tercera cadena cinemática
M3x = r*cos(phi3); M3y = r*sin(phi3); M3z = 0;
a3x = (r + a*cos(q3))*cos(phi3); a3y = (r + a*cos(q3))*sin(phi3); a3z = a*sin(q3);
b3x = px+h*cos(phi3); b3y = py+h*sin(phi3); b3z = pz;
CC3x = [Ox M3x a3x b3x]; CC3y = [Oy M3y a3y b3y]; CC3z = [Oz M3z a3z b3z];

plot3(CC3x,CC3y,CC3z,'Color',"blue",'Marker','o')

% bb1 = sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2); bb2 = sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2); bb3 = sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2);
% if(sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2) < b-1 || sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2) > b+1)
%     bb1
% end
% if(sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2) < b-1 || sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2) > b+1)
%     bb2
% end
% if(sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2) < b-1 || sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2) > b+1)
%     bb3
% end