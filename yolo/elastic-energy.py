import csv
import os
import numpy as np
import pandas as pd
import math

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/elastic-data.csv')

ELASTIC_L0 = 0.135 # unit: m
ELASTIC_CONSTANT = 9.76 # unit: N/m

elastic_energies = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    position = row['position']
    
    elastic_energy = (1/2) * ELASTIC_CONSTANT * (4 * ((ELASTIC_L0/2)**2 + position**2)**2 - 4 * ((ELASTIC_L0/2)**2 + position**2) * ELASTIC_L0 + ELASTIC_L0**2)

    elastic_energies.append(elastic_energy)

print(elastic_energies)