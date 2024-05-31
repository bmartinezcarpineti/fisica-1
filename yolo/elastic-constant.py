import csv
import os
import numpy as np
import pandas as pd
import math

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/elastic-data.csv')

GRAVITY = 9.81 # unit: m/s^s
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_L0 = 0.135 # unit: m
OBJECT_MASS = 0.284 # unit: kg

elastic_constants = []

df = pd.read_csv(INPUT_CSV_PATH)

for index, row in df.iterrows():
    acceleration = row['acceleration']
    position = row['position']

    elastic_constant_numerator = OBJECT_MASS * (acceleration + DYNAMIC_FRICTION_COEFFICIENT * GRAVITY) * np.sqrt((ELASTIC_L0/2)**2 + position**2)
    elastic_constant_denominator = 2 * position * (2 * np.sqrt((ELASTIC_L0/2)**2 + position**2) - ELASTIC_L0)

    elastic_constant = elastic_constant_numerator / elastic_constant_denominator

    elastic_constants.append(elastic_constant)

cleaned_elastic_constants = [i for i in elastic_constants if not math.isnan(i)] # removes NaN values

mean_elastic_constant = np.mean(cleaned_elastic_constants)

print(cleaned_elastic_constants)
print(f"\n\nElastic constant: {mean_elastic_constant}\n\n")