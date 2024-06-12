import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "friction"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-kinetic-energy.txt')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-kinetic-energy-plot.html')

OBJECT_MASS = 0.284 # unit: kg

kinetic_energies = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    speed = row['speed']
    
    kinetic_energy = (1/2) * OBJECT_MASS * (speed**2)

    kinetic_energies.append(kinetic_energy)

df['kinetic_energy'] = kinetic_energies
df.to_csv(INPUT_CSV_PATH)

cleaned_kinetic_energies = [i for i in kinetic_energies if not math.isnan(i)] # removes NaN values

OUTPUT_STRING = f"Kinetic energies: {cleaned_kinetic_energies}\n\nDate: {datetime.now()}"

with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)

# plots the kinetic energy
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['kinetic_energy'],
    mode='lines+markers',
    name='Kinetic Energy'
))

fig.update_layout(
    xaxis_title='Time (s)',
    yaxis_title='Kinetic Energy (J)',
    title='Kinetic Energy vs Time'
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()
