import csv
import os
import numpy as np
import pandas as pd
from tabulate import tabulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# files constants
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/positions.csv')
OUTPUT_CSV_PATH = os.path.join(THIS_FILE_DIRECTORY_PATH, 'data/without-elastic-data.csv')

input_df = pd.read_csv(INPUT_CSV_PATH)

# reduces noise
reduced_noise_time = input_df['time'].iloc[::5]
reduced_noise_position = input_df['position'].iloc[::5]

# output dataframe
df = pd.DataFrame()
df['time'] = reduced_noise_time
df['position'] = reduced_noise_position

# calculates speed and acceleration
df['speed'] = df['position'].diff() / df['time'].diff()
df['acceleration'] = df['speed'].diff() / df['time'].diff()

df.to_csv(OUTPUT_CSV_PATH)

# shows results
print(tabulate(df, headers='keys', tablefmt='psql'))