import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define paths
STUDY_CASE = 'friction'
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-force.html')

# Constants
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8

# Read the input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Rellenar valores nan con 0
df.fillna(0, inplace=True)

# Calculate the friction force
friction_force = - (DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY)
friction_force_array = np.full(len(df), friction_force)  # Crear un array con el mismo tamaño que el DataFrame

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['position'], y=friction_force_array, mode='lines+markers', name='Fuerza de Fricción o Rozamiento'))

fig.update_layout(
    title='Fuerza de Fricción o Rozamiento vs Position',
    xaxis_title='Position (m)',
    yaxis_title='Fuerza Fricción (N)',
    font=dict(
        size=20,  # Tamaño de la fuente para todo el gráfico
    ),
    title_font=dict(
        size=26  # Tamaño de la fuente para el título
    ),
    xaxis=dict(
        title_font=dict(size=22),  # Tamaño de la fuente para el título del eje x
        tickfont=dict(size=18)     # Tamaño de la fuente para las etiquetas del eje x
    ),
    yaxis=dict(
        title_font=dict(size=22),  # Tamaño de la fuente para el título del eje y
        tickfont=dict(size=18)     # Tamaño de la fuente para las etiquetas del eje y
    )
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()

print(f"Valor de la fuerza de rozamiento: {friction_force}")  
