function [Ps, minZ, maxZ, ERR] = DeltaWorkSpace(r, h, a, b, phi1, phi2, phi3)
ERR = 0;
n = 1; % Puntos+1 encontrados
% e = 1; % Puntos+1 encontrados no posibles
% m = 1; % Puntos+1 encontrados con singularidades no resueltas

minZ = a+b;
maxZ = 0;

angI = -45;
angF = 120;
d = 3; % Grados entre mediciones
Ps = zeros((int64(angF-angI)/d)^3, 3);
% Qs = zeros((int64(angF-angI)/d)^3, 3);
% errQs = zeros((int64(angF-angI)/d)^3, 3);
% singQs = zeros((int64(angF-angI)/d)^3, 3);

angI = deg2rad(angI);
angF = deg2rad(angF);
d = deg2rad(d);

for q1 = angI : d : angF
    for q2 = angI : d : angF
        for q3 = angI : d : angF
            [px, py, pz, err] = DeltaFK(r, h, a, b, phi1, phi2, phi3, q1, q2, q3);
            if err == 0 
               Ps(n, 1) = px;
               Ps(n, 2) = py;
               Ps(n, 3) = pz;
%                Qs(n, 1) = q1;
%                Qs(n, 2) = q2;
%                Qs(n, 3) = q3;
               n = n+1;

               if(minZ > pz)
                   minZ = pz;
%                    q = [q1, q2, q3];
%                    pmin = [px, py, pz];
               end
               if(maxZ < pz)
                   maxZ = pz;
%                    Q = [q1, q2, q3];
%                    pmax = [px, py, pz];
               end
             elseif err == 2
                 ERR = 1;
%                 singQs(m, 1) = q1;
%                 singQs(m, 2) = q2;
%                 singQs(m, 3) = q3;
%                 m = m+1;
%             else
%                errQs(e, 1) = rad2deg(q1);
%                errQs(e, 2) = rad2deg(q2);
%                errQs(e, 3) = rad2deg(q3);
%                e = e+1;
             end
         end
    end
end
