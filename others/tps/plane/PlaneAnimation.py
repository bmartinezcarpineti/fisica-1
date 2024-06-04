import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PlaneDataModel import position_values, velocity_values, time_domain
from PlanePlot import fig, ax, line, label


def update(frame):
    positions = position_values[:frame]
    line.set_xdata(positions)
    line.set_ydata(velocity_values[:frame])
    line.set_label(label(frame))
    ax.set_ylim(0, max(velocity_values[frame] * 1.1, ax.get_ylim()[1]))
    ax.set_xlim(0, position_values[frame] * 1.1)
    ax.legend()
    return frame


ani = animation.FuncAnimation(fig=fig, func=update, frames=len(time_domain), interval=75)
plt.show()
