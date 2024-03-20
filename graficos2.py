import matplotlib.pyplot as plt
import numpy as np

t_final = 10
t = np.linspace(0, t_final, 10)

v0 = 2 
x0 = 5

# Funciones MRUV
a = 2
v = v0 + a * t
x = x0 + v0 * t + 0.5 * a * (t**2)

# Grafica las funciones
plt.subplot(311)
plt.axhline(y=a, label="Aceleración")
plt.ylabel("m/s^2")
plt.legend()

plt.subplot(312)
plt.plot(t, v, label="Velocidad")
plt.ylabel("m/s")
plt.legend()

plt.subplot(313)
plt.plot(t, x, label="Posición")
plt.ylabel("m")
plt.xlabel("t (s)")
plt.legend()

plt.show()
