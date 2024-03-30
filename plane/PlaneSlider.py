import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PlanePlot import fig, ax, line, label
from PlaneDataModel import time_domain, position_values, velocity_values

slider_ax = fig.add_axes([0.2, 0.9, 0.65, 0.03])
slider = Slider(ax=slider_ax, label='Time (s)', valmin=0, valmax=len(time_domain) - 1, valinit=0, valfmt='%d')


# Function to update plot based on slider value
def update_plot(val):
    frame = int(val)

    positions = position_values[:frame + 1]
    line.set_xdata(positions)
    line.set_ydata(velocity_values[:frame + 1])

    line.set_label(label(frame))
    ax.set_ylim(0, max(velocity_values[frame] * 1.1, ax.get_ylim()[1]))
    ax.set_xlim(0, position_values[frame] * 1.1)
    ax.legend()

    fig.canvas.draw_idle()  # Update the plot efficiently


# Connect slider to update function
slider.on_changed(update_plot)

plt.show()
