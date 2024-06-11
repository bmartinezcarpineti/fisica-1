#results for case b)
import matplotlib.pyplot as plt
import numpy as np
import os
import numpy as np
import pandas as pd

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/simple-elastic-data.csv')

GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.75  # unit: N/m
ELASTIC_L0 = 0.135 # unit: m

df = pd.read_csv(INPUT_CSV_PATH)

time = df['time'].values
position = df['position'].values

acceleration = (-DYNAMIC_FRICTION_COEFFICIENT * GRAVITY) + (2 * ELASTIC_CONSTANT / OBJECT_MASS) * (2 * position - (ELASTIC_L0 * position) / np.sqrt(position**2 + (ELASTIC_L0 / 2)**2))
   
speed_values = np.zeros_like(position)
new_position = np.zeros_like(position)
new_position[0] = position[0]  # La posición inicial es la primera del archivo

for i in range(1, len(time)):
    delta_t = time[i] - time[i-1]
    speed_values[i] = speed_values[i-1] + acceleration[i-1] * delta_t
    new_position[i] = new_position[i-1] + speed_values[i-1] * delta_t

plt.figure(figsize=(12, 8))

# Graficar aceleración
plt.subplot(3, 1, 1)
plt.plot(time, acceleration, label='Aceleración')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.legend()
plt.grid(True)

# Graficar velocidad
plt.subplot(3, 1, 2)
plt.plot(time, speed_values, label='Velocidad', color='g')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.legend()
plt.grid(True)

# Graficar posición
plt.subplot(3, 1, 3)
plt.plot(time, new_position, label='Posición', color='r')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
