import csv
import os
import numpy as np
import pandas as pd
import math

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/elastic-data.csv')

OBJECT_MASS = 0.284 # unit: kg

kinetic_energies = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    speed = row['speed']
    
    kinetic_energy = (1/2) * OBJECT_MASS * (speed**2)

    kinetic_energies.append(kinetic_energy)

cleaned_kinetic_energies = [i for i in kinetic_energies if not math.isnan(i)] # removes NaN values

print(cleaned_kinetic_energies)