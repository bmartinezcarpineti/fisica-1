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
   
plt.figure(figsize=(12, 8))

# Graficar aceleración
plt.subplot(3, 1, 1)
plt.plot(time, acceleration, label='Aceleración')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
