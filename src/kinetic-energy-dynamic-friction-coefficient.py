import os
import numpy as np
import math
from scipy.optimize import curve_fit
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "friction"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-kinetic-energy-dynamic-friction-coefficient.txt')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-kinetic-energy-dynamic-friction-coefficient-plot.html')

OBJECT_MASS = 0.284 # unit: kg
GRAVITY = 9.81  # unit: m/s^2

df = pd.read_csv(INPUT_CSV_PATH)

def lineal(x,a,b):
    return(b - a*x)

# Ajuste de la curva
popt, pcov = curve_fit(lineal, xdata=df['position'][1:], ydata=df['kinetic_energy'][1:])
errs = np.sqrt(np.diag(pcov))
print("Parámetros óptimos:", popt)
print("Errores estándar de los parámetros:", errs)

slope  = popt[0]
kinetic_energy_dynamic_friction_coefficient = slope / (OBJECT_MASS * GRAVITY)

# calculates error
slope_error = errs[0]
mass_error = 0.001 # mass = 0.284 ---> 3 lugares despiertos despues de la coma
kinetic_energy_dynamic_friction_coefficient_error = math.sqrt(((1/(OBJECT_MASS * GRAVITY)) ** 2 * slope_error ** 2 - (slope/(GRAVITY * OBJECT_MASS ** 2 )) ** 2 * mass_error ** 2))

y = lineal(df.position,2.44,1.08)
df['y']=y

# Save the dynamic friction coefficient to a file
OUTPUT_STRING = f"Dynamic friction coefficient: {kinetic_energy_dynamic_friction_coefficient}\n\
Error: {kinetic_energy_dynamic_friction_coefficient_error}\n\nDate: {datetime.now()}"

with open(OUTPUT_TXT_PATH, 'w') as file:
    file.write(OUTPUT_STRING)

# plots the kinetic energy
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['position'][1:],
    y=df['y'][1:],
    mode='lines+markers',
    name='Ajuste de Energía Cinética | Ecin = 1.08 - 2.44*x'
))
fig.add_trace(go.Scatter(
    x=df['position'][1:],
    y=df['kinetic_energy'][1:],
    mode='lines+markers',
    name='Variación de Energía Cinética vs Posición'
))
fig.update_layout(
    xaxis_title='Posición (m)',
    yaxis_title='Energía Cinética (J)',
    title='Energía Cinética vs Posición'
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()