function [tau_1, tau_2, tau_3] = Dinamica(px, py, pz, d2px, d2py, d2pz, theta11, theta12, theta13, d2theta11, d2theta12, d2theta13)

phi1 = 0; phi2 = 2*pi/3; phi3 = -2*pi/3;

r = 0.100; % radio de base fija (m)
h = 0.065; % radio de base movil (m)
a = 0.280; % longitud bicep (m)
% b = 0.350; % longitud antebrazo (m)
I_m = 0.057565963175172; % Momento de inercia del rotor
m_a = 0.229997; % masa a (kg)
m_b = 0.080931; % masa b (kg) [cada uno]
m_p = 1.160627; % masa de la plataforma movil (kg)
g_c = 9.80665; % valor de la gravedad

f_px = 0;
f_py = 0;
f_pz = 0;

A = [2*( px+h*cos(phi1)-r*cos(phi1)-a*cos(phi1)*cos(theta11) ), 2*( px+h*cos(phi2)-r*cos(phi2)-a*cos(phi2)*cos(theta12) ), 2*( px+h*cos(phi3)-r*cos(phi3)-a*cos(phi3)*cos(theta13) );
     2*( py+h*sin(phi1)-r*sin(phi1)-a*sin(phi1)*cos(theta11) ), 2*( py+h*sin(phi2)-r*sin(phi2)-a*sin(phi2)*cos(theta12) ), 2*( py+h*sin(phi3)-r*sin(phi3)-a*sin(phi3)*cos(theta13) );
     2*( pz-a*sin(theta11) ), 2*( pz-a*sin(theta12) ), 2*( pz-a*sin(theta13) )];

B = [(m_p+3*m_b)*d2px-f_px;
     (m_p+3*m_b)*d2py-f_py;
     (m_p+3*m_b)*(d2pz+g_c)-f_pz];

lambda = inv(A)*B;

tau_1 = (I_m + (1/3)*m_a*a^2 + m_b*a^2)*d2theta11 + ( (1/2)*m_a+m_b )*g_c*a*cos(theta11) - 2*a*lambda(1)*( (px*cos(phi1) + py*sin(phi1) + h - r)*sin(theta11) - pz*cos(theta11) );
tau_2 = (I_m + (1/3)*m_a*a^2 + m_b*a^2)*d2theta12 + ( (1/2)*m_a+m_b )*g_c*a*cos(theta12) - 2*a*lambda(2)*( (px*cos(phi2) + py*sin(phi2) + h - r)*sin(theta12) - pz*cos(theta12) );
tau_3 = (I_m + (1/3)*m_a*a^2 + m_b*a^2)*d2theta13 + ( (1/2)*m_a+m_b )*g_c*a*cos(theta13) - 2*a*lambda(3)*( (px*cos(phi3) + py*sin(phi3) + h - r)*sin(theta13) - pz*cos(theta13) );
