import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Define paths
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/simple-elastic-data.csv')

# Constants
GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.75  # unit: N/m
ELASTIC_L0 = 0.135  # L0 

ZERO_POSITION = 0.115
FINAL_POSITION = 0.2193333333333333

# Read the input CSV file
df = pd.read_csv(INPUT_CSV_PATH)

# Initialize lists for works
friction_works = []
elastic_works = []
total_works = []

# Find the rows corresponding to the zero and final positions
initial_row = df.loc[df['position'] == ZERO_POSITION]
final_row = df.loc[df['position'] == FINAL_POSITION]

# Kinetic energies
initial_kinetic_energy = 0  # Given as zero
final_kinetic_energy = final_row['kinetic_energy'].values[0]

# Calculate the change in kinetic energy
kinetic_energy_variation = final_kinetic_energy - initial_kinetic_energy

# Compute work done by friction and elastic forces
for index, row in df.iterrows():
    position = row['position']
    speed = row['speed']
    elastic_energy = row['elastic_energy']

    # Calculate friction work
    friction_force = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY
    friction_work = - friction_force * (position - ZERO_POSITION)
    
    # Calculate the variation in elastic energy
    delta_elastic_energy = elastic_energy - df.loc[df['position'] == ZERO_POSITION]['elastic_energy'].values[0]
    
    # Calculate total work
    total_work = -delta_elastic_energy + friction_work

    # Append the works to the respective lists
    friction_works.append(friction_work)
    elastic_works.append(elastic_energy * (FINAL_POSITION - position))
    total_works.append(total_work)

# Plot the results
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['position'], y=friction_works, mode='lines+markers', name='Friction Work'))
fig.add_trace(go.Scatter(x=df['position'], y=elastic_works, mode='lines+markers', name='Elastic Work'))
fig.add_trace(go.Scatter(x=df['position'], y=total_works, mode='lines+markers', name='Total Work'))

fig.update_layout(
    title='Work Case B',
    xaxis_title='Position (m)',
    yaxis_title='Friction Work - Elastic Work - Total Work (Joules)',
    legend_title='Legend'
)

output_html_path = os.path.join(THIS_FILE_DIRECTORY_PATH, 'work_case_b.html')
fig.write_html(output_html_path)

# Print the final values
print(f"Friction work final: {friction_works[-1]}")  
print(f"Elastic work final: {elastic_works[-1]}")  
print(f"Total work final: {total_works[-1]}")  
print(f"Kinetic Energy Variation: {kinetic_energy_variation}")
