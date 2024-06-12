import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime

THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
STUDY_CASE = "friction"
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, f'data/{STUDY_CASE}-data.csv')
OUTPUT_TXT_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'results', f'{STUDY_CASE}', f'dynamic-friction-coefficient.txt')

GRAVITY = 9.81 # unit: m/s^s

df = pd.read_csv(INPUT_CSV_PATH)

dynamic_friction_coefficient = - df['acceleration'].mean() / GRAVITY # ud = -a/g

# calculates error
acceleration_error = df['acceleration'].std() # acceleration error = accelartion standard deviation
dynamic_friction_coefficient_error = (1 / GRAVITY) * acceleration_error

OUTPUT_STRING = f"Dynamic friction coefficient: {dynamic_friction_coefficient}\n\
Error: {dynamic_friction_coefficient_error}\n\nDate: {datetime.now()}"

with open(OUTPUT_TXT_PATH, "w") as file:
    file.write(OUTPUT_STRING)

print(OUTPUT_STRING)