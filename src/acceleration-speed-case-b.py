import csv
import os
import numpy as np
import pandas as pd
from tabulate import tabulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# files constants
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "simple-elastic"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-positions.csv')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-speed-acceleration-plot.html')

input_df = pd.read_csv(INPUT_CSV_PATH)

# reduces noise (friction only: 5, simple elastic: 3, double elastic: 3, series elastic: 5)
reduced_noise_time = input_df['time'].iloc[::3]
reduced_noise_position = input_df['position'].iloc[::3]

# output dataframe
df = pd.DataFrame()
df['time'] = reduced_noise_time
df['position'] = reduced_noise_position

# calculates speed and acceleration
df['speed'] = df['position'].diff() / df['time'].diff()
df['acceleration'] = df['speed'].diff() / df['time'].diff()

# Cálculo de la aceleración teórica
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 32.24048176040744 # unit: N/m
ELASTIC_L0 = 0.135 # unit: m

time = df['time'].values
position = df['position'].values

acceleration_theoretical = (-DYNAMIC_FRICTION_COEFFICIENT * GRAVITY) + (2 * ELASTIC_CONSTANT / OBJECT_MASS) * (2 * position - (ELASTIC_L0 * position) / np.sqrt(position**2 + (ELASTIC_L0 / 2)**2))

# Agregar la aceleración teórica al DataFrame
df['acceleration_theoretical'] = acceleration_theoretical

# shows results
print(tabulate(df, headers='keys', tablefmt='psql'))

# plots the position, speed and acceleration
fig = make_subplots(rows=4, cols=1, shared_xaxes=True, 
    vertical_spacing=0.1, subplot_titles=('Position vs Time', 'Speed vs Time', 'Acceleration vs Time', 'Theoretical Acceleration vs Time'))

fig.add_trace(go.Scatter(x=df['time'], y=df['position'], mode='lines+markers', name='Position'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['time'], y=df['speed'], mode='lines+markers', name='Speed'), row=2, col=1)
fig.add_trace(go.Scatter(x=df['time'], y=df['acceleration'], mode='lines+markers', name='Acceleration'), row=3, col=1)
fig.add_trace(go.Scatter(x=df['time'], y=df['acceleration_theoretical'], mode='lines+markers', name='Theoretical Acceleration'), row=4, col=1)

fig.update_layout(
    title='Position, Speed, Acceleration and Theoretical Acceleration in X axis vs. Time',
    height=1200,
    showlegend=False
)

fig.update_xaxes(title_text='Time (s)', row=4, col=1)

fig.update_yaxes(title_text='Position (m)', row=1, col=1)
fig.update_yaxes(title_text='Speed (m/s)', row=2, col=1)
fig.update_yaxes(title_text='Acceleration (m/s^2)', row=3, col=1)
fig.update_yaxes(title_text='Theoretical Acceleration (m/s^2)', row=4, col=1)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()
