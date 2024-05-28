import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# files constants
GRAPHER_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIRECTORY = os.path.join(GRAPHER_DIRECTORY_PATH, 'plots')

all_object_position_in_x = []
all_object_detection_time = []
all_object_speed_in_x = []
all_object_acceleration_in_x = []
all_object_force_in_x = []
TIME_DIFFERENCE = 1 / 240 # 1 / FPS
previous_position = None
previous_speed = None
OBJECT_MASS = 0.283 # unit: kg

with open('positions.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    all_object_position_in_x = next(reader)

all_object_position_in_x = [float(num) for num in all_object_position_in_x]
all_object_detection_time = [TIME_DIFFERENCE + i * TIME_DIFFERENCE for i in range(len(all_object_position_in_x))]

#reduce the noise
all_object_position_in_x = all_object_position_in_x[::3]
all_object_detection_time = all_object_detection_time[::3]

#speed calculation
for position in all_object_position_in_x:
    if previous_position is not None:
        object_position_in_x_difference = position - previous_position
        object_speed_in_x = object_position_in_x_difference / TIME_DIFFERENCE
        all_object_speed_in_x.append(object_speed_in_x)
    previous_position = position

#acceleration calculation
for speed in all_object_speed_in_x:
    if previous_speed is not None:
        object_speed_in_x_difference = speed - previous_speed
        object_acceleration_in_x = object_speed_in_x_difference / TIME_DIFFERENCE
        all_object_acceleration_in_x.append(object_acceleration_in_x)
    previous_speed = speed

# object variables in function of time plot
plt.subplot(311)
plt.plot(all_object_detection_time, all_object_position_in_x, label="Position in X")
plt.ylabel("m")
plt.legend()

plt.subplot(312)
all_object_detection_time.pop(0)
plt.plot(all_object_detection_time, all_object_speed_in_x, label="Speed in X")
plt.ylabel("m/s")
plt.legend()

plt.subplot(313)
all_object_detection_time.pop(0)
plt.plot(all_object_detection_time, all_object_acceleration_in_x, label="Acceleration in X")
plt.ylabel("m/s^2")
plt.xlabel("Time (s)")
plt.legend()

plt.savefig(os.path.join(PLOTS_DIRECTORY, 'object_in_function_of_time.png'))

plt.clf()

# force in function of position calculation
for acceleration in all_object_acceleration_in_x:
    all_object_force_in_x.append(OBJECT_MASS * acceleration)

all_object_position_in_x = np.delete(all_object_position_in_x,0)
all_object_position_in_x = np.delete(all_object_position_in_x,0)
plt.subplot(211)
plt.plot(all_object_position_in_x, all_object_acceleration_in_x, label="Acceleration in X")
plt.ylabel("m/s^2")
plt.legend()

plt.subplot(212)
plt.plot(all_object_position_in_x, all_object_force_in_x, label="Force in X")
plt.ylabel("N (kg * m/s^2)")
plt.xlabel("Position in X (m)")
plt.legend()

plt.savefig(os.path.join(PLOTS_DIRECTORY, 'object_in_function_of_position.png'))