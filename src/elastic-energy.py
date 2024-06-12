import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "series-elastic"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-energy.txt')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-energy-plot.html')

ELASTIC_ZERO_POSITION = 0.28
ELASTIC_L0 = 0.135 # unit: m
ELASTIC_CONSTANT = 74.75 # unit: N/m

elastic_energies = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    distance_to_elastic_zero = ELASTIC_ZERO_POSITION - row['position']
    
    elastic_energy = (1/2) * ELASTIC_CONSTANT * (4 * ((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - 4 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) * ELASTIC_L0 + ELASTIC_L0**2)

    elastic_energies.append(elastic_energy)

df['elastic_energy'] = elastic_energies

df.to_csv(INPUT_CSV_PATH)

OUTPUT_STRING = f"Elastic energies: {elastic_energies}\n\nDate: {datetime.now()}"

with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)

# plots the elastic energy
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['elastic_energy'],
    mode='lines+markers',
    name='Elastic Energy'
))

fig.update_layout(
    xaxis_title='Time (s)',
    yaxis_title='Elastic Energy (J)',
    title='Elastic Energy vs Time'
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()