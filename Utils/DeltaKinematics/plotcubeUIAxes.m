function plotcubeUIAxes(UIAxes, L, O, alpha, color)

oX = O(1);
oY = O(2);
oZ = O(3);

X = [oX-L/2 oX+L/2 oX+L/2 oX-L/2 oX-L/2; 
    oX-L/2 oX+L/2 oX+L/2 oX-L/2 oX-L/2];
Y = [oY-L/2 oY-L/2 oY-L/2 oY-L/2 oY-L/2;
    oY+L/2 oY+L/2 oY+L/2 oY+L/2 oY+L/2];
Z = [oZ+L/2 oZ+L/2 oZ-L/2 oZ-L/2 oZ+L/2; 
    oZ+L/2 oZ+L/2 oZ-L/2 oZ-L/2 oZ+L/2];

surf(UIAxes, X,Y,Z,'FaceAlpha', alpha, 'FaceColor', color)

X = [oX-L/2 oX+L/2; 
    oX-L/2 oX+L/2];
Y = [oY+L/2 oY+L/2;
    oY+L/2 oY+L/2];
Z = [oZ-L/2 oZ-L/2; 
    oZ+L/2 oZ+L/2];

surf(UIAxes, X,Y,Z,'FaceAlpha', alpha, 'FaceColor', color)

X = [oX-L/2 oX+L/2; 
    oX-L/2 oX+L/2];
Y = [oY-L/2 oY-L/2;
    oY-L/2 oY-L/2];
Z = [oZ-L/2 oZ-L/2; 
    oZ+L/2 oZ+L/2];

surf(UIAxes, X,Y,Z,'FaceAlpha', alpha, 'FaceColor', color)