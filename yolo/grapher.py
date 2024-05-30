import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# files constants
GRAPHER_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIRECTORY = os.path.join(GRAPHER_DIRECTORY_PATH, 'plots')
INPUT_CSV_PATH = os.path.join(GRAPHER_DIRECTORY_PATH, 'data/elastic-data.csv')

df = pd.read_csv(INPUT_CSV_PATH)

print(tabulate(df, headers='keys', tablefmt='psql'))

# Create subplots: one row for each plot
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.1, subplot_titles=('Position vs Time', 'Speed vs Time', 'Acceleration vs Time'))

# Add position scatter plot
fig.add_trace(go.Scatter(x=df['time'], y=df['position'], mode='lines+markers', name='Position'), row=1, col=1)

# Add speed scatter plot
fig.add_trace(go.Scatter(x=df['time'], y=df['speed'], mode='lines+markers', name='Speed'), row=2, col=1)

# Add acceleration scatter plot
fig.add_trace(go.Scatter(x=df['time'], y=df['acceleration'], mode='lines+markers', name='Acceleration'), row=3, col=1)

# Update layout
fig.update_layout(
    title='Position, Speed, and Acceleration in X axis vs. Time',
    height=900,  # Increase the height of the figure to accommodate three plots
    showlegend=False  # Disable the legend for individual traces
)

# Update x-axis title for the bottom plot
fig.update_xaxes(title_text='Time (s)', row=3, col=1)

# Update y-axis titles for each plot
fig.update_yaxes(title_text='Position (m)', row=1, col=1)
fig.update_yaxes(title_text='Speed (m/s)', row=2, col=1)
fig.update_yaxes(title_text='Acceleration (m/s^2)', row=3, col=1)

# Show the figure
fig.show()