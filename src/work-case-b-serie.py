import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define paths
STUDY_CASE = 'series-elastic'
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-work-elastic-case-b.html')
OUTPUT_PLOT_PATH_2 = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-frictionwork-energy-case-b.html')
OUTPUT_PLOT_PATH_3 = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-elastic-forces-case-b.html')

# Constants
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 11.32  # unit: N/m
ELASTIC_L0 = 0.135  # L0 

ZERO_POSITION = 0.077
FINAL_POSITION = 0.1456666666666666

# Read the input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Rellenar valores nan con 0
df.fillna(0, inplace=True)

# Initialize lists for works
friction_works = []
elastic_works_1 = []
elastic_works_2 = []
total_works_delta= []
total_works_1= []
total_works_2= []
elastic_energies = []  
kinetic_energies =[]
elastic_forces_1 = []
elastic_forces_2 = []
resultant_forces = []

initial_row = df.loc[df['position'] == ZERO_POSITION]
final_row = df.loc[df['position'] == FINAL_POSITION]

# Kinetic energies
initial_kinetic_energy = 0 
#final_kinetic_energy = final_row['kinetic_energy'].values[0]

# Calculate the change in kinetic energy
#kinetic_energy_variation = final_kinetic_energy - initial_kinetic_energy

friction_force = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY

last_position = ZERO_POSITION
elastic_work_total_1 = 0
elastic_work_total_2 = 0
total_work_1 = 0
total_work_2 = 0
friction_work_total = 0
total_work_delta = 0

# Compute work done by friction and elastic forces
for index, row in df.iterrows():
    position = row['position']
    speed = row['speed']
    acceleration = row['acceleration']
    elastic_energy = row['elastic_energy']
    kinetic_energy = row['kinetic_energy']

    # Calculate friction work
    friction_work = - friction_force * (position - ZERO_POSITION)
    friction_work_total = friction_work_total + friction_work

    # Calculate elastic work 1
    distance_to_elastic_zero = FINAL_POSITION - row['position']
    elastic_force_1 = ELASTIC_CONSTANT * (2 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - ELASTIC_L0)
    elastic_work_1 = elastic_force_1 * (position - last_position)
    
    # Calculate elastic work 2
    elastic_force_2 = (OBJECT_MASS * acceleration) + friction_force
    elastic_work_2 = elastic_force_2 * (position - last_position)

    elastic_work_total_1 = elastic_work_total_1 + elastic_work_1
    elastic_work_total_2 = elastic_work_total_2 + elastic_work_2

    resultant_force = position * acceleration

    last_position = position

    # Calculate the variation in elastic energy
    #delta_elastic_energy = elastic_energy - df.loc[df['position'] == ZERO_POSITION]['elastic_energy'].values[0]
    
    # Calculate total work with delta elastic energy
   # total_work_delta = total_work_delta + (-delta_elastic_energy + friction_work)

    # Append the works to the respective lists
    friction_works.append(friction_work)
    elastic_works_1.append(elastic_work_1)
    elastic_works_2.append(elastic_work_2)
    total_works_delta.append(total_work_delta)
    total_works_1.append(total_work_1)
    total_works_2.append(total_work_2)
    elastic_energies.append(elastic_energy)  
    kinetic_energies.append(kinetic_energy)
    elastic_forces_1.append(elastic_force_1)
    elastic_forces_2.append(elastic_force_2)
    resultant_forces.append(resultant_force)

# First figure for elastic works
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['position'], y=elastic_works_1, mode='lines+markers', name='Trabajo Elástico 1 (Newton)'))
fig.add_trace(go.Scatter(x=df['position'], y=elastic_works_2, mode='lines+markers', name='Trabajo Elástico 2 (Hooke)')) 

fig.update_layout(
    title='Trabajo Fuerza Elástica vs Posición',
    xaxis_title='Posición (m)',
    yaxis_title='Trabajo Elástico (Joules)',
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

# Second figure for friction works and elastic energy
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=df['position'], y=friction_works, mode='lines+markers', name='Trabajo de Rozamiento'))

fig2.update_layout(
    title='Trabajo de Rozamiento vs Posición',
    xaxis_title='Posición (m)',
    yaxis_title='Trabajo (Joules)',
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

fig2.write_html(OUTPUT_PLOT_PATH_2)
fig2.show()

# Third figure for elastic forces
fig3 = go.Figure()

fig3.add_trace(go.Scatter(x=df['position'], y=elastic_forces_1, mode='lines+markers', name='Fuerza Elástica 1 (Newton)'))
fig3.add_trace(go.Scatter(x=df['position'], y=elastic_forces_2, mode='lines+markers', name='Fuerza Elástica 2 (Hooke)'))
fig3.add_trace(go.Scatter(x=df['position'], y=resultant_forces, mode='lines+markers', name='Fuerza Resultante (F=m.a)'))

fig3.update_layout(
    title='Fuerza Elástica y Resultante vs Posición',
    xaxis_title='Position (m)',
    yaxis_title='Fuerza Elástica (N)',
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

fig3.write_html(OUTPUT_PLOT_PATH_3)
fig3.show()

# Print the final values
print(f"Friction work final: {friction_work_total}")  
print(f"Elastic work final 1: {elastic_work_total_1}")  
print(f"Elastic work final 2: {elastic_work_total_2}")  
print(f"Total work final with delta: {total_work_delta}")  
print(f"Total work final with work elastic 1: {elastic_work_total_1 + friction_work_total}")  
print(f"Total work final with work elastic 2: {elastic_work_total_2 + friction_work_total}")  