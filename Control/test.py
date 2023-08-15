import matplotlib.pyplot as plt
from fun.Trayectorias import *
from fun.DeltaEcuaciones import *
import time
start_time = time.time()

t, qd, dqd, d2qd = trapezoide(tf=1, q0=0, qf=40)

plt.subplot(1, 3, 1)
plt.plot(t,qd,color='red')
plt.title('Trayectoria generada')
plt.subplot(1, 3, 2)
plt.plot(t,dqd,color='green')
plt.title('Velocidad de trayectoria')
plt.subplot(1, 3, 3)
plt.plot(t,d2qd,color='blue')
plt.title('Aceleración de trayectoria')
plt.show()

t, qd, dqd, d2qd = bezier(t2=1, q1=0, q2=40)

plt.subplot(1, 3, 1)
plt.plot(t,qd,color='red')
plt.title('Trayectoria generada')
plt.subplot(1, 3, 2)
plt.plot(t,dqd,color='green')
plt.title('Velocidad de trayectoria')
plt.subplot(1, 3, 3)
plt.plot(t,d2qd,color='blue')
plt.title('Aceleración de trayectoria')
plt.show()

#px, py, pz, err = DeltaFK(q1=math.radians(22.545), q2=math.radians(14.434), q3=math.radians(75.43))
#print(px, py, pz, err)

# q1, q2, q3, err = DeltaIK(px=-177.5, py=177.5, pz=177.5)
# print(math.degrees(q1), math.degrees(q2), math.degrees(q3), err)

# tau1, tau2, tau3 = DeltaDinamica(pz=152.561)
# print(tau1, tau2, tau3)
print("--- %s seconds ---" % (time.time() - start_time))