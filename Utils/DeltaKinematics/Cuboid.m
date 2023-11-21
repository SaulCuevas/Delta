function [sum, middleZ, X,Y,Z,Q1,Q2,Q3] = Cuboid(r, h, a, b, phi1, phi2, phi3)
    maxZ = 0;
    minZ = a+b+r+h;
    
    s = 200*8;
    sd = 360/s;
    for Z = 1:sd:s
        [~, ~, pz, err] = DeltaFK(r, h, a, b, phi1, phi2, phi3, Z*sd, Z*sd, Z*sd);
        if(err == 0)
            if(minZ>pz) 
                minZ=pz;
            end
            if(maxZ<pz) 
                maxZ=pz;
            end
        end
    end
    
    middleZ = (maxZ+minZ)/2;
    original_dist = (maxZ-middleZ);
    dist = original_dist/2;
    sum = 0;
    err = zeros(8,1);
    q = zeros(8,3);
    
    mint1= 2*pi;
    maxt1=-2*pi;
    mint2= 2*pi;
    maxt2=-2*pi;
    mint3= 2*pi;
    maxt3=-2*pi;

    while(original_dist > sum && dist > 0.1)
        sum = sum + dist;
        [q(1,1),q(1,2),q(1,3),err(1)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, +sum, +sum, middleZ+sum);
        [q(2,1),q(2,2),q(2,3),err(2)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, +sum, -sum, middleZ+sum);
        [q(3,1),q(3,2),q(3,3),err(3)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, -sum, -sum, middleZ+sum);
        [q(4,1),q(4,2),q(4,3),err(4)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, -sum, +sum, middleZ+sum);
        [q(5,1),q(5,2),q(5,3),err(5)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, +sum, +sum, middleZ-sum);
        [q(6,1),q(6,2),q(6,3),err(6)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, +sum, -sum, middleZ-sum);
        [q(7,1),q(7,2),q(7,3),err(7)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, -sum, -sum, middleZ-sum);
        [q(8,1),q(8,2),q(8,3),err(8)] = DeltaIK(r, h, a, b, phi1, phi2, phi3, -sum, +sum, middleZ-sum);
        if (max(err) ~= 0)
            sum = sum - dist;
            dist = dist/2;
        else
            for i = 1:8
                if(mint1>q(i,1)) 
                    mint1=q(i,1);
                end
                if(maxt1<q(i,1)) 
                    maxt1=q(i,1);
                end
                if(mint2>q(i,2)) 
                    mint2=q(i,2);
                end
                if(maxt2<q(i,2)) 
                    maxt2=q(i,2);
                end
                if(mint3>q(i,3)) 
                    mint3=q(i,3);
                end
                if(maxt3<q(i,3)) 
                    maxt3=q(i,3);
                end
            end
        end
    end
    
    maxX = sum;
    maxY = sum;
    maxZ = middleZ+sum;
    minX = -sum;
    minY = -sum;
    minZ = middleZ-sum;
    X = [minX,maxX];
    Y = [minY,maxY];
    Z = [minZ,maxZ];
    Q1 = rad2deg([mint1,maxt1]);
    Q2 = rad2deg([mint1,maxt1]);
    Q3 = rad2deg([mint1,maxt1]);