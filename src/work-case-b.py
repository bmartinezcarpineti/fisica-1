import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define paths
STUDY_CASE = 'simple-elastic'
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_PLOT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-work-elastic-case-b.html')
OUTPUT_PLOT_PATH_2 = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'{STUDY_CASE}-frictionwork-energy-case-b.html')

# Constants
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 32.24048176040744  # unit: N/m
ELASTIC_L0 = 0.135  # L0 

ZERO_POSITION = 0.115
FINAL_POSITION = 0.2193333333333333

# Read the input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Initialize lists for works
friction_works = []
elastic_works_1 = []
elastic_works_2 = []
total_works_delta= []
total_works_1= []
total_works_2= []
elastic_energies = []  
kinetic_energies =[]

initial_row = df.loc[df['position'] == ZERO_POSITION]
final_row = df.loc[df['position'] == FINAL_POSITION]

# Kinetic energies
initial_kinetic_energy = 0 
final_kinetic_energy = final_row['kinetic_energy'].values[0]

# Calculate the change in kinetic energy
kinetic_energy_variation = final_kinetic_energy - initial_kinetic_energy

# Compute work done by friction and elastic forces
for index, row in df.iterrows():
    position = row['position']
    speed = row['speed']
    acceleration = row['acceleration']
    elastic_energy = row['elastic_energy']
    kinetic_energy = row['kinetic_energy']

    # Calculate friction work
    friction_force = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY
    friction_work = - friction_force * (position - ZERO_POSITION)
    
    # Calculate elastic work 1
    distance_to_elastic_zero = FINAL_POSITION - row['position']
    elastic_force_1 = ELASTIC_CONSTANT * (2 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - ELASTIC_L0)
    elastic_work_1 = elastic_force_1 * (FINAL_POSITION - position)
    
    # Calculate elastic work 2
    elastic_force_2 = (OBJECT_MASS * acceleration) + friction_force
    elastic_work_2 = elastic_force_2 * (FINAL_POSITION - position)

    # Calculate the variation in elastic energy
    delta_elastic_energy = elastic_energy - df.loc[df['position'] == ZERO_POSITION]['elastic_energy'].values[0]
    
    # Calculate total work with delta elastic energy
    total_work_delta = -delta_elastic_energy + friction_work

    # Calculate total work with elastic work 1
    total_work_1 = elastic_work_1 + friction_work
    
    # Calculate total work with elastic work 2
    total_work_2 = elastic_work_2 + friction_work
    
    # Append the works to the respective lists
    friction_works.append(friction_work)
    elastic_works_1.append(elastic_work_1)
    elastic_works_2.append(elastic_work_2)
    total_works_delta.append(total_work_delta)
    total_works_1.append(total_work_1)
    total_works_2.append(total_work_2)
    elastic_energies.append(elastic_energy)  
    kinetic_energies.append(kinetic_energy)

# First figure for elastic works
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['position'], y=elastic_works_1, mode='lines+markers', name='Trabajo Elástico 1'))
fig.add_trace(go.Scatter(x=df['position'], y=elastic_works_2, mode='lines+markers', name='Trabajo Elástico 2')) 

fig.update_layout(
    title='Trabajo Fuerza Elástica',
    xaxis_title='Position (m)',
    yaxis_title='Trabajo Elástico (Joules)',
)

fig.write_html(OUTPUT_PLOT_PATH)
fig.show()

# Second figure for friction works and elastic energy
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=df['position'], y=friction_works, mode='lines+markers', name='Trabajo de Rozamiento'))
fig2.add_trace(go.Scatter(x=df['position'], y=elastic_energies, mode='lines+markers', name='Energía Elástica'))

fig2.update_layout(
    title='Trabajo de Rozamiento y Energía Elástica',
    xaxis_title='Position (m)',
    yaxis_title='Trabajo - Energía (Joules)',
)

fig2.write_html(OUTPUT_PLOT_PATH_2)
fig2.show()

# Print the final values
print(f"Friction work final: {friction_works[-1]}")  
print(f"Elastic work final 1: {elastic_works_1[-1]}")  
print(f"Elastic work final 2: {elastic_works_2[-1]}")  
print(f"Total work final with delta: {total_works_delta[-1]}")  
print(f"Total work final with work elastic 1: {total_works_1[-1]}")  
print(f"Total work final with work elastic 2: {total_works_2[-1]}")  
print(f"Kinetic Energy Variation: {kinetic_energy_variation}")
