import csv
import os
import numpy as np
import pandas as pd

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/without-elastic-data.csv')
GRAVITY = 9.81 # unit: m/s^s
OBJECT_MASS = 0.284 # unit: kg
DYNAMIC_FRICTION_COEFFICIENT = 0.8
ELASTIC_CONSTANT = 74.75 # unit: N/m

# for elastic work
ZERO_POSITION = 0.115
FINAL_POSITION = 0.28333 

# Using theorem of living forces Wtotal = Welastic + Wfriction
# calculates friction forces
friction_forces = DYNAMIC_FRICTION_COEFFICIENT * OBJECT_MASS * GRAVITY

# calculates friction work
friction_work = friction_forces * (FINAL_POSITION - ZERO_POSITION)

# calculates elastic work
elastic_work = ELASTIC_CONSTANT * 0.5 * (FINAL_POSITION**2 - ZERO_POSITION**2)#obs: falta hacerlo con delta x

total_work = elastic_work - friction_work

print(f"Friction work: {friction_work}") #0.375
print(f"Elastic work: {elastic_work}") #2.506
print(f"Total work: {total_work}") #2.13
