import csv
import os
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
from datetime import datetime

# Define paths
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "simple-elastic"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-energy.txt')
OUTPUT_PLOT_TIME_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-energy-plot-time.html')
OUTPUT_PLOT_POSITION_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-energy-plot-position.html')

# Constants
ELASTIC_ZERO_POSITION = 0.28
ELASTIC_L0 = 0.135  # unit: m
ELASTIC_CONSTANT = 74.75  # unit: N/m

elastic_energies = []

# Read input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Calculate elastic energies
for index, row in df.iterrows():
    distance_to_elastic_zero = ELASTIC_ZERO_POSITION - row['position']
    
    elastic_energy = (1/2) * ELASTIC_CONSTANT * (4 * ((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - 4 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) * ELASTIC_L0 + ELASTIC_L0**2)
    elastic_energies.append(elastic_energy)

df['elastic_energy'] = elastic_energies

# Save the updated dataframe to CSV
df.to_csv(INPUT_CSV_PATH, index=False)

# Save elastic energies to TXT
OUTPUT_STRING = f"Elastic energies: {elastic_energies}\n\nDate: {datetime.now()}"
os.makedirs(os.path.dirname(OUTPUT_TXT_PATH), exist_ok=True)
with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)

# Plot the elastic energy vs time
fig_time = go.Figure()

fig_time.add_trace(go.Scatter(
    x=df['time'],
    y=df['elastic_energy'],
    mode='lines+markers',
    name='Elastic Energy vs Time'
))

fig_time.update_layout(
    xaxis_title='Time (s)',
    yaxis_title='Elastic Energy (J)',
    title='Elastic Energy vs Time'
)

# Save the plot as an HTML file
os.makedirs(os.path.dirname(OUTPUT_PLOT_TIME_PATH), exist_ok=True)
fig_time.write_html(OUTPUT_PLOT_TIME_PATH)

print(f"Time plot saved to {OUTPUT_PLOT_TIME_PATH}")

# Plot the elastic energy vs position
fig_position = go.Figure()

fig_position.add_trace(go.Scatter(
    x=df['position'],
    y=df['elastic_energy'],
    mode='lines+markers',
    name='Elastic Energy vs Position'
))

fig_position.update_layout(
    xaxis_title='Position (m)',
    yaxis_title='Elastic Energy (J)',
    title='Elastic Energy vs Position'
)

# Save the plot as an HTML file
os.makedirs(os.path.dirname(OUTPUT_PLOT_POSITION_PATH), exist_ok=True)
fig_position.write_html(OUTPUT_PLOT_POSITION_PATH)

print(f"Position plot saved to {OUTPUT_PLOT_POSITION_PATH}")

# Open the plots in the default web browser
import webbrowser
webbrowser.open('file://' + os.path.realpath(OUTPUT_PLOT_TIME_PATH))
webbrowser.open('file://' + os.path.realpath(OUTPUT_PLOT_POSITION_PATH))
