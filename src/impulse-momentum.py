import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "double-elastic"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-impulse-momentum.txt')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-impulse-plot.html')

GRAVITY = 9.81 # unit: m/s^s
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_ZERO_POSITION = 0.28
ELASTIC_L0 = 0.135 # unit: m
ELASTIC_CONSTANT = 74.75 # unit: N/m
OBJECT_MASS = 0.284 # unit: kg

df = pd.read_csv(INPUT_CSV_PATH)

elastic_forces = []
elastic_impulses = []
positions = []
initial_time = None
elastic_force_impulse = 0

for index, row in df.iterrows():
    distance_to_elastic_zero = ELASTIC_ZERO_POSITION - row['position']
    final_time = row['time']

    elastic_force = ELASTIC_CONSTANT * (2 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - ELASTIC_L0)
        
    if initial_time is not None:
        impulse = elastic_force * (final_time - initial_time)
        elastic_force_impulse += impulse
        elastic_impulses.append(elastic_force_impulse)
        positions.append(row['position'])
    else:
        elastic_impulses.append(0)
        positions.append(row['position'])

    initial_time = final_time

friction_force_impulse = - DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY * (df['time'].iloc[-1] - df['time'].iloc[0])

total_impulse = elastic_force_impulse + friction_force_impulse

momentum_variation = (OBJECT_MASS * df['speed'].iloc[-1]) - (OBJECT_MASS * df['speed'].iloc[1]) # m * v(final) - m * v(inital)

OUTPUT_STRING = f"Elastic force impulse: {elastic_force_impulse}\n\
Friction force impulse: {friction_force_impulse}\n\
Total impulse: {total_impulse}\n\
Variation of momentum: {momentum_variation}"

with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)

# Generate plot of impulse vs position
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=positions,
    y=elastic_impulses,
    mode='lines+markers',
    name='Fuerza de Impulso'
))

fig.update_layout(
    xaxis_title='Posición (m)',
    yaxis_title='Impulso (Ns)',
    title='Impulso vs Posición'
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()
