import matplotlib.pyplot as plt
from PlaneDataModel import position_values, velocity_values, accel_values


def label(time_index):
    position = position_values[time_index]
    velocity = velocity_values[time_index]
    accel = accel_values[time_index]
    return f'x={position:.0f} m\nv={velocity:.2f} m/s\na={accel:.2f} m/s^2'


fig, ax = plt.subplots()
line = ax.plot(position_values[0], 1, label=label(0))[0]
ax.set(xlim=[0, 1000000], ylim=[0, 250], xlabel="Distance (m)", ylabel="Speed (m/s)")
ax.legend()
