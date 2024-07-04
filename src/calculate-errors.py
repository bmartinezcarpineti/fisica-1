import os
import numpy as np
import pandas as pd

# Define paths
STUDY_CASE = 'double-elastic'
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')

# Constants
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.96339703050364  # unit: N/m
ELASTIC_L0 = 0.135  # L0 

ZERO_POSITION = 0.1493333333333333
FINAL_POSITION = 0.2366666666666666

OBJECT_WIDTH_IN_METERS = 0.055
OBJECT_WIDTH_IN_PIXELS = 165
PIXELS_PER_METER = OBJECT_WIDTH_IN_PIXELS / OBJECT_WIDTH_IN_METERS
ORIGINAL_INPUT_VIDEO_FPS = 240

# Read the input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Rellenar valores nan con 0 
df.fillna(0, inplace=True)

initial_row = df.loc[df['position'] == ZERO_POSITION]
final_row = df.loc[df['position'] == FINAL_POSITION]

# Errors
error_X = OBJECT_WIDTH_IN_METERS / PIXELS_PER_METER
error_T = 1 / ORIGINAL_INPUT_VIDEO_FPS
error_M = 0.001
error_G = 0.01
acceleration_error = df['acceleration'].std()
error_dynamic_friction_coefficient = (1 / 9.81) * acceleration_error

print(f"Error en la aceleracion: {acceleration_error}")

# Calcula el error en la velocidad para cada punto
df['delta_position'] = error_X  # error en la posición
df['delta_time'] = error_T  # error en el tiempo

# Calcula el error en la velocidad utilizando los datos existentes
df['error_speed'] = df['speed'] * np.sqrt((df['delta_position'] / df['position'].diff())**2 + (df['delta_time'] / df['time'].diff())**2)

# Error general en la velocidad
error_general_velocidad = df['error_speed'].mean()  # error promedio

# Calculate kinetic energy error
speed = final_row['speed'].values[0]

print(f"Error en la velocidad: {error_general_velocidad}")

error_kinetic_energy = np.sqrt((0.5 * speed**2)**2 * (error_M)**2 + (OBJECT_MASS * speed)**2 * (error_general_velocidad)**2)
print(f"Error en la variacion de energia cinética: {error_kinetic_energy}")


# Calculate the error in friction work
error_friction_work = np.sqrt((DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY * error_X)**2 +
    (DYNAMIC_FRICTION_COEFFICIENT * GRAVITY * (FINAL_POSITION - ZERO_POSITION) * error_M)**2 +
    (DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * (FINAL_POSITION - ZERO_POSITION) * error_G)**2 +
    (OBJECT_MASS * GRAVITY * (FINAL_POSITION - ZERO_POSITION) * error_dynamic_friction_coefficient)**2)

friction_force = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY

error_friction_force = np.sqrt((OBJECT_MASS * GRAVITY * error_dynamic_friction_coefficient)**2 +
                   (DYNAMIC_FRICTION_COEFFICIENT * GRAVITY * error_M)**2 +
                   (DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * error_G)**2)

print(f"Error en el coeficiente de rozamiento dinámico: {error_dynamic_friction_coefficient}")
print(f"Error en la fuerza de rozamiento: {error_friction_force}")
print(f"Error en el trabajo de rozamiento: {error_friction_work}")