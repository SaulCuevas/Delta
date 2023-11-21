%% Planta identificada

clc
clear
close all

K = 0.93515
tau = 0.037049
delay = 0.016343

motor = tf(K, [tau 1], 'InputDelay', delay);
%step(motor)

%% PID Tuner

load('C.mat','C*')
Kp = C.Kp; Ki = C.Ki; Kd = C.Kd;
P = Kp; I = Ki; D = Kd;

%% PID Z-N
out = sim('PIDTuning_obtencion.slx');

figure
plot(out.t,out.y1_1,'DisplayName','Respuesta del sistema','LineWidth',2,'Color',[95/255 15/255 64/255])
grid on
hold on
title('Respuesta al escalón unitario de la FTLA');

[~,x0] = max(abs(out.y1_3)); % Se obtiene el último valor del vector donde es casi 0
x0 = x0 + 1;
y0 = out.y1_1(x0); % Valor para la recta
m = out.y1_2(x0+1);
b = y0 - m*(x0-1)*0.001;
x = 0:0.001:3;
z = m*(x) + b;

plot(x,z,'DisplayName','Aproximación de la FTLA','LineWidth',2,'Color',[251/255 139/255 36/255])
ylim([-1 3])
legend('show')

z0 = find(z>=0);
z0 = z0(1); % Se obtiene el primer valor del vector donde es casi 0
L = delay;

z1 = find(z>=K);
z1 = z1(1); % Se obtiene el primer valor del vector donde es casi 0
T = (z1 - z0)*0.001;

ZN_Kp = 1.2*(T/delay);
ZN_Ti = 2*delay;
ZN_Td = 0.5*delay;

P = ZN_Kp;
I = ZN_Kp/ZN_Ti;
D = ZN_Kp*ZN_Td;

%% PID Lambda

lambda = 3*tau;
LKp = tau/(K*(0.5*delay+lambda));
LTi = tau;
LTd = 0.5*delay;

Lkp = LKp*((LTi+LTd)/LTi);
Lti = LTi + LTd;
Ltd = LTi*LTd/(LTi+LTd);

%% Cohen-Coon
N = K/T;
R = delay/T;
Kc = (1/(N*L))*(1.33+(R/4));
CCTi = L*(30+3*R)/(9+20*R);
CCTd = 4*L/(11+2*R);
CCP = Kc;
CCI = Kc/CCTi;
CCD = Kc*CCTd;