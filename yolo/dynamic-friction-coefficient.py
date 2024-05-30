import csv
import os
import numpy as np
import pandas as pd

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/without-elastic-data.csv')
GRAVITY = 9.81

df = pd.read_csv(INPUT_CSV_PATH)

dynamic_friction_coefficient = - df['acceleration'].mean() / GRAVITY # ud = -a/g

acceleration_error = df['acceleration'].std() # acceleration error = accelartion standar deviation

dynamic_friction_coefficient_error = (1 / GRAVITY) * acceleration_error

print(f"\n\nDynamic friction coefficient: {dynamic_friction_coefficient}\n\
Error: {dynamic_friction_coefficient_error}\n\n")