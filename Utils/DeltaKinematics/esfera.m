function esfera(radius,xoffset,yoffset,zoffset,color)
% Make unit sphere
[x,y,z] = sphere;
% Scale to desire radius.
x = x * radius;
y = y * radius;
z = z * radius;
% Translate sphere to new location.
% Plot as surface.
plot3(xoffset,yoffset,zoffset,'Color',"black",'Marker','o')
surf(x+xoffset,y+yoffset,z+zoffset,'LineStyle',':','FaceColor','none','EdgeColor',color) 