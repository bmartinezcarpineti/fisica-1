import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/simple-elastic-data.csv')

GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.75  # unit: N/m

ZERO_POSITION = 0.115
FINAL_POSITION = 0.28333

df = pd.read_csv(INPUT_CSV_PATH)

friction_works = []
elastic_works = []
total_works = []
kinetic_energy_variations = []

for index, row in df.iterrows():
    position = row['position']
    speed = row['speed']

    friction_forces = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY
    
    friction_work = friction_forces * (position - ZERO_POSITION)

    elastic_work = ELASTIC_CONSTANT * 0.5 * (position**2 - ZERO_POSITION**2)
   
    total_work = elastic_work - friction_work

    variation_kinetic_energy = (0.5 * OBJECT_MASS * (speed**2)) - (0.5 * OBJECT_MASS * (0**2))

    friction_works.append(friction_work)
    elastic_works.append(elastic_work)
    total_works.append(total_work)
    kinetic_energy_variations.append(variation_kinetic_energy)

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['time'], y=friction_works, mode='lines', name='Friction Work'))
fig.add_trace(go.Scatter(x=df['time'], y=elastic_works, mode='lines', name='Elastic Work'))
fig.add_trace(go.Scatter(x=df['time'], y=total_works, mode='lines', name='Total Work'))
fig.add_trace(go.Scatter(x=df['time'], y=kinetic_energy_variations, mode='lines', name='Kinetic Energy Variation'))

fig.update_layout(
    title='Work and Kinetic Energy Variation Over Time',
    xaxis_title='Time (s)',
    yaxis_title='Work (Joules) / Kinetic Energy Variation (Joules)',
    legend_title='Legend'
)

output_html_path = os.path.join(THIS_FILE_DIRECTORY_PATH, 'work_energy_variation.html')
fig.write_html(output_html_path)

print(f"Friction work final: {friction_works[-1]}")  
print(f"Elastic work final: {elastic_works[-1]}")  
print(f"Total work final: {total_works[-1]}")  
print(f"Variation kinetic energy final: {kinetic_energy_variations[-1]}")  