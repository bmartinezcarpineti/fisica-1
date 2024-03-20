import matplotlib.pyplot as plt

t_final = 10
v0 = 2
x0 = 5

# Funciones MRUV
a = 2

def vel(t):
    return v0 + a * t

def pos(t):
    return x0 + v0 * t + 0.5 * a * (t**2)

# Calcula la velocidad y posicion en cada instante de tiempo
v=[]
for t in range(0, t_final):
  v.append(vel(t))

x=[]
for t in range(0, t_final):
  x.append(pos(t))

# Grafica las funciones
plt.subplot(311)
plt.axhline(y=a, label="Aceleración")
plt.ylabel("m/s^2")
plt.legend()

plt.subplot(312)
plt.plot(v, label="Velocidad")
plt.ylabel("m/s")
plt.legend()

plt.subplot(313)
plt.plot(x, label="Posición")
plt.ylabel("m")
plt.xlabel("t (s)")
plt.legend()

plt.show()