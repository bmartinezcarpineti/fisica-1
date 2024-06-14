import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "simple-elastic"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-contant.txt')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-contant-plot.html')

GRAVITY = 9.81 # unit: m/s^s
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_ZERO_POSITION = 0.28
ELASTIC_L0 = 0.135 # unit: m
OBJECT_MASS = 0.284 # unit: kg

elastic_constants = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    acceleration = row['acceleration']
    distance_to_elastic_zero = ELASTIC_ZERO_POSITION - row['position']

    elastic_constant_numerator = OBJECT_MASS * (acceleration + DYNAMIC_FRICTION_COEFFICIENT * GRAVITY) * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2)
    elastic_constant_denominator = 2 * distance_to_elastic_zero * (2 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - ELASTIC_L0)

    elastic_constant = elastic_constant_numerator / elastic_constant_denominator

    elastic_constants.append(elastic_constant)

df['elastic_constant'] = elastic_constants

cleaned_elastic_constants = [i for i in elastic_constants if not math.isnan(i)] # removes NaN values
#cleaned_elastic_constants.pop(-1)
#cleaned_elastic_constants.pop(-1)

mean_elastic_constant = np.mean(cleaned_elastic_constants)
elastic_constant_error = np.std(cleaned_elastic_constants)

OUTPUT_STRING = f"Elastic contants: {cleaned_elastic_constants}\n\
Mean elastic constant: {mean_elastic_constant}\nError: {elastic_constant_error}\n\nDate: {datetime.now()}"

with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)

# plots the kinetic energy
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['elastic_constant'],
    mode='lines+markers',
    name='Elastic Constant'
))

fig.update_layout(
    xaxis_title='Time (s)',
    yaxis_title='Elastic Constant (N/m)',
    title='Elastic Constant vs Time'
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()