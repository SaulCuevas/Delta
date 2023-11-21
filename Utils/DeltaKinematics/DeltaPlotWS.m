function DeltaPlotWS(P)

plot3(P(:,1), P(:,2), P(:,3), '.', 'color', [0.4510 0.1137 0.6588], 'MarkerSize',1)
grid on
axis equal 
set(gca, 'ZDir','reverse')
hold off