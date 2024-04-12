import math
import numpy as np


def time_to_accel(timeset, accel):
    return np.full(len(timeset), accel)


def time_to_velocity(timeset, t0, v0, accel):
    if accel == 0:
        return np.full(len(timeset), v0)
    return v0 + accel * (timeset - t0)


def time_to_positions(timeset, t0, x0, v0, accel):
    if v0 == 0 and accel == 0:
        return np.full(len(timeset), x0)
    return x0 + v0 * (timeset - t0) + accel * (timeset - t0) ** 2 / 2


def map_time_to_values(timeset, t0, x0, v0, a0):
    return time_to_accel(timeset, a0), time_to_velocity(timeset, t0, v0, a0), time_to_positions(timeset, t0, x0, v0, a0)


def setup_time_range(start_time, end_time, frames_scale=1.0, t0=0.0, x0=0.0, v0=0.0, a0=0.0):
    """
    Builds a time domain and MRUV functions.
    :param start_time: start time of domain (in seconds)
    :param end_time: end time of domain (in seconds)
    :param frames_scale: frames for each second. Default: 1 frame per second.
    :param t0: initial time for MRUV funcs (in seconds). Default: 0 s.
    :param x0: initial position for MRUV funcs (in meters). Default: 0 m.
    :param v0: initial velocity for MRUV funcs (in meters/seconds). Default: 0 m/s.
    :param a0: initial acceleration for MRUV funcs (in meters/seconds^2). Default: 0 m/s^2.
    :return: tuple (time_domain, positions, velocity, acceleration).
        All arrays are guaranteed to have the same length. For each value (index) in the time domain there exists a
        corresponding value in positions, velocity and acceleration.
    """
    frames = math.ceil((end_time - start_time) * frames_scale)
    time = np.linspace(start_time, end_time, frames)
    accel, velocity, positions = map_time_to_values(time, t0, x0, v0, a0)
    return time, positions, velocity, accel
