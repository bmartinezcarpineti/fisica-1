import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/elastic-data.csv')

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

print(elastic_energies)

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

fig.show()