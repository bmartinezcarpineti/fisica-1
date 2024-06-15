import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import interpolate

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/simple-elastic-data.csv')

GRAVITY = 9.81  # unit: m/s^2
OBJECT_MASS = 0.284  # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.75  # unit: N/m
ELASTIC_L0 = 0.135  # L0 

ZERO_POSITION = 0.115
FINAL_POSITION = 0.2193333333333333 #0.28333

df = pd.read_csv(INPUT_CSV_PATH)

# Filtrar el DataFrame para incluir solo posiciones >= ZERO_POSITION
df_filtered = df[df['position'] >= ZERO_POSITION]

# Asegurarse de que la posición final esté incluida mediante interpolación
if FINAL_POSITION not in df_filtered['position'].values:
    # Interpolar los valores de velocidad y energía cinética en la posición final
    interpolation_function_speed = interpolate.interp1d(df_filtered['position'], df_filtered['speed'], fill_value="extrapolate")
    interpolated_speed = interpolation_function_speed(FINAL_POSITION)

    # Calcular la energía cinética en la posición final interpolada
    interpolated_kinetic_energy = 0.5 * OBJECT_MASS * interpolated_speed**2

    # Crear un DataFrame para la posición final interpolada
    interpolated_row = pd.DataFrame({
        'time': [None],  
        'position': [FINAL_POSITION],
        'speed': [interpolated_speed],
        'acceleration': [None],  
        'elastic_energy': [None],  
        'kinetic_energy': [interpolated_kinetic_energy]
    })

    # Eliminar columnas que están completamente vacías
    interpolated_row = interpolated_row.dropna(axis=1, how='all')
    
    # Concatenar el DataFrame original con el DataFrame de la posición final interpolada
    df_filtered = pd.concat([df_filtered, interpolated_row], ignore_index=True)

df_filtered = df_filtered.sort_values(by='position').reset_index(drop=True)

kinetic_energy_variations = []
friction_works = []
elastic_works = []
total_works = []
previous_kinetic_energy = 0

friction_forces = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY
last_position = ZERO_POSITION
ELASTIC_ZERO_POSITION = 0.28

for index, row in df_filtered.iterrows():
    position = row['position']
    kinetic_energy = row['kinetic_energy']
    distance_to_elastic_zero = FINAL_POSITION - row['position']

    if pd.notna(kinetic_energy):  # Asegurarse de que la energía cinética no sea NaN
        delta_kinetic_energy = kinetic_energy - previous_kinetic_energy
        kinetic_energy_variations.append(delta_kinetic_energy)
        previous_kinetic_energy = kinetic_energy
    else:
        kinetic_energy_variations.append(0)  # Añadir 0 si la energía cinética es NaN
    
    friction_work = - (friction_forces * (position - last_position))
    
    distance_to_elastic_zero = ELASTIC_ZERO_POSITION - row['position']
    elastic_force = (1/2) * ELASTIC_CONSTANT * (4 * ((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) - 4 * np.sqrt((ELASTIC_L0/2)**2 + distance_to_elastic_zero**2) * ELASTIC_L0 + ELASTIC_L0**2)
    elastic_work = elastic_force * (position - last_position)

    total_work = elastic_work + friction_work
    
    last_position = position
    friction_works.append(friction_work)
    elastic_works.append(elastic_work)
    total_works.append(total_work)

# Filtrar el DataFrame y la lista de variaciones para incluir solo hasta la posición final
df_filtered = df_filtered[df_filtered['position'] <= FINAL_POSITION]
kinetic_energy_variations = kinetic_energy_variations[:len(df_filtered)]
friction_works = friction_works[:len(df_filtered)]
elastic_works = elastic_works[:len(df_filtered)]
total_works = total_works[:len(df_filtered)]

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_filtered['position'], y=kinetic_energy_variations, mode='lines', name='Kinetic Energy Variation'))
fig.add_trace(go.Scatter(x=df_filtered['position'], y=friction_works, mode='lines', name='Friction Work'))
fig.add_trace(go.Scatter(x=df_filtered['position'], y=elastic_works, mode='lines', name='Elastic Work'))
fig.add_trace(go.Scatter(x=df_filtered['position'], y=total_works, mode='lines', name='Total Work'))

fig.update_layout(
    title='Work and Kinetic Energy Variation Over Position',
    xaxis_title='Position (m)',
    yaxis_title='Work and Kinetic Energy Variation (Joules)',
    legend_title='Legend'
)

output_html_path = os.path.join(THIS_FILE_DIRECTORY_PATH, 'work_and_kinetic_energy_variation.html')
fig.write_html(output_html_path)

print(f"Variation kinetic energy final: {kinetic_energy_variations[-1]}")
print(f"Friction work final: {friction_works[-1]}")  
print(f"Elastic work final: {elastic_works[-1]}")  
print(f"Total work final: {total_works[-1]}")  