function [q1, q2, q3, err] = DeltaIK(r,h,a,b,phi1,phi2,phi3,px,py,pz)

err = 0;

cx1 = cos(phi1)*px + sin(phi1)*py + h - r;
cy1 = -sin(phi1)*px + cos(phi1)*py;
cz1 = pz;

cx2 = cos(phi2)*px + sin(phi2)*py + h - r;
cy2 = -sin(phi2)*px + cos(phi2)*py;
cz2 = pz;

cx3 = cos(phi3)*px + sin(phi3)*py + h - r;
cy3 = -sin(phi3)*px + cos(phi3)*py;
cz3 = pz;

th31 = acos(cy1/b);
th32 = acos(cy2/b);
th33 = acos(cy3/b);

k1 = ( cx1^2 + cy1^2 + cz1^2 - a^2 - b^2 ) / (2*a*b*sin(th31));
k2 = ( cx2^2 + cy2^2 + cz2^2 - a^2 - b^2 ) / (2*a*b*sin(th32));
k3 = ( cx3^2 + cy3^2 + cz3^2 - a^2 - b^2 ) / (2*a*b*sin(th33));

th21 = acos(k1);
th22 = acos(k2);
th23 = acos(k3);

L1 = ( a*cx1 + b*sin(th31)*( cz1*sin(th21) + cx1*cos(th21) ) ) / ( a^2 + 2*a*b*sin(th31)*cos(th21) + b^2*sin(th31)^2 );
L2 = ( a*cx2 + b*sin(th32)*( cz2*sin(th22) + cx2*cos(th22) ) ) / ( a^2 + 2*a*b*sin(th32)*cos(th22) + b^2*sin(th32)^2 );
L3 = ( a*cx3 + b*sin(th33)*( cz3*sin(th23) + cx3*cos(th23) ) ) / ( a^2 + 2*a*b*sin(th33)*cos(th23) + b^2*sin(th33)^2 );

q1 = acos(L1);
q2 = acos(L2);
q3 = acos(L3);

a1x = r + a*cos(q1); a1y = 0; a1z = a*sin(q1);
a2x = (r + a*cos(q2))*cos(phi2); a2y = (r + a*cos(q2))*sin(phi2); a2z = a*sin(q2);
a3x = (r + a*cos(q3))*cos(phi3); a3y = (r + a*cos(q3))*sin(phi3); a3z = a*sin(q3);

b1x = px+h; b1y = py; b1z = pz;
b2x = px+h*cos(phi2); b2y = py+h*sin(phi2); b2z = pz;
b3x = px+h*cos(phi3); b3y = py+h*sin(phi3); b3z = pz;

if(sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2) > (b+1) || sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2) < (b-1)) 
    q1 = -q1;
end

if(sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2) > (b+1) || sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2) < (b-1))
    q2 = -q2;
end

if(sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2) > (b+1) || sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2) < (b-1))
    q3 = -q3;
end

a1x = r + a*cos(q1); a1y = 0; a1z = a*sin(q1);
a2x = (r + a*cos(q2))*cos(phi2); a2y = (r + a*cos(q2))*sin(phi2); a2z = a*sin(q2);
a3x = (r + a*cos(q3))*cos(phi3); a3y = (r + a*cos(q3))*sin(phi3); a3z = a*sin(q3);

bb1 = sqrt((a1x-b1x)^2 + (a1y-b1y)^2 + (a1z-b1z)^2); bb2 = sqrt((a2x-b2x)^2 + (a2y-b2y)^2 + (a2z-b2z)^2); bb3 = sqrt((a3x-b3x)^2 + (a3y-b3y)^2 + (a3z-b3z)^2);
if(bb1 < b-1 || bb1 > b+1 || ~isreal(bb1))
    err = 2;
    return
end
if(bb2 < b-1 || bb2 > b+1 || ~isreal(bb2))
    err = 2;
    return
end
if(bb3 < b-1 || bb3 > b+1 || ~isreal(bb3))
    err = 2;
    return
end

% if(abs(cy1) < b && abs(k1) < 1) 
%     fprintf('A1B1 intersecta en dos puntos');
% elseif(abs(cy1)==b && (cx1^2+cz1^2)==a^2)
%     fprintf('A1B1 intersecta en un punto singular');
if(abs(cy1)>b || abs(cy2)>b || abs(cy3)>b)
    %fprintf('A1B1 no intersecta');
    err = 1;
end
% if(abs(cy2) < b && abs(k2) < 1) 
%     fprintf('A2B2 intersecta en dos puntos');
% elseif(abs(cy2)==b && (cx2^2+cz2^2)==a^2)
%     fprintf('A2B2 intersecta en un punto singular');
% if(abs(cy2)>b)
%     fprintf('A2B2 no intersecta');
% end
% if(abs(cy3) < b && abs(k3) < 1) 
%     fprintf('A3B3 intersecta en dos puntos');
% elseif(abs(cy3)==b && (cx3^2+cz3^2)==a^2)
%     fprintf('A3B3 intersecta en un punto singular');
% if(abs(cy3)>b)
%     fprintf('A3B3 no intersecta');
% end